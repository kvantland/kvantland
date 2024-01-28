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

all_info = [['name', 'text', 'Имя'],
			['surname', 'text', 'Фамилия'],
			['email', 'email', 'E-mail'],
			['login', 'text', 'Логин'],
			['password', 'password', 'Пароль'],
			['city', 'text', 'Город'],
			['school', 'text', 'Школа'],
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
def reg_from(db):
	if current_user(db) != None:
		redirect('/')
	yield from display_registration_form(empty_user_info())

def display_registration_form(user_info, err=None):
	global type_info, placeholder_info, option_info
	yield '<!DOCTYPE html>'
	yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
	yield '<title> Регистрация — Квантландия </title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/registration.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/nav.css">'
	if err:
		yield '<dialog open="open" class="reg_dialog">'
		yield f'<p> {err} </p>'
		yield '<form method="dialog">'
		yield '<button type="submit" class="dialog_button">Закрыть</button>'
		yield '</form>'
		yield '</dialog>'
	yield '<div class="content_wrapper">'
	yield from nav.display_breadcrumbs(('/', 'Квантландия'))
	yield '<div class="reg_form">'
	yield '<div class="header">'
	yield '<a href="/login">'
	yield '<span class="light"> ВХОД </span>'
	yield '</a>'
	yield '<a href="/reg">'
	yield '<span class="dark"> РЕГИСТРАЦИЯ </span>'
	yield '</a>'
	yield '</div>'
	yield f'<form id="reg" method="post">'
	yield '<div class="fields">'
	for name in placeholder_info:
		yield '<div class="field">'	
		placeholder_ = placeholder_info[name]
		type_ = type_info[name]
		value_ = user_info[name]
		yield f'<div class="placeholder"> {placeholder_} </div>'
		if type_ == 'select':
			yield f'<select name="{name}" required>'
			if not(user_info[name]):
				yield f'<option value="" disabled selected> </option>'
			opt_list = option_info[name]
			for opt in opt_list:
				if user_info[name] != str(opt):
					yield f'<option> {opt} </option>'
				else:
					yield f'<option selected> {opt} </option>'
		else:
			yield f'<input name="{name}" type="{type_}" value="{escape(value_)}" required />'
		yield '</div>'
	yield '</select>'
	yield '</div>'
	yield '</div>'
	yield '<div class="check_cont">'
	yield '<input class="checkbox" type="checkbox" name="approval" id="approval" required />'
	yield '''<label for="approval"> Я принимаю условия Политики конфиденциальности и даю согласие
		на обработку своих персональных данных'''
	yield '</label>'
	yield '</div>'
	yield '<div class="g-recaptcha-outer">'
	yield '<div class="g-recaptcha-inner">'
	yield f'<div class="g-recaptcha" data-sitekey="{sitekey}"></div>'
	yield '</div>'
	yield '</div>'
	yield '<hr size="1">'
	yield f'<button type="submit" class="reg_button" form="reg"> Зарегистрироваться </button>'
	yield '</form>'
	yield '</div>'
	yield '<script type="text/javascript" src ="/static/registration.js"></script>'
	yield '<script src="https://www.google.com/recaptcha/api.js" async defer></script>'

def add_user(db, info):
	db.execute("insert into Kvantland.Student (login, password, name, surname, school, clas, town, email) values (%s, %s, %s, %s, %s, %s, %s, %s) returning student", (info['login'], pwhash.hash(info['password']), info['name'], info['surname'], info['school'], info['clas'], info['city'], info['email']))
	(user, ), = db.fetchall()
	db.execute("insert into Kvantland.AvailableProblem (student, variant) select distinct on (problem) %s, variant from Kvantland.Variant order by problem, random();", (user, ))
	return int(user)

def check_login(db, login):
	db.execute("select student from Kvantland.Student where login = %s", (login,))
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
					return "Логин должен состоять из английских букв, цифр и символов - и _ <br /> Ваш login содержит недопустимые символы", field
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
				return "Пароль должен содержать заглавные и строчные буквы, а также цифры", field

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
			approval = request.forms['approval']
			if approval:
				if check_login(db, user_info['login']):
					user_info['login'] = ''
					yield from display_registration_form(user_info, 'К сожалению, пользователь с таким loginом уже существует, <br /> попробуйте другой login')
				else:
					mes, param_to_change = check_format(user_info)
					if not mes:
						user = add_user(db, user_info)
						do_login(user, user_info['login'])
						redirect('/')
					else:
						user_info[param_to_change] = ''
						yield from display_registration_form(user_info, mes)
			else:
				yield from display_registration_form(user_info, 'Нет согласия на обработку персональных данных')
		else:
			yield from display_registration_form(user_info, 'Ошибка заполнения капчи')
	else:
		yield from display_registration_form(user_info,'Заполните капчу!')