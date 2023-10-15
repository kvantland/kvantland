from login import do_login, current_user
from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash
import nav
import json
from config import config
import urllib.request as urllib2
import urllib.parse

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

@route('/reg')
def reg_from():
	if current_user() != None:
		redirect('/')
	yield from display_registration_form()

def display_registration_form(err=None):
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
	yield f'<input style="height: {field_size}px" name="login" type="text" placeholder="Логин" required />'
	yield f'<input style="height: {field_size}px" name="password" type="password" placeholder="Пароль" required />'
	yield f'<input style="height: {field_size}px" name="name" type="text" placeholder="Имя" required/>'
	yield f'<input style="height: {field_size}px" name="surname" type="text" placeholder="Фамилия" required/>'
	yield f'<input style="height: {field_size}px" name="school" type="text" placeholder="Школа" required/>'
	yield f'<select style="height: {field_size}px" name="clas" required>'
	yield '<option value="" disabled selected> Класс </option>'
	yield '<option> 1 </option>'
	yield '<option> 2 </option>'
	yield '<option> 3 </option>'
	yield '<option> 4 </option>'
	yield '<option> 5 </option>'
	yield '<option> 6 </option>'
	yield '<option> 7 </option>'
	yield '<option> 8 </option>'
	yield '<option> 9 </option>'
	yield '<option> 10 </option>'
	yield '<option> 11 </option>'
	yield '<option> Другое </option>'
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
		return "Слишком длинный логин"
	for s in login:
		if s != '_' and s != '-' and s not in alph:
			return "Логин должен состоять из английских букв и символов - и _ <br /> Ваш логин содержит недопустимые символы"
	if len(login) < min_log_size:
		return "Количество символов в логине должно составлять минимум " + str(min_log_size)
	if len(password) > max_password_size:
		return "Слишком длинный пароль"
	if len(password) < min_password_size:
		return "Количество символов в пароле должно составлять минимум " + str(min_password_size)
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
		return "Пароль должен содержать заглавные и строчные буквы, а так же цифры"
	if len(name) > max_name_size:
		return "Слишком длинное имя"
	if len(surname) > max_surname_size:
		return "Слишком длинная фамилия"
	if len(school) > max_school_size:
		return "Слишком длинное название школы"
	if len(school) < min_school_size:
		return "Слишком короткое название школы"
	if not(clas in [str(i) for i in range(1, 12)]) and clas != "Другое":
		return "Класса с таким номером не существует"
	return False

@route('/reg', method='POST')
def login_attempt(db):
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
				yield from display_registration_form('К сожалению, пользователь с таким логином уже существует, <br /> попробуйте другой логин')
			else:
				login = request.forms.login.strip()
				password = request.forms.password.strip()
				name = request.forms.name.strip()
				surname = request.forms.surname.strip()
				clas = request.forms.clas.strip()
				school = request.forms.school.strip()
				stat = check_format(login, password, name, surname, school, clas)
				if not stat:
					user = add_user(db, login, password, name, surname, school, clas)
					do_login(user)
					redirect('/')
				else:
					yield from display_registration_form(stat)
		else:
			yield from display_registration_form('Ошибка заполнения капчи')
	else:
		yield from display_registration_form('Заполните капчу!')