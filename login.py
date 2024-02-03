#!/usr/bin/python3
from html import escape

from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash
import urllib.parse

from config import config
import user

_key = config['keys']['cookie']

client_id = config['vk']['client_id']
redirect_uri = config['vk']['redirect_uri']
auth_url = config['vk']['auth_url']

params = {'client_id': 	client_id, 'redirect_uri': redirect_uri, 'response_type': 'code'}

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
	response.set_cookie('user', str(user), path='/', httponly=True, samesite='lax', secret=_key)
	response.set_cookie('login', str(login), path='/', httponly=True, samesite='lax', secret=_key)

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
