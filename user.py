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
	yield f'<li><a href="/rules">Правила</a>'
	if user != None:
		db.execute('select логин, счёт from Ученик where ученик = %s', (user,))
		(login, money), = db.fetchall()
		yield f'<li>{escape(login)}'
		yield f'<li>Счёт: {money}'
		yield f'<li><a class="login" href="/logout?path={path_arg}">Выйти</a>'
	else:
		yield f'<li><a class="login" href="/login?path={path_arg}">Войти</a>'
	yield '</ul>'
	yield '</nav>'
