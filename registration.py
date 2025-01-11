#!/usr/bin/python3

from bottle import route, request
from passlib.hash import pbkdf2_sha256 as pwhash
import json
from send_mail import send_mail
from config import config
import time
import jwt
from check_fields_format import *

import sys


@route('/api/registration_fields')
def get_registration_fields():
	fields = [
		    {'type': "input", 'inputType': "text", 'name':"name", 'placeholder':"Имя"},
			{'type': "input", 'inputType': "text", 'name': "surname", 'placeholder': "Фамилия"},
			{'type': "input", 'inputType': "text", 'name': "email", 'placeholder': "E-mail"},
			{'type': "input", 'inputType': "text", 'name': "login", 'placeholder': "Логин"},
			{'type': "input", 'inputType': "password", 'name': "password", 'placeholder': "Пароль"},
			{'type': "input", 'inputType': "text", 'name': "town", 'placeholder': "Город"},
			{'type': "input", 'inputType': "text", 'name': "school", 'placeholder': "Школа"},
			{'type': "select", 'options': [str(i) for i in range(1, 12)] + ['Другое'], 'name': "clas", 'placeholder': "Класс"},
		]
	return json.dumps(fields)


@route('/api/checkout_reg', method="POST")
def checkout_reg(db, required_captcha=True):
	resp = {
		'status': False,
		'errors': {},
    }
	
	email_check = ['email']
	pw_check = []
	select_check = dict()
	expected_fields = ['approval']
	
	for field in json.loads(get_registration_fields()):
		expected_fields.append(field['name'])
		if field['type'] == 'select':
			select_check[field['name']] = field['options']
		if field['type'] == 'input':
			if field['inputType'] == 'password':
				pw_check.append(field['name'])

	try:
		data = json.loads(request.body.read())
		user_info = data['user']
	except:
		return json.dumps(resp)
		
	print(user_info, file=sys.stderr)
	resp['errors'] = check_fields_format(user_info, expected_fields, pw_check, 
									email_check, select_check)
	
	if required_captcha:
		try:
			captcha_token = data['captcha']
			if check_captcha(captcha_token):
				resp['errors']['captcha'] = check_captcha(captcha_token)		
		except:
			resp['errors']['captcha'] = "Заполните капчу!"
		
	if 'login' in user_info.keys():
		if login_already_exists(db, user_info['login']):
			resp['errors']['login'] = "Логин уже используется"
			
	if 'email' in user_info.keys():
		if email_already_exists(db, user_info['email']):
			resp['errors']['email'] = "Почта уже используется"
			
	if not resp['errors']:
		if check_email_amount(db, user_info):
			resp['status'] = True
			send_status = send_registration_confirm_message(user_info, request.get_header('Origin'))
			print('send status: ', send_status)
			if send_status['status']:
				update_email_amount(db, user_info)
			else:
				resp['errors']['email'] = send_status['error']	
		else:
			resp['errors']['email'] = "Превышен лимит писем за день!"
	print('fields check status: ', resp, file=sys.stderr)
	return json.dumps(resp)


@route('/api/send_reg_message_again', method="POST")
def send_again(db):
	return checkout_reg(db, required_captcha=False)

def send_registration_confirm_message(user_info, origin):
	user_info['time'] = time.time()
	token = jwt.encode(payload=user_info,  key=config['keys']['email_confirm'], algorithm='HS256')
	link = f"{origin}?email_confirm_token={token}&request=registration"
	
	email_content = f'''
        <!DOCTYPE html>
        <head>
        <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Montserrat">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Регистрация</title>
        </head>
        <body style="padding: 80px;
            font-family: Montserrat, Arial !important;
            word-wrap: break-word;
            font-size: 20px;
            font-weight: 500;">
        <div style="font-family: Montserrat, Arial !important;">
        <div style="font-family: Montserrat, Arial !important;"> Здравствуйте, {user_info['name']}! </div>
        <div style="margin-top: 20px"> Спасибо за регистрацию в <a href="{config['server']['host']}:{config['server']['port']}">Квантландии</a>. 
        Для подтверждения регистрации нажмите на кнопку ниже: </div>
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
        <div style="margin-top: 20px; font-family: Montserrat, Arial !important;"> 
            Данные для входа:<br/><br/>
            <span style="font-weight:700">Логин:</span> {user_info['login']}<br/>
            <span style="font-weight:700">Пароль:</span> {user_info['password']}<br/><br/>
            С уважением, команда Kvantland </div>
        </body>
        </html>'''

	return send_mail(email_content=email_content, email=user_info['email'], subject="Подтверждение регистрации")

@route('/api/registration', method="POST")
def registration(db):
	resp = {
        'login': "",
        'password': "",
		'user_id': "",
    }
	token = json.loads(request.body.read())['email_confirm_token']
	user_info = jwt.decode(jwt=token, key=config['keys']['email_confirm'], algorithms=['HS256'])
	user_id = add_new_user(db, user_info)
	resp['login'] = user_info['login']
	resp['password'] = user_info['password']
	print('resp: ', resp, file=sys.stderr)
	return json.dumps(resp)
		
def add_new_user(db, info):
	try:
		db.execute("select student from Kvantland.Student where login = %s", (info['login'], ))
		(user, ), = db.fetchall()
	except:
		db.execute("insert into Kvantland.Student (login, password, name, surname, school, clas, town, email) values (%s, %s, %s, %s, %s, %s, %s, %s) returning student", 
			(info['login'], pwhash.hash(info['password']), info['name'], info['surname'], info['school'], info['clas'], info['town'], info['email']))
		(user, ), = db.fetchall()
		db.execute("""
						insert into Kvantland.AvailableProblem (student, variant)
						select distinct on (problem, classes)
						%s, variant
						from Kvantland.Student, Kvantland.Variant 
							join Kvantland.Problem using (problem) 
							join Kvantland.CurrentTournament using (tournament)
						order by problem, classes, random();""", (user, ))
		db.execute("insert into Kvantland.Score (student, tournament) values (%s, %s)", (user, config["tournament"]["version"]))
	return int(user)


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
