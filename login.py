#!/usr/bin/python3

from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash

from config import config
import nav

_key = config['keys']['cookie']

@route('/login')
def login_form():
	if current_user() != None:
		do_redirect()
	yield from display_login_form()

def display_login_form(err: str=None):
	yield '<!DOCTYPE html>'
	yield '<title>Вход — Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from nav.display_breadcrumbs(('/', 'Квантландия'))
	yield '<main>'
	yield '<h1>Вход</h1>'
	yield '<form method="post">'
	yield '<div class="classic_form">'
	yield '<label><span class="label">Логин:</span><input name="login" type="text" required /></label>'
	yield '<label><span class="label">Пароль:</span><input name="password" type="password" required /></label>'
	yield '</div>'
	yield '<div class="button_bar">'
	yield '<button type="submit">Войти</button>'
	yield '</div>'
	if err:
		yield f'<p class="error">{err}</p>'
	yield '</form>'
	yield '</main>'
	yield '</div>'

def check_login(db, user_name, password):
	db.execute('select ученик, пароль from Ученик where логин = %s', (user_name, ))
	try:
		(user, password_hash), = db.fetchall()
	except ValueError:
		return None
	if pwhash.verify(password, password_hash):
		return user
	return None

def current_user():
	user = request.get_cookie('user', secret=_key)
	try:
		return int(user)
	except Exception:
		return None

def do_login(user):
	response.set_cookie('user', str(user), max_age=3600, httponly=True, samesite='strict', secret=_key)

def do_logout():
	response.set_cookie('user', '', max_age=0, httponly=True, samesite='strict')

def do_redirect():
	path = request.query.path
	if not path.startswith('/'):
		path = '/'
	redirect(path)

@route('/login', method='POST')
def login_attempt(db):
	if (user := check_login(db, request.forms.login, request.forms.password)) != None:
		do_login(user)
		do_redirect()
	else:
		response.status = 403
		return display_login_form('Неверное имя пользователя или пароль')

@route('/logout')
def logout():
	do_logout()
	do_redirect()
