#!/usr/bin/python3

from html import escape
from urllib.parse import quote
from bottle import route, request, response, redirect

from login import current_user

def display_banner(db):
	path_arg = escape(quote('?'.join(request.urlparts[2:4]), safe=''))
	user = current_user()
	yield '<nav class="user_nav">'
	yield '<ul>'
	yield f'<li><a href="/">На главную</a>'
	if user != None:
		yield f'<li><a class="login" href="/logout?path={path_arg}">Выйти</a>'
	else:
		yield f'<li><a class="login" href="/login?path={path_arg}">Войти</a>'
	yield '</ul>'
	yield '</nav>'
