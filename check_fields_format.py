import urllib
import json
from config import  config
import re


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


def check_fields_format(data, expected_fields=[], pw_check=[], email_check=[], select_check={}):
	err_dict = {}

	alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	alph_lower = 'abcdefghijklmnopqrstuvwxyz'
	alph_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	num = '0123456789'
	login_spec_symb = '-_@.'

	for expected_field_name in expected_fields:
		if not(expected_field_name in data.keys()):
			err_dict[expected_field_name] = 'Поле обязательно для заполнения'

	for field_name, field_data_ in data.items():
		try:
			field_data = field_data_.strip()
		except:
			field_data = field_data_
		print(field_name, field_data)
		
		if not(field_name in expected_fields):
			continue
		if field_name == 'approval':
			continue
		try:
			min_size = config['reg'][f'min_{field_name}_size']
		except:
			min_size = 1
		try:
			max_size = config['reg'][f'max_{field_name}_size']
		except:
			max_size = 500

		if len(field_data) < min_size:
			err_dict[field_name] = f"Минимум {str(min_size)} {lang_form(min_size)}"
		if len(field_data) > max_size:
			err_dict[field_name] = "Слишком много символов"
		
		if field_name in pw_check:
			tmp_upper, tmp_lower, tmp_number = (0, 0, 0)
			for s in field_data:
				if s in alph_upper:
					tmp_upper = 1
				if s in alph_lower:
					tmp_lower = 1
				if s in num:
					tmp_number = 1
			if not(tmp_lower and tmp_upper and tmp_number):
				err_dict[field_name] = "Пароль должен содержать заглавные и </br> строчные буквы, а также цифры"
		
		if field_name == "login":
			tmp_alph = 0
			for s in field_data:
				if s not in login_spec_symb and s not in alph and s not in num:
					err_dict[field_name] = "Логин должен состоять из английских букв, </br> цифр и символов - и _"
				if s in alph:
					tmp_alph = 1
			if not tmp_alph:
				err_dict[field_name] = "Логин должен содержать буквы"
		
		if field_name == 'approval':
			if field_data != True:
				err_dict[field_name] = "Поставьте галочку"
			continue

		if field_name in select_check:
			if not(field_data in select_check[field_name]):
				err_dict[field_name] = "Значение не из списка"

		if field_name in email_check:
			if not(re.match(r'.+@.+', field_data)):
				err_dict[field_name] = "Неверный формат данных"

		if len(field_data) == 0:
			err_dict[field_name] = "Поле обязательно для заполнения"

	print(err_dict)
	return err_dict


def email_already_exists(db, email):
	db.execute("select student from Kvantland.Student where email = %s", (email,))
	try:
		(user,) = db.fetchall()
	except ValueError:
		return None
	return user


def is_new_email(db, new_email, login):
	try:
		db.execute("select email from Kvantland.Student where login = %s", (login, ))
		(prev_email, ), = db.fetchall()
		if prev_email != new_email:
			return True
	except:
		return False
	return False


def login_already_exists(db, login):
	db.execute("select student from Kvantland.Student where login = %s", (login,))
	try:
		(user,) = db.fetchall()
	except ValueError:
		return None
	return user


def check_captcha(token):
	not_robot = False
	params = {
		"secret": config['reg']['secret'],
		"response": token,
	}
	out = config['reg']['reg_url'] + '?' + urllib.parse.urlencode(params)
	cont = urllib.request.urlopen(out)
	not_robot = json.loads(cont.read())['success']
	if not_robot:
		return ""
	else:
		return "Капча не пройдена"

