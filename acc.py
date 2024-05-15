#!/usr/bin/python3

from html import escape
from bottle import route, request, response, redirect
import nav
import user
import sys
from login import current_user, do_login, check_token
import approv
import hmac
import email.message
from email.message import EmailMessage
import smtplib
from config import config
import time
import math

import urllib.parse
import json

@route('/api/tournament_results')
def get_tournament_results(db):
	tournament_results = []
	tournament_amount = get_tournament_amount(db, config['tournament']['version'], config['tournament']['season'])
	for tournament in range(0, tournament_amount):
		tournament_results.append(
			{
				'title': f'{to_roman_number(tournament_amount - tournament)} Турнир',
				'score': get_score_text(db, config["tournament"]["version"] - tournament),
            }
        )
	return json.dumps(tournament_results)

@route('/api/acc_fields')
def get_acc_fields():
	fields = [
		    {'type': "input", 'inputType': "text", 'name':"name", 'placeholder':"Имя"},
			{'type': "input", 'inputType': "text", 'name': "surname", 'placeholder': "Фамилия"},
			{'type': "input", 'inputType': "text", 'name': "school", 'placeholder': "Школа"},
			{'type': "input", 'inputType': "text", 'name': "town", 'placeholder': "Город"},
			{'type': "input", 'inputType': "email", 'name': "email", 'placeholder': "Почта"},
			{'type': "select", 'options': [str(i) for i in range(1, 12)] + ['Другое'], 'name': "clas", 'placeholder': "Класс"},
		]
	return json.dumps(fields)

def is_new_email(db, new_email, login):
	try:
		db.execute("select email from Kvantland.Student where login = %s", (login, ))
		(prev_email, ), = db.fetchall()
		print(prev_email, new_email, file=sys.stderr)
		if prev_email != new_email:
			return True
	except:
		return False
	return False

@route('/api/update_user_info', method="POST")
def update_user_info(db):
	resp = {
		'status': "updated",
		'email_changed': False,
    }
	update_info = json.loads(request.body.read())
	check_token_status = check_token(request)
	if check_token_status['error']:
		response.status = 400
		return json.dumps({'error': check_token_status['error']})
	else:
		user = check_token_status['login']
	try:
		db.execute('update Kvantland.Student set name=%s, surname=%s, school=%s, clas=%s, town=%s where login=%s', 
			(update_info['name'], update_info['surname'], update_info['school'], update_info['clas'], update_info['town'], 
	            user))
	except:
		resp['status'] = "rejected"
		
	if 'email' in update_info.keys():
		if is_new_email(db, update_info['email'], user):
			resp['email_changed'] = True
	print(resp, file=sys.stderr)
	return json.dumps(resp)


@route('/api/check_email_amount', method="POST")
def check_user_email_amount(db):
	check_token_status = check_token(request)
	if check_token_status['error']:
		response.status = 400
		return json.dumps({'error': check_token_status['error']})
	else:
		user = check_token_status['login']
		
	email = json.loads(request.body.read())['email']
	print(email, file=sys.stderr)
	
	db.execute('select first_mail from Kvantland.Mail where mail = %s', (email, ))
	first_ = db.fetchall()
	if len(first_) > 0:
		(first_email, ), = first_
	else:
		first_email = time.time()
		db.execute('insert into Kvantland.Mail (mail, first_mail) values(%s, %s)', (email, first_email))
	print(first_email, file=sys.stderr)
	if time.time() - first_email > config['mail_check']['allowed_period']:
		return json.dumps({'status': True})
	else:
		db.execute('select remainig_mails from Kvantland.Mail where mail = %s', (email, ))
		(remainig_mails, ), = db.fetchall()
		if remainig_mails > 0:
			return json.dumps({'status': True})
	return json.dumps({'status': False, 'error': "Not enough time passed"})

		
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

def to_roman_number(num):
	romansDict = {
			1: "I",
			5: "V",
			10: "X",
			50: "L",
			100: "C",
			500: "D",
			1000: "M",
			5000: "G",
			10000: "H"
		}
	div = 1
	while num >= div:
		div *= 10

	div /= 10

	res = ""

	while num:
		lastNum = int(num / div)

		if lastNum <= 3:
			res += (romansDict[div] * lastNum)
		elif lastNum == 4:
			res += (romansDict[div] +
					romansDict[div * 5])
		elif 5 <= lastNum <= 8:
			res += (romansDict[div * 5] +
					(romansDict[div] * (lastNum - 5)))
		elif lastNum == 9:
			res += (romansDict[div] +
					romansDict[div * 10])
 
		num = math.floor(num % div)	
		div /= 10 
	return res

