from html import escape
from bottle import route, request, response, redirect
import nav
import user
import sys
from login import current_user
from config import config

all_info = [['name', 'text', 'Имя'],
			['surname', 'text', 'Фамилия'],
			['school', 'text', 'Школа'],
			['city', 'text', 'Город'],
			['email', 'email', 'Почта'],
			['clas', 'select', 'Класс', ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', 'Другое']]]

alph_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
alph_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
symb = ' -_'

# поля в которых могут использоваться только буквы и символы из symb
lett_only = ['name', 'surname', 'city']

field_amount = len(all_info) + 1 # количество полей в форме
field_size = 40 # размер поля
pad = 4 # расстояние между полями
button_margin = 20 # расстояние до кнопки
button_size = 70 # размер кнопки
form_size = button_size + field_amount * field_size + pad * field_amount + button_margin # размер формы

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

def empty_user_info():
	user_info = dict()
	for field in all_info:
		user_info[field[0]] = ''
	return user_info

@route('/acc')
def display_pers_acc(db, err={}, user_info=empty_user_info()):
	if current_user(db) == None:
		redirect('/')
	yield '<!DOCTYPE html>'
	yield '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
	yield '<title> Личный кабинет — Квантландия </title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/acc.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'

	yield from user.display_banner_empty()
	yield '<div class="content_wrapper">'
	yield '<div class="acc_form">'
	yield '<div class="header"> Личный кабинет </div>'
	yield f'<form id="acc" method="post">'
	yield '<div class="fields">'
	start_user_info = get_user(db, current_user(db))
	for i in range(len(all_info)):
		field = all_info[i]
		name = field[0]
		if user_info[name]:
			value_ = user_info[name]
		else:
			value_ = start_user_info[name]
		if value_ == None:
			value_ = ''
		yield '<div class="full_field">'
		yield '<div class="field">'
		yield '<div class="content">'
		placeholder_ = placeholder_info[name]
		type_ = type_info[name]
		yield f'<div class="placeholder"> {placeholder_} </div>'
		if type_ == 'select':
			yield f'<div class="select_line" name="{name}">'
			yield f' <input name="{name}" type="{type_}" value="{escape(value_)}" readonly required />'
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
	yield '''<label for="approval"> Я принимаю условия <a href="/policy"> Политики конфиденциальности</a> и даю <span class="underline approval"> согласие
		на обработку своих персональных данных</span>'''
	yield '</label>'
	yield '</div>'
	if err and 'approval' in err.keys():
		yield f'<div class="err"> {err["approval"]} </div>'
	else:
		yield f'<div class="err hidden"></div>'
	yield '</div>'
	yield '</form>'
	yield '<div class="button_area">'
	yield f'<button type="submit" class="acc_button" form="acc"> Сохранить </button>'
	yield '<hr size="1">'
	yield f'<a href="/"><div class="back_button"> Назад </div></a>'
	yield '</div>'
	yield '</div>'

	yield '<div class="approv hidden">'
	yield '<div class="header">' 
	yield '<div> Согласие на обработку персональных данных </div>'
	yield '<div> <img class="cross" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="content">'
	yield '''<div class="par">
				На­сто­я­щим я со­гла­ша­юсь с тем, что про­чи­тал <a href="/policy">По­ли­ти­ку 
				Конфиденциальности</a> и дал согласие на обработку моих 
				персональных данных: фамилия, имя, наименование и номер 
				школы, номер класса, город, e-mail и иных, указанных в <a href="/policy">Политике</a>, 
				в соответствии с её положени­я­ми. </div>'''
	yield '''<div class="par"> 
				Если мне меньше 14 лет,  я со­гла­ша­юсь с тем, что мои за­конные 
				пред­ста­ви­те­ли –  ро­ди­те­ли/усы­но­ви­те­ли/по­пе­чи­тель  прочитали 
				<a href="/policy">По­ли­ти­ку Конфиденци­аль­но­сти</a> и дали согласие на обработку 
				моих персональных данных: фамилия, имя, наименование и 
				номер школы, номер класса, город, e-mail и иных, указанных в 
				Политике,  в соответствии с её положениями.</div>'''
	yield '''<div class="par">
				Я по­ни­маю, что могу ото­звать свое со­гла­сие в любой мо­мент по 
				адресу электронной почты support@kvantland.com.</div>'''
	yield '</div>'
	yield '</div>'
	yield '<script type="text/javascript" src="/static/design/user.js"></script>'
	yield '<script type="text/javascript" src ="/static/dialog.js"></script>'
	yield '<script type="text/javascript" src ="/static/design/acc.js"></script>'
	yield '<script src="https://www.google.com/recaptcha/api.js" async defer></script>'

def get_user(db, user):
	db.execute('select name, surname, school, town, clas, score, email from Kvantland.Student where student= %s', (user, ))
	user_list = list(db.fetchall()[0])
	user_info = {'name': user_list[0],
				'surname': user_list[1],
				'school': user_list[2],
				'city': user_list[3],
				'clas': user_list[4],
				'score': user_list[5],
				'email': user_list[6]}
	return user_info

def check_format(user_info):
	err_dict = {}

	for field in user_info:
		min_size = config['acc']['min_' + field + '_size']
		max_size = config['acc']['max_' + field + '_size']
		name = placeholder_info[field]

		'''
		if field in lett_only:
			tmp_en = 0
			tmp_ru = 0
			for s in user_info[field]:
				if s in alph_en:
					tmp_en = 1
				elif s in alph_ru:
					tmp_ru = 1
				elif s in symb:
					continue
				else:
					err_dict[field] = "Недопустимые символы в поле " + name
			if tmp_ru + tmp_en == 0:
				err_dict[field] = "В поле " + name + " должны присутствовать буквы"
			if tmp_ru + tmp_en == 2:
				err_dict[field] = "В поле " + name + " присутствуют буквы из разных языков"
		'''

		if type_info[field] == "select":
			if not(user_info[field] in option_info[field]):
				err_dict[field] = "Значение не из списка"

		if len(user_info[field]) < min_size:
			err_dict[field] = "Слишком мало символов в поле, <br /> должно быть минимум " + str(min_size)
		if len(user_info[field]) > max_size:
			err_dict[field] = "Слишком много символов"

	return False, ''

def update_info(user_info, field):
	user_info[field] = ''
	return user_info

@route('/acc', method="post")
def check_new_params(db):

	user_info = dict()

	for i in range(len(all_info)):
		name = all_info[i][0]
		user_info[name] = request.forms.decode().get(name).strip()

	stat, field_to_update = check_format(user_info)

	if not stat:
		set_new_params(db, user_info)
		redirect('/')
	else:
		user_info = update_info(user_info, field_to_update)
		yield from display_pers_acc(db, stat, user_info)

def set_new_params(db, user_info):
	new_name = user_info['name']
	new_surname = user_info['surname']
	new_school = user_info['school']
	new_city = user_info['city']
	new_class = user_info['clas']
	new_email = user_info['email']
	db.execute('update Kvantland.Student set name=%s, surname=%s, school=%s, town=%s, clas=%s, email=%s where student=%s', (new_name, new_surname, new_school, new_city, new_class, new_email, current_user(db), ))
