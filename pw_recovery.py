#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bottle import route, request
from passlib.hash import pbkdf2_sha256 as pwhash
from check_fields_format import *
import json
import sys
from send_mail import send_mail
import time
import jwt

from login import do_login
from config import config

alph_lower = 'abcdefghijklmnopqrstuvwxyz'
alph_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = '0123456789'


@route('/api/pw_recovery', method="POST")
def pw_recovery(db):
	resp = {
		'status': False,
		'errors': {},
	}
	try:
		user_info = json.loads(request.body.read())
		print('user info: ', user_info, file=sys.stderr)
	except:
		return json.dumps(resp)
	
	if not('email' in user_info.keys()):
		resp['errors']['email'] = 'Не указана почта'
		return json.dumps(resp)
	
	email_check = ['email']
	resp.update(check_fields_format(user_info, email_check=email_check))

	user_add_info = user_exists(db, user_info['email'])
	print('user add info: ', user_add_info, file=sys.stderr)
	if not(user_add_info['status']):
		resp['errors']['email'] = 'Неверный адрес почты'
	else:
		user_info['name'] = user_add_info['name']
		user_info['login'] = user_add_info['login']
		
	if not(resp['errors']):
		if check_email_amount(db, user_info['email']):
			send_status = send_pw_recovery_message(user_info, request.get_header('Origin'))
			if send_status['status']:
				update_email_amount(db, user_info['email'])
			else:
				resp['errors']['email'] = send_status['error']	
		else:
			resp['errors']['email'] = "Превышен лимит писем за день!"
	
	if not(resp['errors']):
		resp['status'] = True
	print('errors: ', resp['errors'], file=sys.stderr)

	return json.dumps(resp)


def user_exists(db, email):
	resp = {
		'login': None,
		'name': None,
		'status': False,
	}
	db.execute('select login, name from Kvantland.Student where email=%s', (email, ))
	if len(arr := db.fetchall()):
		(login, name, ), = arr
		resp['login'] = login
		resp['name'] = name
		resp['status'] = True
	else:
		db.execute('select login, name from Kvantland.Previousmail join Kvantland.Student using (student) where Kvantland.Previousmail.email=%s', (email, ))
		if len(arr := db.fetchall()):
			(login, name, ), = arr
			resp['login'] = login
			resp['name'] = name
			resp['status'] = True
	return resp
	
	
def send_pw_recovery_message(user_info, origin):
	user_info['time'] = time.time()
	token = jwt.encode(payload=user_info,  key=config['keys']['email_confirm'], algorithm='HS256')
	link = f"{origin}/login/pwRecovery?email_confirm_token={token}&request=pw_recovery"
	
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
				<div style="font-family: Montserrat, Arial !important;"> Здравствуйте, {user_info['name']}! </div>
				<div style="margin-top: 20px"> Недавно был получен запрос на изменение пароля вашей учетной записи. 
				Если вы запрашивали это изменение пароля, нажмите на ссылку ниже для установки нового пароля: </div>
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
				Нажмите здесь, чтобы изменить пароль
				</div>
				</a>
				</div>
				<div>
				<div style="font-family: Montserrat, Arial !important;"> Если вам не нужно менять пароль, просто проигнорируйте данное сообщение. </div>
				<div style="margin-top: 20px; font-family: Montserrat, Arial !important;"> С уважением, команда Kvantland </div>
				</div>
				</body>
				</html>'''
	
	return send_mail(email_content=email_content, email=user_info['email'], subject="Восстановление пароля")


@route('/api/pw_update', method="POST")
def pw_update(db):
	resp = {
		'status': False,
		'errors': dict(),
		'user_info': dict(),
	}

	try:
		data = json.loads(request.body.read())
		token = data['token']
		fields = data['fields']
	except:
		return json.dumps(resp)

	if not('token' in data.keys()):
		return json.dumps(resp)

	try:
		decoded_token = jwt.decode(jwt=token, key=config['keys']['email_confirm'], algorithms=['HS256'])
		login = decoded_token['login']
		email = decoded_token['email']
	except:
		return json.dumps(resp)
	
	if not('password' in fields.keys()):
		fields['password'] = ''
	if not('password_repeat' in fields.keys()):
		fields['password_repeat'] = ''
	
	expected_fields = ['password', 'password_repeat']
	pw_check = ['password', 'password_repeat']
	resp['errors'].update(check_fields_format(fields, 
										   expected_fields=expected_fields, 
										   pw_check=pw_check))
	
	print('fields: ', fields, file=sys.stderr)
	if fields['password'] != fields['password_repeat'] and not(resp['errors']):
		resp['errors']['password_repeat'] = 'Пароли не совпадают'
	
	if not(resp['errors']):
		update_user(db, email, fields['password'])
		resp['status'] = True
		resp['user_info'] = {'login': login, 'password': fields['password']}
	
	print('resp: ',  resp, file=sys.stderr)
	return json.dumps(resp)


def check_email_amount(db, email):
	db.execute('select first_mail from Kvantland.Mail where mail = %s', (email, ))
	first_ = db.fetchall()
	if len(first_) > 0:
		(first_email, ), = first_
	else:
		first_email = time.time()
		db.execute('insert into Kvantland.Mail (mail, first_mail) values(%s, %s)', (email, first_email))
	if time.time() - first_email > config['mail_check']['allowed_period']:
		return True
	else:
		db.execute('select remainig_mails from Kvantland.Mail where mail = %s', (email, ))
		(remainig_mails, ), = db.fetchall()
		if remainig_mails > 0:
			return True
	return False

def update_email_amount(db, email):
	db.execute('select first_mail from Kvantland.Mail where mail = %s', (email, ))
	(first_email, ), = db.fetchall()
	if time.time() - first_email < config['mail_check']['allowed_period']:
		db.execute('update Kvantland.Mail set remainig_mails = remainig_mails - 1 where mail = %s', (email, ))
	else:
		db.execute('update Kvantland.Mail set first_mail = %s, remainig_mails = %s where mail = %s', (time.time(), config['mail_check']['allowed_amount'], email))


def update_user(db, email, password):
	try: 
		db.execute('select student from Kvantland.Student where email = %s', (email, ))
		(user, ) = db.fetchall()[0]
	except IndexError:
		db.execute('select student from Kvantland.Previousmail where email = %s', (email, ))
		(user, ) = db.fetchall()[0]
	db.execute('update Kvantland.Student set password=%s where student = %s returning student, login', (pwhash.hash(password), user, ))
	(user, login, ) = db.fetchall()[0]
	do_login(user, login)