def get_tournament_amount(db, tournament, season):
	db.execute('select tournament from Kvantland.Season where season=%s', (season, ))
	tournaments = db.fetchall()
	return len(tournaments)

def get_score_text(db, tournament):
	if tournament == config['tournament']['version']:
		return "Идёт сейчас"
	db.execute('select score from Kvantland.Score where student=%s and tournament=%s', (current_user(db), tournament, ))
	try:
		(score, ), = db.fetchall()
	except ValueError:
		return "Не принимал участия"
	db.execute('select sum(points) from Kvantland.Problem where tournament=%s', (tournament, ))
	(total_score, ), = db.fetchall()
	total_score += 10 # вынести в config!
	return f'Счёт: {score}/{total_score} {lang_form(score)}'

def lang_form(score):
	if score % 100 >= 10 and score % 100 < 20:
		return 'квантиков'
	else:
		if score % 10 in [2, 3, 4]:
			return 'квантика'
		elif score % 10 == 1:
			return 'квантик'
		else:
			return 'квантиков'



@route('/acc')
def display_pers_acc(db):
	if current_user(db) == None:
		redirect('/')
	try:
		page = request.query['page']
	except KeyError:
		redirect('/acc?page=startPage')
	if page == 'startPage':
		yield from display_pers_acc_start_page(db)
	elif page == 'dataPage':
		yield from display_pers_acc_data_page(db)

def display_pers_acc_start_page(db):
	db.execute('select name, surname, town, school from Kvantland.Student where student=%s', (current_user(db), ))
	(name, surname, town, school, ), = db.fetchall()
	user_info = {
		'name': name,
		'surname': surname,
		'town': town,
		'school': school,
	}

	for field in user_info:
		if user_info[field] == None:
			if field == 'surname':
				user_info[field] = ''
			else:
				user_info[field] = 'Не указано'

	yield '<!DOCTYPE html>'
	yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
	yield '<title> Личный кабинет — Квантландия </title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/accStartPage.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/approv.css">'

	yield from user.display_banner_acc(db)
	yield '<div class="content_wrapper">'
	yield '<div class="acc_form">'
	yield '<div class="header"> Личный кабинет </div>'

	yield '<div class="data_preview">'
	yield '<img class="avatar_img" src="/static/design/icons/userAvatar.png" />'

	yield '<div class="text_data">'
	yield '<div class="name_with_edit">'
	yield f'<div class="name"> {user_info["name"]} {user_info["surname"]} </div>'
	yield '<a href="/acc?page=dataPage">'
	yield '<img class="edit" src="/static/design/icons/edit.svg" />'
	yield '</a>'
	yield '</div>'

	yield f'<div class="city"> {user_info["town"]} </div>'
	yield f'<div class="school"> {user_info["school"]} </div>'
	yield '</div>'
	yield '</div>'

	yield '<hr/>'

	yield '<div class="header"> Ваши результаты </div>'
	tournament_amount = get_tournament_amount(db, config['tournament']['version'], config['tournament']['season'])
	for tournament in range(0, tournament_amount):
		yield f'<div class="tournament_result" num="{tournament_amount - tournament}">'
		yield '<img class="win_cup" src="static/design/icons/win_cup.svg" />'
		yield '<div class="text_content">'
		yield f'<div class="tournament_number"> {to_roman_number(tournament_amount - tournament)} Турнир </div>'
		yield f'<div class="score"> {get_score_text(db, config["tournament"]["version"] - tournament)} </div>'
		yield '</div>'
		yield '</div>'

	yield '<hr/>'

	yield f'<a href="javascript:history.back()"><div class="back_button"> Назад </div></a>'

	yield '</div>'
	yield '</div>'
	yield '</div>'

	yield '<script type="text/javascript" src="/static/design/user.js"></script>'


