#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bottle import route, redirect, request, response
from passlib.hash import pbkdf2_sha256 as pwhash
import json
import hmac
import urllib.parse
import sys
import email.message
from pathlib import Path
from email.message import EmailMessage
import smtplib
from html import escape

from login import do_login, current_user
from config import config
import user

alph_lower = 'abcdefghijklmnopqrstuvwxyz'
alph_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = '0123456789'

_key = config['keys']['recovery']


@route('/pw_recovery')
def display_recovery_form(err=None):
	yield '<!DOCTYPE html>'
	yield '<title>Восстановление пароля</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/pw_recovery.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield from user.display_banner_empty()
	yield '<div class="content_wrapper">'
	yield '<div class="email_req_form">'
	yield '<div class="header"> Восстановление пароля </div>'
	yield '<div class="description"> Введите адрес электронной почты,</br> привязанной к Вашему аккаунту </div>'
	yield '<form method="post" id="email_req">'
	yield '<div class="full_field">'
	yield '<div class="field">'
	yield '<div class="content">'
	yield '<div class="placeholder"> Почта </div>'
	yield '<input name="email" type="email" required />'
	yield '</div>'
	if err and 'email' in err.keys():
		yield '<div class="info"> <img src="/static/design/icons/info.svg" /> </div>'
		yield '</div>'
		yield f'<div class="err"> {err["email"]} </div>'
	else:
		yield '<div class="info hidden"> <img src="/static/design/icons/info.svg" /> </div>'
		yield '</div>'
		yield f'<div class="err hidden"></div>'
	yield '</div>'
	yield '</form>'
	yield '<button type="submit" form="email_req"> Отправить </button>'
	yield '<div class="login">'
	yield '<a href="/login"> Авторизироваться </a>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '<script type="text/javascript" src="/static/design/user.js"></script>'
	yield '<script type="text/javascript" src ="/static/design/pw_recovery.js"></script>'

def show_send_message(email):
	yield '<!DOCTYPE html>'
	yield '<title>Восстановление пароля</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/pw_recovery.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/mail_timer.css">'
	yield from user.display_banner_empty()
	yield '<div class="content_wrapper">'
	yield '<div class="advert_form">'
	yield '<div class="header"> Восстановление пароля </div>'
	yield '''<div class="description"> Письмо для восстановления пароля</br>успешно отправлено на Ваш адрес!</br>
		Для смены пароля перейдите по ссылке</br>
		в письме, которое придёт Вам на почту</div>'''
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
	yield '<div class="timer"> Отправить еще раз через: 10</div>'
	yield '</div>'
	yield '</div>'
	yield '<script type="text/javascript" src="/static/design/user.js"></script>'
	yield '<script type="text/javascript" src="/static/design/mail_timer.js"></script>'

@route('/pw_recovery', method="POST")
def recovery_attempt(db):
	_email = request.forms.email
	if not _email:
		yield from display_recovery_form(err={"email":"Не указан адрес электронной почты"})
		return
	try:
		db.execute('select student, name from Kvantland.Student where email=%s', (_email, ))
		(user, name, ), = db.fetchall()
		yield from show_send_message(_email)
		check_user = current_user(db)
		if check_user:
			redirect('/')
		else:
			token = hmac.new(_key.encode('utf-8'), _email.encode('utf-8'), 'sha256').hexdigest()
			params = {'token': token, 'mail': _email}
			link = f'''
			{config['recovery']['redirect_uri']}?{urllib.parse.urlencode(params)}
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

			msg = EmailMessage()
			msg['Subject'] = 'Восстановление пароля'
			msg['From'] = sender
			msg['To'] = _email
			msg.set_content(email_content, subtype='html')

			server.login(str(login), str(password))
			try:
				server.sendmail(sender, [_email], msg.as_string())
			except:
				yield from display_recovery_form(err={'email':'Адреса не существует'})
			finally:
				server.quit()	
	except ValueError:
		yield from display_recovery_form(err={'email':'Неверный адрес электронной почты'})
		return

@route('/pw_recovery/new_password')
def display_new_password_form(err=None):
	user_info = request.query.decode()
	email = user_info['mail']
	token = user_info['token']
	if not email or not token:
		redirect('/')
	if hmac.new(_key.encode('utf-8'), email.encode('utf-8'), 'sha256').hexdigest() != token:
		redirect('/')
	response.set_cookie('email', str(email), path='/', httponly=True, samesite='lax', secret=_key)
	yield '<!DOCTYPE html>'
	yield '<title>Восстановление пароля</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/pw_recovery.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield from user.display_banner_empty()
	yield '<div class="content_wrapper">'
	yield '<div class="new_pw_form">'
	yield '<div class="header"> Восстановление пароля </div>'
	yield '<div class="description"> Придумайте новый пароль </div>'
	yield '<form method="post" id="new_pw">'
	yield '<div class="full_field">'
	yield '<div class="field">'
	yield '<div class="content">'
	yield '<div class="placeholder"> Пароль </div>'
	yield '<input name="password" type="password" required />'
	yield '</div>'
	yield '<div class="info hidden"> <img src="/static/design/icons/info.svg" /> </div>'
	yield '</div>'
	yield f'<div class="err hidden"></div>'
	yield '</div>'
	yield '<div class="full_field">'
	yield '<div class="field">'
	yield '<div class="content">'
	yield '<div class="placeholder"> Повторите пароль </div>'
	yield '<input name="password_confirm" type="password" required />'
	yield '</div>'
	if err and 'password' in err.keys():
		yield '<div class="info"> <img src="/static/design/icons/info.svg" /> </div>'
		yield '</div>'
		yield f'<div class="err"> {err["password"]} </div>'
	else:
		yield '<div class="info hidden"> <img src="/static/design/icons/info.svg" /> </div>'
		yield '</div>'
		yield f'<div class="err hidden"></div>'
	yield '</div>'
	yield '</form>'
	yield '<button type="submit" form="new_pw"> Отправить </button>'
	yield '</div>'
	yield '</div>'
	yield '<script type="text/javascript" src="/static/design/user.js"></script>'
	yield '<script type="text/javascript" src ="/static/design/pw_recovery.js"></script>'


@route('/pw_recovery/new_password', method="POST")
def new_password_attempt(db):
	email = request.get_cookie('email', secret=_key)
	password = request.forms.password
	password_confirm = request.forms.password_confirm
	if (not password or not password_confirm):
		return display_new_password_form(err={"password": "Заполните форму!"})
	if password != password_confirm:
		return display_new_password_form(err={"password": "Пароли не совпадают"})

	min_size = config['reg']['min_password_size']
	max_size = config['reg']['max_password_size']

	tmp_upper, tmp_lower, tmp_number = (0, 0, 0)
	for s in password:
		if s in alph_upper:
			tmp_upper = 1
		if s in alph_lower:
			tmp_lower = 1
		if s in num:
			tmp_number = 1
	if not(tmp_lower and tmp_upper and tmp_number):
		return display_new_password_form(err={"password": "Пароль должен содержать заглавные <br /> и строчные буквы, а также цифры"})

	if len(password) < min_size:
		return display_new_password_form(err={"password": f"Слишком мало символов, <br /> должно быть минимум  {min_size}"})
	if len(password) > max_size:
		return display_new_password_form(err={"password": f"Слишком много символов"})

	update_user(db, email, password)
	redirect('/')


def update_user(db, email, password):
	db.execute('update Kvantland.Student set password=%s where email=%s returning student, login', (pwhash.hash(password), email, ))
	(user, login, ) = db.fetchall()[0]
	do_login(user, login)
