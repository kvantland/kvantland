#!/usr/bin/python3

from html import escape
from bottle import route, request, response, redirect
import nav
import user
import sys
from login import current_user, do_login
import approv
import hmac
import email.message
from email.message import EmailMessage
import smtplib
from config import config

_key = config['keys']['mail_confirm']

all_info = [['name', 'text', 'Имя'],
			['surname', 'text', 'Фамилия'],
			['school', 'text', 'Школа'],
			['town', 'text', 'Город'],
			['email', 'email', 'Почта'],
			['clas', 'select', 'Класс', ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', 'Другое']]]

alph_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
alph_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
symb = ' -_'

# поля в которых могут использоваться только буквы и символы из symb
lett_only = ['name', 'surname', 'town']

field_amount = len(all_info) + 1 # количество полей в форме
field_size = 40 # размер поля
pad = 4 # расстояние между полями
button_margin = 20 # расстояние до кнопки
button_size = 70 # размер кнопки
form_size = button_size + field_amount * field_size + pad * field_amount + button_margin # размер формы

# типы полей
type_info = dict()

# Отображаемые названия полей
placeholder_info = dict()

# Опции для полей с выбором
option_info = dict()

# Заполнение словарей
for field in all_info:
	field_name = field[0]
	type_name = field[1]
	placeholder_name = field[2]
	type_info[field_name] = type_name
	placeholder_info[field_name] = placeholder_name
	if type_name == 'select':
		options = field[3]
		option_info[field_name] = options

def empty_user_info():
	user_info = dict()
	for field in all_info:
		user_info[field[0]] = ''
	return user_info

def req_query(params):
	query = []
	for key, val in params.items():
		query.append(f'{key}={val}')
	return '&'.join(query)

@route('/acc')
def display_pers_acc(db, err={}, user_info=empty_user_info()):
	if current_user(db) == None:
		redirect('/')
	yield '<!DOCTYPE html>'
	yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
	yield '<title> Личный кабинет — Квантландия </title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/acc.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/approv.css">'

	yield from user.display_banner_acc(db)
	yield '<div class="content_wrapper">'
	yield '<div class="acc_form">'
	yield '<div class="header"> Личный кабинет </div>'
	yield f'<form id="acc" method="post">'
	yield '<div class="fields">'
	start_user_info = get_user(db, current_user(db))
	for i in range(len(all_info)):
		field = all_info[i]
		name = field[0]
		if user_info[name]:
			value_ = user_info[name]
		else:
			value_ = start_user_info[name]
		if value_ == None:
			value_ = ''
		yield '<div class="full_field">'
		yield '<div class="field">'
		yield '<div class="content">'
		placeholder_ = placeholder_info[name]
		type_ = type_info[name]
		yield f'<div class="placeholder"> {placeholder_} </div>'
		if type_ == 'select':
			yield f'<div class="select_line" name="{name}">'
			yield f' <input name="{name}" type="{type_}" value="{escape(value_)}" readonly required />'
			yield '<img class="arrow" src="/static/design/icons/down_arrow.svg" />'
			yield '</div>'
		else:
			yield f'<input name="{name}" type="{type_}" value="{escape(value_)}" required />'
		yield '</div>'
		if err and name in err.keys():
			yield '<div class="info"> <img src="/static/design/icons/info.svg" /> </div>'
			yield '</div>'
			yield f'<div class="err"> {err[name]} </div>'
		else:
			yield '<div class="info hidden"> <img src="/static/design/icons/info.svg" /> </div>'
			yield '</div>'
			yield f'<div class="err hidden"></div>'
		if type_ == 'select':
			yield f'<div class="select_box hidden" name="{name}">'
			opt_list = option_info[name]
			for opt in opt_list:
				if user_info[name] != str(opt):
					yield f'<div class="option"> {opt} </div>'
				else:
					yield f'<div class="option selected"> {opt} </div>'
			yield '</div>'
		yield '</div>'
	yield '</div>'
	yield '<div class="full_field">'
	yield '<div class="check_cont">'
	yield '<input class="checkbox" type="checkbox" name="approval" id="approval" required />'
	yield '''<div class="label"> Я принимаю условия <a href="/policy"> Политики конфиденциальности</a> и даю <span class="underline approval"> согласие
		на обработку своих персональных данных</span>'''
	yield '</div>'
	yield '</div>'
	if err and 'approval' in err.keys():
		yield f'<div class="err"> {err["approval"]} </div>'
	else:
		yield f'<div class="err hidden"></div>'
	yield '</div>'
	yield '</form>'
	yield '<div class="button_area">'
	yield f'<button type="submit" class="acc_button" form="acc"> Сохранить </button>'
	yield '<hr size="1">'
	yield f'<a href="/"><div class="back_button"> Назад </div></a>'
	yield '</div>'
	yield '</div>'

	yield from approv.display_confirm_window()

	yield '<script type="text/javascript" src="/static/design/user.js"></script>'
	yield '<script type="text/javascript" src ="/static/dialog.js"></script>'
	yield '<script type="text/javascript" src ="/static/design/acc.js"></script>'
	yield '<script src="https://www.google.com/recaptcha/api.js" async defer></script>'

def get_user(db, user):
	db.execute('select name, surname, school, town, clas, score, email from Kvantland.Student where student= %s', (user, ))
	user_list = list(db.fetchall()[0])
	user_info = {'name': user_list[0],
				'surname': user_list[1],
				'school': user_list[2],
				'town': user_list[3],
				'clas': user_list[4],
				'score': user_list[5],
				'email': user_list[6]}
	return user_info

def check_format(user_info):
	err_dict = {}

	for field in user_info:
		try:
			min_size = config['acc']['min_' + field + '_size']
		except:
			min_size = 1
		try:
			max_size = config['acc']['max_' + field + '_size']
		except:
			max_size = 500
		name = placeholder_info[field]

		if type_info[field] == "select":
			if not(user_info[field] in option_info[field]):
				err_dict[field] = "Значение не из списка"

		if len(user_info[field]) < min_size:
			err_dict[field] = "Слишком мало символов в поле, <br /> должно быть минимум " + str(min_size)
		if len(user_info[field]) > max_size:
			err_dict[field] = "Слишком много символов"

	return err_dict

def update_info(user_info, err_dict):
	for field in err_dict:
		if field in user_info.keys():
			user_info[field] = ''
	return user_info

@route('/acc', method="POST")
def check_new_params(db):
	user_info = dict()

	for field in all_info:
		name = field[0]
		new_value = request.forms.get(name).encode('l1').decode().strip()
		user_info[name] = new_value

	err_dict = check_format(user_info)

	db.execute("select login from Kvantland.Student where student = %s", (current_user(db), ))
	(login, ), = db.fetchall()
	user_info['login'] = login

	approval = request.forms['approval']
	if not approval:
		err_dict['approval'] = 'Поставьте галочку'

	if not err_dict:
		update_user(db, user_info)
		if new_mail(db, user_info):
			yield from send_reg_confirm_message(user_info)
			yield from show_send_message(user_info['email'], db)
		else:
			redirect('/')
	else:
		user_info = update_info(user_info, err_dict)
		yield from display_pers_acc(db, err_dict, user_info)

def new_mail(db, info):
	if not current_user(db):
		return True
	else:
		db.execute("select email from Kvantland.Student where student = %s", (current_user(db), ))
		(_email, ), = db.fetchall()
		if not _email:
			return True
		if _email != info['email']:
			return True
		
	return False

def show_send_message(email, db):
	yield '<!DOCTYPE html>'
	yield '<title>Личный кабинет — Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/acc.css">'
	yield from user.display_banner_acc(db)
	yield '<div class="content_wrapper">'
	yield '<div class="advert_form">'
	yield '<div class="header"> Смена адреса электронной почты </div>'
	yield '''<div class="description"> 
		Письмо для подтверждения смены адреса</br>
		электронной почты, привязанной к вашему</br>
		аккаунту успешно отправлено! </div>'''
	yield '<div id="advert">'
	yield '<div class="full_field">'
	yield '<div class="field">'
	yield '<div class="content">'
	yield '<div class="placeholder"> Почта </div>'
	yield f'<div class="input"> {email} </div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '<script type="text/javascript" src="/static/design/user.js"></script>'

def send_reg_confirm_message(info):
	_email = info['email']
	name = info['name']
	try:
		token = hmac.new(_key.encode('utf-8'), _email.encode('utf-8'), 'sha256').hexdigest()
		info['token'] = token
		link = f'''
		{config['recovery']['acc_confirm_uri']}?{req_query(info)}
		'''
		localhost = config['recovery']['localhost']
		host = config['recovery']['host']
		port = config['recovery']['port']
		login = config['recovery']['login']
		password = config['recovery']['password']
		sender = config['recovery']['sender']

		server = smtplib.SMTP_SSL(host, port, local_hostname=localhost, timeout=120)
		email_content =  f'''
			<!DOCTYPE html>
			<head>
			<link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Montserrat">
   			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    		<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>Восстановление пароля</title>
			</head>
			<body style="padding: 80px;
				font-family: Montserrat, Arial !important;
				word-wrap: break-word;
				font-size: 20px;
				font-weight: 500;">
			<div style="font-family: Montserrat, Arial !important;">
			<div style="font-family: Montserrat, Arial !important;"> Здравствуйте, {name}! </div>
			<div style="margin-top: 20px"> 
				 Недавно был получен запрос на изменение адреса электронной почты, связанной с вашей учетной записью. 
				Если вы запрашивали это изменение, нажмите на ссылку ниже для подтверждения: </div>
			</div>
			<div style="width: 640px;
				margin: 80px auto; 
				background: #1E8B93; 
				box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.25); 
				border-radius: 6px;">
			<a href="{link}" style="text-decoration: none">
			<div style="text-align: center;
				padding: 10px 0;
				color: white; 
				font-weight: 600;
				box-sizing: border-box;
				font-family: Montserrat, Arial !important;">
			Нажмите здесь для подтверждения
			</div>
			</a>
			</div>
			<div>
			<div style="font-family: Montserrat, Arial !important;"> Если вам не нужно менять адрес электронной почты, 
			просто проигнорируйте данное сообщение.</div>
			<div style="margin-top: 20px; font-family: Montserrat, Arial !important;"> С уважением, команда Kvantland </div>
			</div>
			</body>
			</html>'''

		msg = EmailMessage()
		msg['Subject'] = 'Email changing'
		msg['From'] = sender
		msg['To'] = _email
		msg.set_content(email_content, subtype='html')

		server.login(str(login), str(password))
		try:
			server.sendmail(sender, [_email], msg.as_string())
		except:
			redirect('/')
		finally:
			server.quit()	
	except ValueError:
		yield from display_registration_form(info, err={'email':'Неверный адрес электронной почты'})
		return

def update_user(db, info):
	db.execute("update Kvantland.Student set name = %s, surname = %s, school = %s, clas = %s, town = %s where login = %s returning student", (info['name'], info['surname'], info['school'], info['clas'], info['town'], info['login']))
	(user, ), = db.fetchall()
	return int(user)

def update_email(db, info):
	db.execute("update Kvantland.Student set email = %s where login = %s returning student", (info['email'], info['login']))
	(user, ), = db.fetchall()
	return int(user)

@route('/acc_confirm')
def check(db):
	email = request.query['email']
	token = request.query['token']
	if not email or not token:
		redirect('/')
	elif hmac.new(_key.encode('utf-8'), email.encode('utf-8'), 'sha256').hexdigest() != token:
		redirect('/')
	else:
		user_info = request.query.decode()
		del user_info['token']
		user = update_email(db, user_info)
		do_login(user, user_info['login'])
		redirect('/')