def display_pers_acc_data_page(db, err={}, user_info=empty_user_info()):
	yield '<!DOCTYPE html>'
	yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
	yield '<title> Личный кабинет — Квантландия </title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/accDataPage.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/approv.css">'

	yield from user.display_banner_acc(db)
	yield '<div class="content_wrapper">'
	yield '<div class="acc_form">'
	yield '<div class="header"> Личный кабинет </div>'
	if not err:
		try:
			if request.query['empty']:
				yield '<div class="empty_field_info">'
				yield '<img src="/static/design/icons/info.svg" />'
				yield '<div class="err"> Все поля в личном кабинете обязательны<br>для заполнения </div>'
				yield '</div>'
		except KeyError:
			pass
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
			if err and name in err.keys():
				yield f' <input name="{name}" type="{type_}" value="" readonly required />'
			else:
				yield f' <input name="{name}" type="{type_}" value="{escape(value_)}" readonly required />'
			yield '<img class="arrow" src="/static/design/icons/down_arrow.svg" />'
			yield '</div>'
		else:
			if err and name in err.keys():
				yield f'<input name="{name}" type="{type_}" value="" required />'
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
	yield f'<a href="javascript:history.back()"><div class="back_button"> Назад </div></a>'
	yield '</div>'
	yield '</div>'

	yield from approv.display_confirm_window()

	yield '<script type="text/javascript" src="/static/design/user.js"></script>'
	yield '<script type="text/javascript" src ="/static/design/accDataPage.js"></script>'


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

	if (new_mail(db, user_info) and check_email(db, user_info['email'])):
		user_info['email'] = ''
		err_dict['email'] = 'Почта уже используется'

	if not err_dict:
		update_user(db, user_info)
		if new_mail(db, user_info):
			yield from send_reg_confirm_message(db, user_info)
		else:
			redirect('/')
	else:
		user_info = update_info(user_info, err_dict)
		yield from display_pers_acc_data_page(db, err_dict, user_info)


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

def check_email(db, email):
	db.execute("select student from Kvantland.Student where email = %s", (email,))
	try:
		(user,) = db.fetchall()
	except ValueError:
		return None
	return user

def show_send_message(info, db, limit_err=False):
	yield '<!DOCTYPE html>'
	yield '<title>Личный кабинет — Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/mail_timer.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/accDataPage.css">'
	yield from user.display_banner_acc(db)
	yield '<div class="content_wrapper">'
	yield '<div class="advert_form">'
	yield '<div class="header"> Подтверждение адреса электронной почты </div>'
	if not limit_err:
		yield '''<div class="description"> 
			Письмо для подтверждения адреса
			электронной почты,</br> 
			привязанной	к Вашему аккаунту, успешно отправлено!</br>
			Для подтверждения адреса, перейдите по ссылке в</br>
			письме, которое придёт Вам на почту</div>'''
	else:
		yield '<div class="limit_info">'
		yield '<img src="/static/design/icons/info.svg" />'
		yield '<div class="err"> Превышен лимит писем за день! </div>'
		yield '</div>'
	yield '<div id="advert">'
	yield '<div class="full_field">'
	yield '<div class="field">'
	yield '<div class="content">'
	yield '<div class="placeholder"> Почта </div>'
	yield f'<div class="input"> {info["email"]} </div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield f'<div class="timer"> Отправить еще раз через: {config["recovery"]["send_again"]}</div>'
	yield '</div>'
	yield '</div>'
	yield f'<input name="name" value={info["name"]} type="hidden"/>'
	yield f'<input name="login" value={info["login"]} type="hidden"/>'
	yield '<script type="text/javascript" src="/static/design/user.js"></script>'
	yield '<script type="text/javascript" src="/static/design/mail_timer.js"></script>'


def check_email_amount(db, info):
	db.execute('select first_mail from Kvantland.Mail where mail = %s', (info['email'], ))
	first_ = db.fetchall()
	if len(first_) > 0:
		(first_email, ), = first_
	else:
		first_email = time.time()
		db.execute('insert into Kvantland.Mail (mail, first_mail) values(%s, %s)', (info['email'], first_email))
	if time.time() - first_email > config['mail_check']['allowed_period']:
		return True
	else:
		db.execute('select remainig_mails from Kvantland.Mail where mail = %s', (info['email'], ))
		(remainig_mails, ), = db.fetchall()
		if remainig_mails > 0:
			return True
	return False

def update_email_amount(db, info):
	db.execute('select first_mail from Kvantland.Mail where mail = %s', (info['email'], ))
	(first_email, ), = db.fetchall()
	if time.time() - first_email < config['mail_check']['allowed_period']:
		db.execute('update Kvantland.Mail set remainig_mails = remainig_mails - 1 where mail = %s', (info['email'], ))
	else:
		db.execute('update Kvantland.Mail set first_mail = %s, remainig_mails = %s where mail = %s', (time.time(), config['mail_check']['allowed_amount'], info['email']))


