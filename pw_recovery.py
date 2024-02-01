#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bottle import route, redirect, request, response
from passlib.hash import pbkdf2_sha256 as pwhash
import json
import hmac
import urllib.parse
import sys
import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from html import escape

from login import do_login, current_user
from config import config
import nav

alph_lower = 'abcdefghijklmnopqrstuvwxyz'
alph_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = '0123456789'

_key = config['keys']['recovery']



@route('/pw_recovery')
def display_recovery_form(err=None):
	yield '<!DOCTYPE html>'
	yield '<title>Восстановление пароля</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	if err:
		yield '<dialog open="open" class="reg_dialog">'
		yield f'<p> {err} </p>'
		yield '<form method="dialog">'
		yield '<button type="submit" class="dialog_button">Закрыть</button>'
		yield '</form>'
		yield '</dialog>'
	yield from nav.display_breadcrumbs(('/', 'Квантландия'), ('/login', 'Войти'))
	yield '<main>'
	yield '<div class="recovery_form">'
	yield '<div class="login_form_header"> Восстановление пароля </div>'
	yield '<form method="post" class="recovery">'
	yield '<div class="form_desc">'
	yield '<p> Введите адрес электронной почты, привязанной к вашему аккаунту </p>'
	yield '</div>'
	yield '<input name="email" type="email" placeholder="Почта..." class="form_field" required />'
	yield '<button type="submit" class="submit_button"> ОТПРАВИТЬ </button>'
	yield '</form>'
	yield '</div>'
	yield '</div>'
	yield '</main>'
	yield '<script type="text/javascript" src ="/static/dialog.js"></script>'

def show_send_message():
	yield '<!DOCTYPE html>'
	yield '<title>Восстановление пароля</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield from nav.display_breadcrumbs(('/', 'Квантландия'), ('/login', 'Войти'))
	yield '<div> Письмо с восстановлением пароля отправлено на ваш адрес! </div>'

@route('/pw_recovery', method="POST")
def recovery_attempt(db):
	_email = request.forms.email
	if not _email:
		return display_recovery_form(err="Не указан адрес электронной почты")
	try:
		yield from show_send_message()
		db.execute('select student, name from Kvantland.Student where email=%s', (_email, ))
		(user, name, ) = db.fetchall()[0]

		check_user = current_user(db)
		if check_user:
			redirect('/')
		else:
			token = hmac.new(_key.encode('utf-8'), _email.encode('utf-8'), 'sha256').hexdigest()
			link = f'''
			{config['recovery']['redirect_uri']}?token={token}&mail={_email} 
			'''
			host = config['recovery']['host']
			port = config['recovery']['port']
			login = config['recovery']['login']
			password = config['recovery']['password']
			sender = config['recovery']['sender']

			server = smtplib.SMTP(f'{host}')
			email_content =  f'''
				<!DOCTYPE html>
				<title>Восстановление пароля</title>
				<div style="margin: 100px 50px 0 50px">
				<p> Здравствуйте, {name}! </p>
				<p> Недавно был получен запрос на изменение пароля вашей учетной записи. 
				Если вы запрашивали это изменение пароля, нажмите на ссылку ниже для установки нового пароля: </p>
				<a href="{link}"> 
				<div style="text-align:center; color:white; background-color:blue; display:block; padding:3px 10px 3px 10px;
				width:500px; margin: 50px auto 60px auto"> <p> Нажмите здесь, чтобы изменить пароль </p> </div>
				</a>
				<p> Если вам не нужно менять пароль, просто проигнорируйте данное сообщение. </p>
				<p> С уважением, команда Kvantland </p>
				</div>
				</html>'''

			msg = MIMEMultipart()
			msg['Subject'] = 'Password recovery'
			msg['From'] = sender
			msg['To'] = _email
			msg.attach(MIMEText(email_content, 'html'))

			server.starttls()
			server.login(str(login), str(password))
			try:
				server.sendmail(sender, [_email], msg.as_string())
			except:
				redirect('/')
			finally:
				server.quit()	
	except ValueError:
		return display_recovery_form(err="Неверный адрес электронной почты")

@route('/pw_recovery/new_password')
def display_new_password_form(err=None):
	email = request.query['mail']
	token = request.query['token']
	if not email or not token:
		redirect('/')
	if hmac.new(_key.encode('utf-8'), email.encode('utf-8'), 'sha256').hexdigest() != token:
		redirect('/')
	response.set_cookie('email', str(email), path='/', httponly=True, samesite='lax', secret=_key)
	yield '<!DOCTYPE html>'
	yield '<title>Восстановление пароля</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	if err:
		yield '<dialog open="open" class="reg_dialog">'
		yield f'<p> {err} </p>'
		yield '<form method="dialog">'
		yield '<button type="submit" class="dialog_button">Закрыть</button>'
		yield '</form>'
		yield '</dialog>'
	yield from nav.display_breadcrumbs(('/', 'Квантландия'), ('/login', 'Войти'))
	yield '<main>'
	yield '<div class="recovery_form">'
	yield '<div class="login_form_header"> Восстановление пароля </div>'
	yield f'<form method="post" class="recovery">'
	yield '<div class="form_desc">'
	yield '<p> Придумайте новый пароль </p>'
	yield '</div>'
	yield '<input name="password" type="password" placeholder="Пароль..." class="form_field" required />'
	yield '<input name="password_confirm" type="password" placeholder="Повторите пароль..." class="form_field" required />'
	yield '<button type="submit" class="submit_button"> ОТПРАВИТЬ </button>'
	yield '</form>'
	yield '</div>'
	yield '</div>'
	yield '</main>'
	yield '<script type="text/javascript" src ="/static/dialog.js"></script>'


@route('/pw_recovery/new_password', method="POST")
def new_password_attempt(db):
	email = request.get_cookie('email', secret=_key)
	password = request.forms.password
	password_confirm = request.forms.password_confirm
	if (not password or not password_confirm):
		return display_new_password_form(err="Заполните форму!")
	if password != password_confirm:
		return display_new_password_form(err="Пароли не совпадают")

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
		return display_new_password_form(err="Пароль должен содержать заглавные и строчные буквы, а также цифры")

	if len(password) < min_size:
		return display_new_password_form(err=f"Слишком мало символов в поле Пароль, <br /> должно быть минимум  {min_size}")
	if len(password) > max_size:
		return display_new_password_form(err=f"Слишком много символов в поле Пароль")

	update_user(db, email, password)
	redirect('/')


def update_user(db, email, password):
	db.execute('update Kvantland.Student set password=%s where email=%s returning student, login', (pwhash.hash(password), email, ))
	(user, login, ) = db.fetchall()[0]
	do_login(user, login)
