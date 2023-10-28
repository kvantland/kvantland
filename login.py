#!/usr/bin/python3
from html import escape

from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash
import urllib.parse

from config import config
import nav

_key = config['keys']['cookie']

client_id = config['vk']['client_id']
redirect_uri = config['vk']['redirect_uri']
auth_url = config['vk']['auth_url']

params = {'client_id': 	client_id, 'redirect_uri': redirect_uri, 'response_type': 'code'}

@route('/login')
def login_form():
	if current_user() != None:
		do_redirect()
	yield from display_login_form()

def display_login_form(err: str=None):
  yield '<!DOCTYPE html>'
  yield '<title>Вход — Квантландия</title>'
  yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
  yield from nav.display_breadcrumbs(('/', 'Квантландия'))
  yield '<main>'
  yield '<div class="login_form">'
  yield '<div class="login_form_header">Вход</div>'
  yield '<form method="post" class="login">'
  yield '<input name="login" type="text" placeholder="Логин..." class=form_field required />'
  yield '<input name="password" type="password" placeholder="Пароль..." class=form_field required />'
  yield '<button type="submit" class="submit_button"> ВОЙТИ </button>'
  yield '</form>'
  yield '<div class="auth_button_bar">'
  yield '<div class = button_bar_text> ВОЙТИ ЧЕРЕЗ: </div>'
  yield '<div class="vk button_bar_item">'
  yield f'<a class="button_bar_item" href="' + escape(auth_url + '?' + urllib.parse.urlencode(params)) + '"></a>'
  yield '</div>' 
  yield '</div>'
  yield '<div class="anon_reg">'
  yield f'<a href="/reg"> Зарегистрироваться </a>'
  yield '</div>'
  yield '</div>'
  yield '</main>'
  yield '<script type="text/javascript" src = "/static/master.js"></script>'
  if err:
    yield f'<p class="error">{err}</p>'

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
	response.set_cookie('user', str(user), path='/', httponly=True, samesite='lax', secret=_key)

def do_logout():
	response.set_cookie('user', '', path='/', max_age=0, httponly=True, samesite='lax')

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
		do_login(user)
		do_redirect()
	else:
		response.status = 403
		return display_login_form('Неверное имя пользователя или пароль')

@route('/logout')
def logout():
	do_logout()
	do_redirect_to_root()