def send_reg_confirm_message(db, info, only_send = False):
	_email = info['email']
	name = info['name']
	try:
		token = hmac.new(_key.encode('utf-8'), _email.encode('utf-8'), 'sha256').hexdigest()
		info['token'] = token
		link = f'''
		{config['recovery']['acc_confirm_uri']}?{urllib.parse.urlencode(info)}
		'''
		localhost = config['recovery']['localhost']
		host = config['recovery']['host']
		port = config['recovery']['port']
		login = config['recovery']['login']
		password = config['recovery']['password']
		sender = config['recovery']['sender']

		server = smtplib.SMTP_SSL(host, port,  local_hostname=localhost, timeout=120)
		email_content =  f'''
			<!DOCTYPE html>
			<head>
			<link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Montserrat">
   			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    		<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<title>Подтверждение почты</title>
			</head>
			<body style="padding: 80px;
				font-family: Montserrat, Arial !important;
				word-wrap: break-word;
				font-size: 20px;
				font-weight: 500;">
			<div style="font-family: Montserrat, Arial !important;">
			<div style="font-family: Montserrat, Arial !important;"> Здравствуйте, {name}! </div>
			<div style="margin-top: 20px"> 
				Недавно был получен запрос на подтверждение адреса электронной почты, связанной с вашей учетной записью. 
				Если вы запрашивали это подтверждение, нажмите на ссылку ниже: </div>
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
			<div style="font-family: Montserrat, Arial !important;"> Если вам не нужно подтверждать адрес электронной почты, 
			просто проигнорируйте данное сообщение.</div>
			<div style="margin-top: 20px; font-family: Montserrat, Arial !important;"> С уважением, команда Kvantland </div>
			</div>
			</body>
			</html>'''

		msg = EmailMessage()
		msg['Subject'] = 'Подтверждение почты'
		msg['From'] = sender
		msg['To'] = _email
		msg.set_content(email_content, subtype='html')

		server.login(str(login), str(password))
		try:
			if check_email_amount(db, info):
				server.sendmail(sender, [_email], msg.as_string())
				update_email_amount(db, info)
				if not only_send:
					yield from show_send_message(info, db)
			else:
				yield from show_send_message(info, db, limit_err=True)
		except:
			if not only_send:
				info['email'] = ''
				yield from display_pers_acc_data_page(db, {'email':'Адреса не существует'}, info)
		finally:
			server.quit()	
	except ValueError:
		if not only_send:
			info['email'] = ''
			yield from display_pers_acc_data_page(db, {'email':'Неверный адрес электронной почты'}, info)
			return

def update_user(db, info):
	db.execute("update Kvantland.Student set name = %s, surname = %s, school = %s, clas = %s, town = %s where login = %s returning student", (info['name'], info['surname'], info['school'], info['clas'], info['town'], info['login']))
	(user, ), = db.fetchall()
	return int(user)

def update_email(db, info):
	try:
		db.execute("select email from Kvantland.Student where login = %s", (info['login'], ))
		(prev_email, ), = db.fetchall()
	except:
		prev_email = None
	db.execute("update Kvantland.Student set email = %s where login = %s returning student", (info['email'], info['login']))
	(user, ), = db.fetchall()
	if prev_email:
		try:
			db.execute("select email from Kvantland.Previousmail where student = %s", (user, ))
			(mail, ), = db.fetchall()
			db.execute("update Kvantland.Previousmail set email = %s where student = %s", (prev_mail, user))
		except:
			db.execute("insert into Kvantland.Previousmail (student, email) values(%s, %s)", (user, prev_email))
	return int(user)

@route('/acc_confirm')
def check(db):
	user_info = request.query.decode()
	email = user_info['email']
	token = user_info['token']
	if not email or not token:
		redirect('/')
	elif hmac.new(_key.encode('utf-8'), email.encode('utf-8'), 'sha256').hexdigest() != token:
		redirect('/')
	else:
		del user_info['token']
		user = update_email(db, user_info)
		do_login(user, user_info['login'])
		redirect('/')

@route('/acc/send_again', method="POST")
def send_again(db):
	try:
		info = json.loads(request.body.read())
		email = info['email'].strip()
		name = info['name'].strip()
		login = info['name'].strip()
		yield from send_reg_confirm_message(db, {'email': email, 'name': name, 'login': login}, True)
	except KeyError:
		return 
