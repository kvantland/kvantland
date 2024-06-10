#!/usr/bin/python3
from html import escape

from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash
import urllib.parse
import json
import hmac
import jwt
import sys
import time

from config import config
from check_fields_format import *
import user

_key = config['keys']['cookie']

client_id = config['vk']['client_id']
redirect_uri = config['vk']['redirect_uri']
auth_url = config['vk']['auth_url']

params = {'client_id': 	client_id, 'redirect_uri': redirect_uri, 'response_type': 'code'}

@route('/api/login_fields')
def get_login_fields():
	fields = [
		{'type': "input", 'inputType': "text", 'name': "login", 'placeholder': "Логин"},
		{'type': "input", 'inputType': "password", 'name': "password", 'placeholder': "Пароль"}
	]
	return json.dumps(fields)


@route('/api/refresh_tokens', method="POST")
def refresh_tokens():
	print('refresh', file=sys.stderr)
	resp = {
		'access_token': "",
		'refresh_token': "",
	}
	try:
		data = json.loads(request.body.read())
		old_refresh_token = data['refresh_token']
	except:
		return json.dumps(resp)
	print(old_refresh_token, file=sys.stderr)
	
	try:
		user_data = jwt.decode(jwt=old_refresh_token, key=config['keys']['refresh_key'], algorithms=['HS256'])
		login = user_data['login']
		user_id = user_data['user_id']
	except:
		return json.dumps(resp)
	
	resp['refresh_token'] = jwt.encode(payload={'login': login, 'user_id': user_id, 'time': time.time()}, key=config['keys']['refresh_key'], algorithm='HS256')
	resp['access_token'] = jwt.encode(payload={'login': login, 'user_id': user_id, 'time': time.time()}, key=config['keys']['access_key'], algorithm='HS256')

	return json.dumps(resp)


@route('/api/check_login', method="POST")
def check_login_request(db):
	user_data = json.loads(request.body.read())
	resp = {
		'tokens': {
			'access_token': '',
			'refresh_token': '',
		},
		'status': False,
		'errors': dict(),
	}
	try:
		login = user_data['login']
	except:
		login = ''
	
	try:
		password = user_data['password']
	except:
		password = ''
	print(login, password, file=sys.stderr)
	expected_fields = ['login', 'password']
	pw_check = ['password']
	
	try:
		db.execute('select password, student from Kvantland.Student where login = %s', (login, ))
		(password_hash, user_id, ), = db.fetchall()
	except:
		resp['errors']['password'] = 'Неверный логин или пароль'
		password_hash = pwhash.hash('-')

	if pwhash.verify(password, password_hash) and login and user_id:
		access_key = config['keys']['access_key']
		refresh_key = config['keys']['refresh_key']
		resp['tokens']['access_token'] = jwt.encode(payload={'login': login, 'user_id': user_id}, key=access_key, algorithm='HS256')
		resp['tokens']['refresh_token'] = jwt.encode(payload={'login': login, 'user_id': user_id}, key=refresh_key, algorithm='HS256')
	else:
		resp['errors']['password'] = 'Неверный логин или пароль'

	resp['errors'].update(check_fields_format(data=user_data, expected_fields=expected_fields, pw_check=pw_check))
	print(resp['errors'], file=sys.stderr)
	
	if not(resp['errors']):
		resp['status'] = True
	return json.dumps(resp)
	
def check_token(request):
	auth_header = request.get_header('Authorization')
	if auth_header is None:
		return {'error': "Incorrect request format", 'login': ""}
	if 'Bearer' not in auth_header:
		return {'error': "No Bearer in header", 'login': ""}
	token = auth_header.replace('Bearer ', '')
	try:
		payload = jwt.decode(jwt=token, key=config['keys']['access_key'], algorithms=['HS256'])
		print(payload, file=sys.stderr)
	except:
		return {'error': "Not correct token", 'login': ""}
	user_login = payload['login']
	user_id = payload['user_id']
	return {'error': None, 'login': user_login, 'user_id': user_id}


@route('/login')
def login_form(db):
	if current_user(db) != None:
		do_redirect()
	yield from display_login_form()

