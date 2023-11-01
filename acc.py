from html import escape
from bottle import route, request, response, redirect
import nav
import sys
from login import current_user
from config import config

all_info = config['reg']['all_info']

alph_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
alph_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
symb = ' -_'

# поля в которых могут использоваться только буквы и символы из symb
let_only = ['name', 'surname', 'city']

field_amount = len(all_info) - 1 # количество полей в форме
field_size = 40 # размер поля
pad = 4 # расстояние между полями
button_margin = 20 # расстояние до кнопки
button_size = 70 # размер кнопки
form_size = button_size + field_amount * field_size + pad * field_amount + button_margin # размер формы

# отображаемая в форме пользовательсткая информация
user_info = dict()

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
	user_info[field_name] = ''
	type_info[field_name] = type_name
	placeholder_info[field_name] = placeholder_name
	if type_name == 'select':
		options = field[3]
		option_info[field_name] = options

@route('/acc')
def display_pers_acc(db, err=''):
	yield '<!DOCTYPE html>'
	yield '<title>Личный кабинет</title>'
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
	yield '<div class="acc_plot">'
	yield '<div class="acc_header"> Личный кабинет </div>'
	yield '<div class="acc_form">'
	yield f'<form method="post" class="acc" style="height: {form_size}px">'
	user = get_user(db, current_user())
	for i in range(2, len(all_info)):
		field = all_info[i]
		if user[i - 2] == None:
			user[i - 2] = ''
		yield '<div class="acc_field">'
		yield f'<p> {field[2]}: </p>'
		if field[1] != 'select':
			yield f'<input class="acc" style="height: {field_size}px" name="{field[0]}" type="{field[1]}" value="{user[i - 2]}" required/>'
		else:
			yield f'<select class="acc" style="height: {field_size}px" name="{field[0]}" required>'
			yield f'<option  value="" disabled selected> </option>'
			opt_list = field[3]
			for opt in opt_list:
				if user[i - 2] != str(opt):
					yield f'<option> {opt} </option>'
				else:
					yield f'<option selected> {opt} </option>'
			yield '</select>'
		yield '</div>'
	yield '<div class="acc_field">'
	yield '<p>Счёт</p>'
	yield f'<input class="acc" style="height: {field_size}px" value="{user[5]}" readonly/>'
	yield '</div>'
	yield f'<button type="submit" class="acc_submit_button" style="height: {button_size}px; margin-top:{button_margin}px"> СОХРАНИТЬ </button>'
	yield '</form>'
	yield '</div>'
	yield '</div>'
	yield '</main>'

def get_user(db, user):
	db.execute('select имя, фамилия, школа, город, класс, счёт from Ученик where ученик= %s', (user, ))
	user_list = list(db.fetchall()[0])
	return user_list

def check_format(user_info):
	for field in user_info:
		min_size = config['reg']['min_' + field + '_size']
		max_size = config['reg']['max_' + field + '_size']
		name = placeholder_info[field]

		if field in let_only:
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
					return "Недопустимые символы в поле " + name
			if tmp_ru + tmp_en == 0:
				return "В поле " + name + " должны присутствовать буквы"
			if tmp_ru + tmp_en == 2:
				return "В поле " + name + " присутствуют буквы из разных языков"


		if type_info[field] == "select":
			if not(user_info[field] in option_info[field]):
				return "Недопустимое значение в поле " + name + "<br /> Пожалуйста, выберите значение из выпадающего списка"

		if len(user_info[field]) < min_size:
			return "Слишком мало символов в поле " + name + ", <br /> должно быть минимум " + str(min_size)
		if len(user_info[field]) > max_size:
			return "Слишком много символов в поле " + name

	return False

@route('/acc', method="post")
def check_new_params(db):

	user_info = dict()

	for i in range(2, len(all_info)):
		name = all_info[i][0]
		user_info[name] = request.forms.get(name).encode('l1').decode().strip()

	if not(stat := check_format(user_info)):
		set_new_params(db, user_info)
		redirect('/')
	else:
		yield from display_pers_acc(db, stat)

def set_new_params(db, user_info):
	new_name = user_info['name']
	new_surname = user_info['surname']
	new_school = user_info['school']
	new_city = user_info['city']
	new_class = user_info['clas']
	db.execute('update Ученик set имя=%s, фамилия=%s, школа=%s, город=%s, класс=%s where ученик=%s', (new_name, new_surname, new_school, new_city, new_class, current_user(), ))
