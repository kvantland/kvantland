#!/usr/bin/python3
from html import escape
import sys

from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash
from pathlib import Path
import urllib.parse

from config import config
import nav
import json
import urllib.request as urllib2
import http.cookiejar as cookielib

_key = config['keys']['cookie']
ROOT = Path(__file__).parent

client_id = 51749604
redirect_uri = 'http://localhost:8080/login/vk'
client_secret = 'oGUIYzsB2dsk7hwp6GBI'
auth_url = 'http://oauth.vk.com/authorize'
token_url = 'https://oauth.vk.com/access_token'

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
	yield '<h1>Вход</h1>'
	yield '<form method="post" class="login">'
	yield '<label><span class="label"></span><input name="login" type="text" placeholder="Логин..." class=form_field required /></label>'
	yield '<label><span class="label"></span><input name="password" type="password" placeholder="Пароль..." class=form_field required /></label>'
	yield '<div class="button_bar">'
	yield '<button type="submit"> Войти </button>'
	yield '<div class="vk auth" id="Vk">'
	yield f'<a class="login" href="' + escape(auth_url + '?' + urllib.parse.urlencode(params)) + '"></a>'
	yield '</div>' 
	yield '</div>'
	yield '</form>'
	yield '<div class="auth_type" id="auth_type"><div>'
	yield '</div>'
	yield '</main>'
	yield '<script type="text/javascript" src = "/static/master.js"></script>'
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
	if user_name.startswith('vk#'):
		return user
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
	response.set_cookie('user', str(user), secret=_key)
	print('here', user, file=sys.stderr)


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