def display_login_form(err: str=None):
	yield '<!DOCTYPE html>'
	yield '<title>Вход — Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/login.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield from user.display_banner_empty()
	yield '<div class="content_wrapper">'
	yield '<div class="login_form">'
	yield '<div class="header">'
	yield '<a href="/login">'
	yield '<span class="dark"> ВХОД </span>'
	yield '</a>'
	yield '<a href="/reg">'
	yield '<span class="light"> РЕГИСТРАЦИЯ </span>'
	yield '</a>'
	yield '</div>'
	yield '<form method="post" id="login">'
	yield '<div class="full_field">'
	yield '<div class="field">'
	yield '<div class="content">'
	yield '<div class="placeholder"> Логин </div>'
	yield '<input name="login" type="text" required />'
	yield '</div>'
	yield '<div class="info hidden"> <img src="/static/design/icons/info.svg" /> </div>'
	yield '</div>'
	yield '<div class="err hidden"></div>'
	yield '</div>'
	yield '<div class="full_field">'
	yield '<div class="field">'
	yield '<div class="content">'
	yield '<div class="placeholder"> Пароль </div>'
	yield '<input name="password" type="password" required />'
	yield '</div>'
	if err:
		yield '<div class="info"> <img src="/static/design/icons/info.svg" /> </div>'
		yield '</div>'
		yield f'<div class="err"> {err} </div>'
	else:
		yield '<div class="info hidden"> <img src="/static/design/icons/info.svg" /> </div>'
		yield '</div>'
		yield f'<div class="err hidden"></div>'
	yield '</div>'
	yield '</form>'
	yield '<div class="button_area">'
	yield '<button type="submit" class="button" form="login"> Войти </button>'
	yield '<hr class="line" />'
	yield '<a href="' + escape(auth_url + '?' + urllib.parse.urlencode(params)) + '">'
	yield '<div class="vk_button">'
	yield '<span> Войти через </span>'
	yield '<img src="/static/design/icons/vk_button.svg" />'
	yield '</div>'
	yield '</a>'
	yield '</div>'
	yield '<div class="pw_recovery">'
	yield '<a href="/pw_recovery"> Восстановить пароль </a>'
	yield '</div>'
	yield '<script type="text/javascript" src="/static/design/user.js"></script>'
	yield '<script type="text/javascript" src ="/static/design/login.js"></script>'

def check_login(db, user_name, password):
	db.execute('select student, password from Kvantland.Student where login = %s', (user_name, ))
	try:
		(user, password_hash), = db.fetchall()
	except ValueError:
		return None
	if pwhash.verify(password, password_hash):
		return user
	return None

def current_user(db):
	user = request.get_cookie('user', secret=_key)
	login = request.get_cookie('login', secret=_key)
	db.execute('select student from Kvantland.Student where student = %s and login = %s', (user, login, ))
	try:
		(user_check, ), = db.fetchall()
	except ValueError:
		do_logout()
		return None
	return int(user)
		
def do_login(user, login):
	response.set_cookie('user', str(user), path='/', max_age=30 * 24 * 3600, httponly=True, samesite='lax', secret=_key)
	response.set_cookie('login', str(login), path='/', max_age =30 * 24 * 3600, httponly=True, samesite='lax', secret=_key)

def do_logout():
	response.set_cookie('user', '', path='/', max_age=0, httponly=True, samesite='lax')
	response.set_cookie('login', '', path='/', max_age=0, httponly=True, samesite='lax')
	response.set_cookie('email', '', path='/', max_age=0, httponly=True, samesite='lax')

def do_redirect():
	path = request.query.path
	if not path.startswith('/'):
		path = '/'
	redirect(path)

def do_redirect_to_root():
	redirect('/')

@route('/login', method='POST')
def login_attempt(db):
	if (user := check_login(db, request.forms.login, request.forms.password)) != None:
		do_login(user, request.forms.login)
		do_redirect()
	else:
		response.status = 403
		return display_login_form('Неверное имя пользователя или пароль')

@route('/logout')
def logout():
	do_logout()
	do_redirect_to_root()
