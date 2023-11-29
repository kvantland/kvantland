from login import do_login, current_user
from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash
import nav
import json
from html import escape
from config import config
import urllib.request as urllib2
import urllib.parse

import sys

secret = config['reg']['secret']
reg_url = config['reg']['reg_url']
sitekey = config['reg']['sitekey']
alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph_lower = 'abcdefghijklmnopqrstuvwxyz'
alph_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = '0123456789'

all_info = [['login', 'text', 'Логин'],
			['password', 'password', 'Пароль'],
			['email', 'email', 'Почта'],
			['name', 'text', 'Имя'],
			['surname', 'text', 'Фамилия'],
			['patronymic', 'text', 'Отчество'],
			['school', 'text', 'Школа'],
			['city', 'text', 'Город'],
			['clas', 'select', 'Класс', [str(i) for i in range(1, 12)] + ['Другое']]]


field_amount = len(all_info) # количество полей в форме без учета капчи и кнопки
button_size = 70 # размер кнопки
field_size = 40 # размер поля
pad = 4 # расстояние между полями
captcha_size = 78 # размер каптчи
button_margin = 20 # расстояние до кнопки
form_size = button_size + field_amount * field_size + pad * field_amount + captcha_size  + button_margin # размер формы

# типы полей
type_info = dict()

# Отображаемые названия полей
placeholder_info = dict()

# Опции для полей с выбором
option_info = dict()

# Заполнение словарей
for field in all_info:
	field_name = field[0]
	type_name = field[1]
	placeholder_name = field[2]
	type_info[field_name] = type_name
	placeholder_info[field_name] = placeholder_name
	if type_name == 'select':
		options = field[3]
		option_info[field_name] = options

@route('/reg')
def reg_from():
	if current_user() != None:
		redirect('/')
	yield from display_registration_form(empty_user_info())

def display_registration_form(user_info, err=None):
	global type_info, placeholder_info, option_info
	yield '<!DOCTYPE html>'
	yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
	yield '<title> Регистрация — Квантландия </title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	if err:
		yield '<dialog open="open" class="reg_dialog">'
		yield f'<p> {err} </p>'
		yield '<form method="dialog">'
		yield '<button type="submit" class="dialog_button">Закрыть</button>'
		yield '</form>'
		yield '</dialog>'
	yield '<main>'
	yield from nav.display_breadcrumbs(('/', 'Квантландия'))
	yield '<div class="reg_form">'
	yield '<div class = "reg_form_header"> Регистрация </div>'
	yield f'<form class="reg" style="height: {form_size}px" method="post">'
	for name in placeholder_info:
		placeholder_ = placeholder_info[name]
		type_ = type_info[name]
		value_ = user_info[name]
		if type_ == 'select':
			yield f'<select style="height: {field_size}px" name="{name}" required>'
			if not(user_info[name]):
				yield f'<option value="" disabled selected> {placeholder_} </option>'
			opt_list = option_info[name]
			for opt in opt_list:
				if user_info[name] != str(opt):
					yield f'<option> {opt} </option>'
				else:
					yield f'<option selected> {opt} </option>'
		else:
			yield f'<input style="height: {field_size}px" name="{name}" type="{type_}" placeholder="{placeholder_}" value="{escape(value_)}" required />'
	yield '</select>'	
	yield f'<div class="g-recaptcha" data-sitekey="{sitekey}"></div>'
	yield f'<button type="submit" class="reg_button" style="height: {button_size}px; margin-top: {button_margin}px"> Зарегистрироваться </button>'
	yield '</form>'
	yield '<div class="back_to_log">'
	yield '<a href="/login"> Уже зарегистрированы? </a>'
	yield '</div>'
	yield '</div>'
	yield '</main>'
	yield '<script type="text/javascript" src ="/static/registration.js"></script>'
	yield '<script src="https://www.google.com/recaptcha/api.js" async defer></script>'

def add_user(db, info):
	db.execute("insert into Ученик (логин, пароль, имя, фамилия, отчество, школа, класс, город, почта) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning ученик", (info['login'], pwhash.hash(info['password']), info['name'], info['surname'], info['patronymic'], info['school'], info['clas'], info['city'], info['email']))
	(user, ), = db.fetchall()
	db.execute("insert into ДоступнаяЗадача (ученик, вариант) select distinct on (задача) %s, вариант from Вариант order by задача, random();", (user, ))
	return int(user)

def check_login(db, логин):
	db.execute("select ученик from Ученик where логин = %s", (логин,))
	try:
		(user,) = db.fetchall()
	except ValueError:
		return None
	return user

def empty_user_info():
	user_info = dict()
	for field in all_info:
		field_name = field[0]
		user_info[field_name] = ''
	return user_info

def check_format(user_info):
	
	for field in user_info:
		min_size = config['reg']['min_' + field + '_size']
		max_size = config['reg']['max_' + field + '_size']
		name = placeholder_info[field]

		if type_info[field] == "select":
			if not(user_info[field] in option_info[field]):
				return "Недопустимое значение в поле " + name + "<br /> Пожалуйста, выберите значение из выпадающего списка", field

		if field == "login":
			tmp_alph = 0
			for s in user_info[field]:
				if s != '_' and s != '-' and s not in alph and s not in num:
					return "Логин должен состоять из английских букв, цифр и символов - и _ <br /> Ваш логин содержит недопустимые символы", field
				if s in alph:
					tmp_alph = 1
			if not tmp_alph:
				return "Логин должен содержать буквы", field


		if type_info[field] == "password":
			tmp_upper, tmp_lower, tmp_number = (0, 0, 0)
			for s in user_info[field]	:
				if s in alph_upper:
					tmp_upper = 1
				if s in alph_lower:
					tmp_lower = 1
				if s in num:
					tmp_number = 1
			if not(tmp_lower and tmp_upper and tmp_number):
				return "Пароль должен содержать заглавные и строчные буквы, а так же цифры", field

		if len(user_info[field]) < min_size:
			return "Слишком мало символов в поле " + name + ", <br /> должно быть минимум " + str(min_size),  field
		if len(user_info[field]) > max_size:
			return "Слишком много символов в поле " + name, field

	return False, ''

@route('/reg', method='POST')
def login_attempt(db):

	user_info = dict()

	for field in all_info:
		name = field[0]
		new_value = request.forms.get(name).encode('l1').decode().strip()
		user_info[name] = new_value

	if len(request.forms['g-recaptcha-response']) != 0:
		params = {
		"secret": secret,
		"response": request.forms['g-recaptcha-response']
		}
		out = reg_url + '?' + urllib.parse.urlencode(params)
		cont = urllib2.urlopen(out)
		not_robot = json.loads(cont.read())['success']

		if not_robot:
			if check_login(db, user_info['login']):
				user_info['login'] = ''
				yield from display_registration_form(user_info, 'К сожалению, пользователь с таким логином уже существует, <br /> попробуйте другой логин')
			else:
				mes, param_to_change = check_format(user_info)
				if not mes:
					user = add_user(db, user_info)
					do_login(user)
					redirect('/')
				else:
					user_info[param_to_change] = ''
					yield from display_registration_form(user_info, mes)
		else:
			yield from display_registration_form(user_info, 'Ошибка заполнения капчи')
	else:
		yield from display_registration_form(user_info,'Заполните капчу!')