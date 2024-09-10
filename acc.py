#!/usr/bin/python3
from copy import deepcopy
from bottle import route, request, response
import sys
from login import check_token
from registration import add_new_user
from check_fields_format import *
from send_mail import send_mail
from config import config
import time
import math
import jwt
import json

@route('/api/user', method="OPTIONS")
def resp():
	response.iter_headers(
		('Allow', 'GET'),
		('Access-Control-Allow-Origin', config['client']['url']),
		('Access-Control-Allow-Methods', ['GET', 'OPTIONS']),
	)
	response.status = 200
	
@route('/api/user')
def get_user_info(db):	
	print('user info requested', file=sys.stderr)
	token_check_status = check_token(request)
	print(token_check_status, file=sys.stderr)
	if token_check_status['error']:
		response.status = 400
		return json.dumps({'error': token_check_status['error']})
	else:
		user = token_check_status['login']
	print(user, file=sys.stderr)
		
	resp = {
		'user': {
			'login': '',
			'name': '',
			'email': '',
			'surname': '',
			'school': '',
			'clas': '',
			'town': '',
			'score': '',
		}
	}
	if user:
		try:
			db.execute('select name, email, surname, school, clas, town, score from Kvantland.Student where login = %s', (user, ))
		except:
			response.status = 400
			return json.dumps({'error': "No such user!"})
		(name, email, surname, school, clas, town, score), = db.fetchall()
		resp['user']['name'] = name
		resp['user']['email'] = email
		resp['user']['surname'] = surname
		resp['user']['school'] = school
		resp['user']['clas'] = clas
		resp['user']['town'] = town
		resp['user']['score'] = score
		resp['user']['login'] = user
	return json.dumps(resp) 


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

@route('/api/acc_form_request', method="POST")
def acc_form_request(db):
	resp = {
		'status': False,
		'email_changed': False,
		'errors': dict(),
	}
	try:
		data = json.loads(request.body.read().decode('utf-8'))
		update_info = data['user_info']
		request_type = data['action_type']
	except:
		return json.dumps(resp)
	print(update_info, request_type, sep='\n')
	
	if request_type in ['updateInfo']:
		check_token_status = check_token(request)
		if check_token_status['error']:
			resp['errors']['token'] = check_token_status['error']
			return json.dumps(resp)
		else:
			login = check_token_status['login']
	
	email_check = ['email']
	expected_fields = ['approval']
	select_check = dict()
	
	for field in json.loads(get_acc_fields()):
		expected_fields.append(field['name'])
		if field['type'] == 'select':
			select_check[field['name']] = field['options']

	resp['errors'].update(check_fields_format(update_info, 
										   email_check=email_check,
										   expected_fields=expected_fields,
										   select_check=select_check))
	
	if request_type in ['updateInfo']:
		update_status = update_user_info(db, update_info=update_info,  field_errors=resp['errors'], login=login)
		resp['errors'].update(update_status['errors']) # добавляем ошибки, возникшие при запросах к дб на обновление информации о пользователе

	elif request_type in ['oauthReg']:
		try:
			login = update_info['login']	
			update_info['password'] = 'vk_password'
		except:
			return json.dumps(resp)
	
	if 'email' in update_info.keys() and not(resp['errors']):
		if is_new_email(db, update_info['email'], login) or request_type in ['send_again', 'oauthReg']:
			if not email_already_exists(db, update_info['email']):
				origin = request.get_header('Origin')
				send_status = send_acc_confirm_message(login=login, user_info=update_info, request_type=request_type, origin=origin)
				if send_status['status']:
					resp['email_changed'] = True
				else:
					resp['errors']['email'] = send_status['error']
			else:
				resp['errors']['email'] = "Почта уже используется"
	
	if not(resp['errors']):
		resp['status'] = True
	print('resp: ', resp, file=sys.stderr)
		
	return json.dumps(resp)


def update_user_info(db, update_info={}, field_errors={}, login=''):
	resp = {
		'status': False,
		'errors': {},
	}
	try:
		db.execute('select name, surname, school, clas, town from Kvantland.Student where login=%s', (login, )) # предыдущие значения
		(prev_name, prev_surname, prev_school, prev_clas, prev_town, ), = db.fetchall()
	except:
		resp['errors']['db'] = 'User not exists'
		return resp
	
	prev_info = {
		'name': prev_name,
		'surname': prev_surname,
		'school': prev_school, 
		'clas': prev_clas,
		'town': prev_town,
	}
	
	print('prev info: ', prev_info, file=sys.stderr)
	for field in update_info: # поля с ошибками остаются прежними
		if field in field_errors:
			if field_errors[field]:
				update_info[field] = prev_info[field]
	try:
		db.execute('update Kvantland.Student set name=%s, surname=%s, school=%s, clas=%s, town=%s where login=%s', 
			(update_info['name'], update_info['surname'], update_info['school'], update_info['clas'], update_info['town'], 
				login))
	except:
		resp['errors']['db'] = "Can't update user info"
	return resp


