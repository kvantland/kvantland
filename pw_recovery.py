#!/usr/bin/python3

from bottle import route, redirect, request, response
from passlib.hash import pbkdf2_sha256 as pwhash
import json
import hmac
import urllib.parse
import sys

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
	yield '<main>'
	yield '<div style="text-align:center">'
	yield '<p> На вашу почту отправлено письмо с подтверждением! </p>'
	yield '</div>'
	yield '</main>'

@route('/pw_recovery', method="POST")
def recovery_attempt(db):
	email = request.forms.email
	if not email:
		return display_recovery_form(err="Не указан адрес электронной почты")
	try:
		db.execute('select student from Kvantland.Student where email=%s', (email, ))
		(user, ), = db.fetchall()

		check_user = current_user(db)
		if check_user:
			redirect('/')
		else:
			params = {
			'email': email,
			'redirect_uri': config['recovery']['redirect_uri'],
			'token': hmac.new(_key.encode('utf-8'), email.encode('utf-8'), 'sha256') 
			}
			send_recovery_request(params)
			return show_send_message()
	except ValueError:
		return display_recovery_form(err="Неверный адрес электронной почты")


def send_recovery_request(params):
	pass

@route('/pw_recovery/response', method="POST")
def get_response():
	params = request.query
	redirect(f'/pw_recovery/new_password?{escape(urllib.parse.urlencode(params))}')


@route('/pw_recovery/new_password')
def display_new_password_form(err=None):
	email = request.query['email']
	if not email:
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

	mp_upper, tmp_lower, tmp_number = (0, 0, 0)
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
	(user, login), = db.fetchall()
	do_login(user, login)
