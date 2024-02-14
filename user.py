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


	yield '<div class="menu">'
	yield '<div class="menu_item" id="info"><div>О турнире</div></div>'
	yield '<div class="menu_item" id="team"><div>О нас</div></div>'
	yield '<div class="menu_item" id="examples"><div>Примеры задач</div></div>'
	yield '<div class="menu_item" id="contacts"><div>Наши контакты</div></div>'
	yield '</div>'

	if user == None:
		yield '<div class="button_area">'
		yield '<a href="/login">'
		yield '<div class="login_button"> Войти </div>'
		yield '</a>'
		'''
		yield '<div class="lang_button">'
		yield '<div> RU </div>'
		yield '<img id="lang_change" src="/static/design/icons/down_arrow.svg" />'
		yield '</div>'
		'''
		yield '</div>'
	else:
		yield '<div class="button_area">'
		yield '<a href="/acc">'
		yield '<div class="acc_cont">'
		yield '<img class="acc_button" src="/static/design/icons/acc.svg" />'
		yield '</div>'
		yield '</a>'
		yield '<div class="logout_button"> Выйти </div>'
		'''
		yield '<div class="lang_button">'
		yield '<div> RU </div>'
		yield '<img id="lang_change" src="/static/design/icons/down_arrow.svg" />'
		yield '</div>'
		'''
		yield '</div>'

	yield '</nav>'

	yield '<div class="dialog out">'
	yield '''<div class="content"> Вы уверены, что хотите выйти? <br/><br/> 
			Все ваши ответы будут сохранены, вы<br/>сможете вернуться к решению задач<br/>позже </div>'''
	yield '<div class="button_area">'
	yield '<div class="button cancel"> Отмена </div>'
	yield f'<a href="/logout?path={path_arg}">'
	yield '<div class="button out"> Выйти </div>'
	yield '</a>'
	yield '</div>'
	yield '</div>'
	yield '</div>'

def display_banner_tournament(db):
	path_arg = escape(quote('?'.join(request.urlparts[2:4]), safe=''))
	user = current_user(db)
	db.execute('select coalesce(name, login), score from Kvantland.Student where student = %s', (user,))
	(login, money), = db.fetchall()
	yield '<nav class="user_nav">'

	yield '<a href="/">'
	yield '<div class="logo_area">'
	yield '<img class="logo" src="/static/design/icons/logo.svg" />'
	yield '<div class="logo_name"> КВАНТ<br/>ЛАНДИЯ </div>'
	yield '</div>'
	yield '</a>'

	if user != None:
		yield '<div class="user_area">'
		yield f'<div> {login} </div>'
		yield f'<div> Счёт: {money} </div>'
		yield '</div>'

		yield '<div class="button_area">'
		yield '<a href="/acc">'
		yield '<div class="acc_cont">'
		yield '<img class="acc_button" src="/static/design/icons/acc.svg" />'
		yield '</div>'
		yield '</a>'
		yield '<a href="/rules">'
		yield '<div class="rules_button"> Правила </div>'
		yield '</a>'
		yield '<div class="logout_button"> Выйти </div>'
		'''
		yield '<div class="lang_button">'
		yield '<div> RU </div>'
		yield '<img id="lang_change" src="/static/design/icons/down_arrow.svg" />'
		yield '</div>'
		'''
		yield '</div>'

	yield '</nav>'

	yield '<div class="dialog out">'
	yield '''<div class="content"> Вы уверены, что хотите выйти? <br/><br/> 
			Все ваши ответы будут сохранены, вы<br/>сможете вернуться к решению задач<br/>позже </div>'''
	yield '<div class="button_area">'
	yield '<div class="button cancel"> Отмена </div>'
	yield f'<a href="/logout?path={path_arg}">'
	yield '<div class="button out"> Выйти </div>'
	yield '</a>'
	yield '</div>'
	yield '</div>'
	yield '</div>'

def display_banner_empty():
	yield '<nav class="user_nav">'

	yield '<a href="/">'
	yield '<div class="logo_area">'
	yield '<img class="logo" src="/static/design/icons/logo.svg" />'
	yield '<div class="logo_name"> КВАНТ<br/>ЛАНДИЯ </div>'
	yield '</div>'
	yield '</a>'

	yield '<div class="button_area">'
	'''
	yield '<div class="lang_button">'
	yield '<div> RU </div>'
	yield '<img id="lang_change" src="/static/design/icons/down_arrow.svg" />'
	yield '</div>'
	'''
	yield '</div>'

	yield '</nav>'

def display_banner_acc(db):
	path_arg = escape(quote('?'.join(request.urlparts[2:4]), safe=''))
	user = current_user(db)
	db.execute('select coalesce(name, login), score from Kvantland.Student where student = %s', (user,))
	(login, money), = db.fetchall()
	yield '<nav class="user_nav">'

	yield '<a href="/">'
	yield '<div class="logo_area">'
	yield '<img class="logo" src="/static/design/icons/logo.svg" />'
	yield '<div class="logo_name"> КВАНТ<br/>ЛАНДИЯ </div>'
	yield '</div>'
	yield '</a>'

	if user != None:
		yield '<div class="user_area centred">'
		yield f'<div> {login} </div>'
		yield f'<div> Счёт: {money} </div>'
		yield '</div>'

		yield '<div class="button_area">'
		yield f'<a href="/logout?path={path_arg}">'
		yield '<div class="logout_button"> Выйти </div>'
		yield '</a>'
		''''
		yield '<div class="lang_button">'
		yield '<div> RU </div>'
		yield '<img id="lang_change" src="/static/design/icons/down_arrow.svg" />'
		yield '</div>'
		'''
		yield '</div>'

	yield '</nav>'

	yield '<div class="dialog out">'
	yield '''<div class="content"> Вы уверены, что хотите выйти? <br/><br/> 
			Все ваши ответы будут сохранены, вы<br/>сможете вернуться к решению задач<br/>позже </div>'''
	yield '<div class="button_area">'
	yield '<div class="button cancel"> Отмена </div>'
	yield f'<a href="/logout?path={path_arg}">'
	yield '<div class="button out"> Выйти </div>'
	yield '</a>'
	yield '</div>'
	yield '</div>'
	yield '</div>'