def send_acc_confirm_message(login="", user_info={}, request_type="", origin=""):
	add_info = {'login': login, 'send_time': time.time(), 'request_type': request_type}
	link_params = deepcopy(user_info)
	link_params.update(add_info)
	print(link_params)
	token = jwt.encode(payload=link_params, key=config['keys']['email_confirm'], algorithm='HS256')
	link = f"{origin}?email_confirm_token={token}&request=update_acc"
	
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
		<div style="font-family: Montserrat, Arial !important;"> Здравствуйте, {user_info['name']}! </div>
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
	
	return send_mail(email_content=email_content, email=user_info['email'], subject="Подтверждение почты")


@route('/api/check_email_amount', method="POST")
def check_user_email_amount(db):
	check_token_status = check_token(request)
	if check_token_status['error']:
		return json.dumps({'error': check_token_status['error']})
		
	email = json.loads(request.body.read())['email']
	
	db.execute('select first_mail from Kvantland.Mail where mail = %s', (email, ))
	first_ = db.fetchall()
	if len(first_) > 0:
		(first_email, ), = first_
	else:
		first_email = time.time()
		db.execute('insert into Kvantland.Mail (mail, first_mail) values(%s, %s)', (email, first_email))
	if time.time() - first_email > config['mail_check']['allowed_period']:
		update_user_email_amount(db, email)
		return json.dumps({'status': True})
	else:
		db.execute('select remainig_mails from Kvantland.Mail where mail = %s', (email, ))
		(remainig_mails, ), = db.fetchall()
		if remainig_mails > 0:
			update_user_email_amount(db, email)
			return json.dumps({'status': True})
	return json.dumps({'status': False, 'error': "Not enough time passed"})


def update_user_email_amount(db, email):
	db.execute('select first_mail from Kvantland.Mail where mail = %s', (email, ))
	(first_email, ), = db.fetchall()
	if time.time() - first_email < config['mail_check']['allowed_period']:
		db.execute('update Kvantland.Mail set remainig_mails = remainig_mails - 1 where mail = %s', (email, ))
	else:
		db.execute('update Kvantland.Mail set first_mail = %s, remainig_mails = %s where mail = %s', (time.time(), config['mail_check']['allowed_amount'], email))

@route('/api/email_update', method="POST")
def email_update(db):
	resp = {
		'status': False,
		'tokens': {'access_token': "", 'refresh_token': ""}
	}
	request_data = json.loads(request.body.read())
	decoded_data = jwt.decode(jwt=request_data['email_confirm_token'], key=config['keys']['email_confirm'], algorithms=['HS256'])
	if not('request_type' in decoded_data.keys()):
		return json.dumps(resp)
	else:
		request_type = decoded_data['request_type']
	
	if request_type == 'updateInfo':
		db.execute('update Kvantland.Student set email=%s where login=%s', (decoded_data['email'], decoded_data['login']))
	elif request_type == 'oauthReg':
		try:
			user_id = add_new_user(db, decoded_data)
			login = decoded_data['login']
			access_key = config['keys']['access_key']
			refresh_key = config['keys']['refresh_key']
			resp['tokens']['access_token'] = jwt.encode(payload={'login': login, 'user_id': user_id}, key=access_key, algorithm='HS256')
			resp['tokens']['refresh_token'] = jwt.encode(payload={'login': login, 'user_id': user_id}, key=refresh_key, algorithm='HS256')
		except:
			return json.dumps(resp)
	
	resp['status'] = True
	return json.dumps(resp)


@route('/api/is_user_info_full', method="POST")
def is_user_info_full(db):
	resp = {
		'status': False
	}

	token_status = check_token(request)
	print(token_status, file=sys.stderr)
	if token_status['error']:
		return json.dumps(resp)
	login = token_status['login']
	print(login, file=sys.stderr)

	db.execute('select name, surname, town, clas, email from Kvantland.Student where login=%s', (login,))
	(name, surname, town, clas, email, ), = db.fetchall()
	if name and surname and town and clas and email:
		resp['status'] = True

	return json.dumps(resp)

		
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
	token_check_status = check_token(request)
	print(token_check_status, file=sys.stderr)
	if token_check_status['error']:
		response.status = 400
		return "Ошибка авторизации!"
	else:
		user = token_check_status['user_id']
	if tournament == config['tournament']['version']:
		return "Идёт сейчас"
	db.execute('select score from Kvantland.Score where student=%s and tournament=%s', (user, tournament, ))
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