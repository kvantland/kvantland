from login import do_login, current_user
from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash
import nav
import json
from config import config
import urllib.request as urllib2
import urllib.parse

import sys

secret = config['reg']['secret']
reg_url = config['reg']['reg_url']
alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
alph_lower = 'abcdefghijklmnopqrstuvwxyz'
alph_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = '0123456789'

min_log_size = config['reg']['min_log_size']
max_log_size = config['reg']['max_log_size']
min_password_size = config['reg']['min_password_size']
max_password_size = config['reg']['max_password_size']
max_school_size = config['reg']['max_school_size']
max_name_size = config['reg']['max_name_size']
max_surname_size = config['reg']['max_surname_size']
min_school_size = config['reg']['min_school_size']

field_amount = 6 # количество полей в форме без учета капчи и кнопки
button_size = 70 # размер кнопки
field_size = 40 # размер поля
pad = 4 # расстояние между полями
form_size = button_size + field_amount * field_size + pad * (field_size - 1) # размер формы

# отображаемая в форме пользовательсткая информация
user_info = {
	'login': '',
	'password': '',
	'name': '',
	'surname': '',
	'school': '',
	'clas': ''
} 

# типы полей
type_info = {
	'login': 'text',
	'password': 'password',
	'name': 'text',
	'surname': 'text',
	'school': 'text'
}

# Отображаемые названия полей
placeholder_info = {
	'login': 'Логин',
	'password': 'Пароль',
	'name': 'Имя',
	'surname': 'Фамилия',
	'school': 'Школа'
}

@route('/reg')
def reg_from():
	if current_user() != None:
		redirect('/')
	yield from display_registration_form()

def display_registration_form(err=None):
	global user_info, type_info, placeholder_info
	global field_size
	yield '<!DOCTYPE html>'
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
	for i in placeholder_info:
		placeholder_ = placeholder_info[i]
		type_ = type_info[i]
		value_ = user_info[i]
		yield f'<input style="height: {field_size}px" name="{i}" type="{type_}" placeholder="{placeholder_}" value="{value_}" required />'
	yield f'<select style="height: {field_size}px" name="clas" required>'
	if not(user_info['clas']):
		yield '<option value="" disabled selected> Класс </option>'
	clas_opt = [str(i) for i in range(1, 12)] + ['Другое']
	for i in clas_opt:
		if user_info["clas"] != str(i):
			yield f'<option> {i} </option>'
		else:
			yield f'<option selected> {i} </option>'
	yield '</select>'
	yield '<div class="g-recaptcha" data-sitekey="6LcWR2MoAAAAABz4UpMRZlmwmWZlvne32dKbc1Kx"></div>'
	yield f'<button type="submit" class="reg_button" style="height: {button_size}px"> Зарегистрироваться </button>'
	yield '</form>'
	yield '<div class="back_to_log">'
	yield '<a href="/login"> Уже зарегистрированы? </a>'
	yield '</div>'
	yield '</div>'
	yield '</main>'
	yield '<script type="text/javascript" src ="/static/registration.js"></script>'
	yield '<script src="https://www.google.com/recaptcha/api.js" async defer></script>'

def add_user(db, логин, пароль, имя, фамилия, школа, класс):
	db.execute("insert into Ученик (логин, пароль, имя, фамилия, школа, класс) values (%s, %s, %s, %s, %s, %s) returning ученик", (логин, pwhash.hash(пароль), имя, фамилия, школа, класс))
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

def check_format(login, password, name, surname, school, clas):
	if len(login) > max_log_size:
		return "Слишком длинный логин", 'login'
	for s in login:
		if s != '_' and s != '-' and s not in alph:
			return "Логин должен состоять из английских букв и символов - и _ <br /> Ваш логин содержит недопустимые символы", 'login'
	if len(login) < min_log_size:
		return "Количество символов в логине должно составлять минимум " + str(min_log_size), 'login'
	if len(password) > max_password_size:
		return "Слишком длинный пароль", 'password'
	if len(password) < min_password_size:
		return "Количество символов в пароле должно составлять минимум " + str(min_password_size), 'password'
	tmp_upper = 0
	tmp_lower = 0
	tmp_number = 0
	for s in password:
		if s in alph_upper:
			tmp_upper = 1
		if s in alph_lower:
			tmp_lower = 1
		if s in num:
			tmp_number = 1
	if not(tmp_lower and tmp_upper and tmp_number):
		return "Пароль должен содержать заглавные и строчные буквы, а так же цифры", 'password'
	if len(name) > max_name_size:
		return "Слишком длинное имя", 'name'
	if len(surname) > max_surname_size:
		return "Слишком длинная фамилия", 'surname'
	if len(school) > max_school_size:
		return "Слишком длинное название школы", 'school'
	if len(school) < min_school_size:
		return "Слишком короткое название школы", 'school'
	if not(clas in [str(i) for i in range(1, 12)]) and clas != "Другое":
		return "Класса с таким номером не существует", 'clas'
	return False, ''

def update_info(param):
	global user_info
	user_info[param] = ''

@route('/reg', method='POST')
def login_attempt(db):
	global user_info

	login = request.forms.login.strip()
	password = request.forms.password.strip()
	name = request.forms.name.strip()
	surname = request.forms.surname.strip()
	clas = request.forms.clas.strip()
	school = request.forms.school.strip()

	user_info = {
	"login": login,
	"password": password,
	"name": name,
	"surname": surname,
	"school": school,
	"clas": clas
	}

	if len(request.forms['g-recaptcha-response']) != 0:
		params = {
		"secret": secret,
		"response": request.forms['g-recaptcha-response']
		}
		out = reg_url + '?' + urllib.parse.urlencode(params)
		cont = urllib2.urlopen(out)
		not_robot = json.loads(cont.read())['success']

		if not_robot:
			if check_login(db, request.forms.login):
				update_info('login')
				yield from display_registration_form('К сожалению, пользователь с таким логином уже существует, <br /> попробуйте другой логин')
			else:
				mes, param_to_change = check_format(login, password, name, surname, school, clas)
				if not mes:
					user = add_user(db, login, password, name, surname, school, clas)
					do_login(user)
					redirect('/')
				else:
					update_info(param_to_change)
					yield from display_registration_form(mes)
		else:
			yield from display_registration_form('Ошибка заполнения капчи')
	else:
		yield from display_registration_form('Заполните капчу!')