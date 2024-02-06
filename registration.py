from login import do_login, current_user
from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash
import user
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

def lang_form(num):
	r = num % 10
	if num > 10 and num < 20:
		return 'символов'
	elif r in [5, 6, 7, 8, 9, 0]:
		return 'символов'
	elif r in [1]:
		return 'символ'
	else:
		return 'символа'

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
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'

	yield from user.display_banner_empty()
	yield '<div class="content_wrapper">'
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
		yield '<div class="full_field">'
		yield '<div class="field">'
		yield '<div class="content">'	
		placeholder_ = placeholder_info[name]
		type_ = type_info[name]
		value_ = user_info[name]
		yield f'<div class="placeholder"> {placeholder_} </div>'
		if type_ == 'select':
			yield f'<div class="select_line" name="{name}">'
			yield f' <input name="{name}" type="{type_}" value="{escape(value_)}" required />'
			yield '<img class="arrow" src="/static/design/icons/down_arrow.svg" />'
			yield '</div>'
		else:
			yield f'<input name="{name}" type="{type_}" value="{escape(value_)}" required />'
		yield '</div>'
		if err and name in err.keys():
			yield '<div class="info"> <img src="/static/design/icons/info.svg" /> </div>'
			yield '</div>'
			yield f'<div class="err"> {err[name]} </div>'
		else:
			yield '<div class="info hidden"> <img src="/static/design/icons/info.svg" /> </div>'
			yield '</div>'
			yield f'<div class="err hidden"></div>'
		if type_ == 'select':
			yield f'<div class="select_box hidden" name="{name}">'
			opt_list = option_info[name]
			for opt in opt_list:
				if user_info[name] != str(opt):
					yield f'<div class="option"> {opt} </div>'
				else:
					yield f'<div class="option selected"> {opt} </div>'
			yield '</div>'
		yield '</div>'
	yield '</div>'
	yield '<div class="full_field">'
	yield '<div class="check_cont">'
	yield '<input class="checkbox" type="checkbox" name="approval" id="approval" required />'
	yield '''<label for="approval"> Я принимаю условия <a href="/policy"> Политики конфиденциальности</a> и даю <span class="underline"> согласие
		на обработку своих персональных данных</span>'''
	yield '</label>'
	yield '</div>'
	if err and 'approval' in err.keys():
		yield f'<div class="err"> {err["approval"]} </div>'
	else:
		yield f'<div class="err hidden"></div>'
	yield '</div>'
	yield '<div class="full_field">'
	yield '<div class="g-recaptcha-outer">'
	yield '<div class="g-recaptcha-inner">'
	yield f'<div class="g-recaptcha" data-sitekey="{sitekey}"></div>'
	yield '</div>'
	yield '</div>'
	if err and 'captcha' in err.keys():
		yield f'<div class="err"> {err["captcha"]} </div>'
	else:
		yield f'<div class="err hidden"></div>'
	yield '</div>'
	yield '<hr size="1">'
	yield f'<button type="submit" class="reg_button" form="reg"> Зарегистрироваться </button>'
	yield '</form>'
	yield '</div>'
	yield '<script type="text/javascript" src ="/static/dialog.js"></script>'
	yield '<script type="text/javascript" src ="/static/design/registration.js"></script>'
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
	err_dict = {}
	
	for field in user_info:
		min_size = config['reg']['min_' + field + '_size']
		max_size = config['reg']['max_' + field + '_size']
		name = placeholder_info[field]

		if type_info[field] == "select":
			if not(user_info[field] in option_info[field]):
				err_dict[field] = "Значение не из списка"

		if field == "login":
			tmp_alph = 0
			for s in user_info[field]:
				if s != '_' and s != '-' and s not in alph and s not in num:
					err_dict[field] = "Логин должен состоять из английских букв, </br> цифр и символов - и _"
				if s in alph:
					tmp_alph = 1
			if not tmp_alph:
				err_dict[field] = "Логин должен содержать буквы"


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
				err_dict[field] = "Пароль должен содержать заглавные и </br> строчные буквы, а также цифры"

		if len(user_info[field]) < min_size:
			err_dict[field] = "Минимум " + str(min_size) + ' ' + lang_form(min_size)
		if len(user_info[field]) > max_size:
			err_dict[field] = "Слишком много символов"

	return err_dict

@route('/reg', method='POST')
def login_attempt(db):

	user_info = dict()

	for field in all_info:
		name = field[0]
		new_value = request.forms.get(name).encode('l1').decode().strip()
		user_info[name] = new_value

	not_robot = False
	captcha = 0
	if len(request.forms['g-recaptcha-response']) != 0:
		params = {
		"secret": secret,
		"response": request.forms['g-recaptcha-response']
		}
		out = reg_url + '?' + urllib.parse.urlencode(params)
		cont = urllib2.urlopen(out)
		not_robot = json.loads(cont.read())['success']
	else:
		captcha = 1

	err_dict = check_format(user_info)

	if not not_robot:
		err_dict['captcha'] = 'Ошибка заполнения капчи'

	if captcha:
		err_dict['captcha'] = 'Заполните капчу!'

	approval = request.forms['approval']
	if not approval:
		err_dict['approval'] = 'Поставьте галочку'

	if check_login(db, user_info['login']):
		user_info['login'] = ''
		err_dict['login'] = 'Логин уже используется'

	if len(err_dict) == 0:
		user = add_user(db, user_info)
		do_login(user, user_info['login'])
		redirect('/')
	else: 
		for field in err_dict:
			if field in user_info.keys():
				user_info[field] = ''
		yield from display_registration_form(user_info, err_dict)