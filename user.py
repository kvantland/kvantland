#!/usr/bin/python3
from html import escape
from urllib.parse import quote
from bottle import route, request, response, redirect

from login import current_user

def display_banner(db):
	path_arg = escape(quote('?'.join(request.urlparts[2:4]), safe=''))
	user = current_user(db)
	yield '<nav class="user_nav">'

	yield '<a href="/">'
	yield '<div class="logo_area">'
	yield '<img class="logo" src="/static/design/icons/logo.svg" />'
	yield '<div class="logo_name"> КВАНТ<br/>ЛАНДИЯ </div>'
	yield '</div>'
	yield '</a>'

	if user == None:
		yield '<div class="menu">'
		yield '<div class="menu_item" id="info">О турнире</div>'
		yield '<div class="menu_item" id="team">О команде</div>'
		yield '<div class="menu_item" id="examples">Примеры задач</div>'
		yield '<div class="menu_item" id="contacts">Наши контакты</div>'
		yield '</div>'

		yield '<div class="button_area">'
		yield '<a href="/login">'
		yield '<div class="login_button"> Войти </div>'
		yield '</a>'
		yield '<div class="lang_button">'
		yield '<div> RU </div>'
		yield '<img id="lang_change" src="/static/design/icons/down_arrow.svg" /> '
		yield '</div>'

	yield '</nav>'

	'''
	if user != None:
		db.execute('select coalesce(name, login), score from Kvantland.Student where student = %s', (user,))
		(login, money), = db.fetchall()
		yield f'<li>{escape(login)}'
		yield f'<li>Счёт: {money}'
	yield f'<li><a href="/rules">Правила</a>'
	if user != None:
		yield f'<li><a class="login" href="/logout?path={path_arg}">Выйти</a>'
		yield f'<li><div class="acc_icon"> <a class="acc_href" href="/acc"></a> </div>'
	else:
		yield f'<li><a class="login" href="/login?path={path_arg}">Войти</a>'
	yield '</ul>'
	yield '</nav>'
	'''
