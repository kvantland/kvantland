#!/usr/bin/python3

from unittest import result
from bottle import route, request
from passlib.hash import pbkdf2_sha256 as pwhash
import json
import jwt
import sys
import time

from config import config
from check_fields_format import *

client_id = config['vk']['client_id']
redirect_uri = config['vk']['redirect_uri']
auth_url = config['vk']['auth_url']

params = {'client_id': 	client_id, 'redirect_uri': redirect_uri, 'response_type': 'code'}

@route('/api/login_fields')
def get_login_fields():
	fields = [
		{'type': "input", 'inputType': "text", 'name': "login", 'placeholder': "Логин или email"},
		{'type': "input", 'inputType': "password", 'name': "password", 'placeholder': "Пароль"}
	]
	return json.dumps(fields)


@route('/api/refresh_tokens', method="POST")
def refresh_tokens():
	print('refresh', file=sys.stderr)
	resp = {
		'access_token': "",
		'refresh_token': "",
	}
	try:
		data = json.loads(request.body.read())
		old_refresh_token = data['refresh_token']
	except:
		return json.dumps(resp)
	print(old_refresh_token, file=sys.stderr)
	
	try:
		user_data = jwt.decode(jwt=old_refresh_token, key=config['keys']['refresh_key'], algorithms=['HS256'])
		login = user_data['login']
		user_id = user_data['user_id']
	except:
		return json.dumps(resp)
	
	resp['refresh_token'] = jwt.encode(payload={'login': login, 'user_id': user_id, 'time': time.time()}, key=config['keys']['refresh_key'], algorithm='HS256')
	resp['access_token'] = jwt.encode(payload={'login': login, 'user_id': user_id, 'time': time.time()}, key=config['keys']['access_key'], algorithm='HS256')

	return json.dumps(resp)


@route('/api/check_login', method="POST")
def check_login_request(db):
	user_data = json.loads(request.body.read())
	resp = {
		'tokens': {
			'access_token': '',
			'refresh_token': '',
		},
		'status': False,
		'errors': dict(),
	}
	try:
		login = user_data['login']
	except:
		login = ''
	
	try:
		password = user_data['password']
	except:
		password = ''
	expected_fields = ['login', 'password']
	pw_check = ['password']
	login_password_strategy = False
	email_password_strategy = False
	
	while True:
		db.execute('select password, student from Kvantland.Student where login = %s', (login, ))
		user_results = db.fetchall()
		if len(user_results) != 0:
			login_password_strategy = True
			break
		db.execute('select password, student from Kvantland.Student where email = %s', (login, ))
		user_results = db.fetchall()
		if len(user_results) != 0:
			email_password_strategy = True
			break
		break

	if len(user_results) == 0:
		resp['errors']['password'] = 'Неверный логин или пароль'
		password_hash = pwhash.hash('-')
	else:
		(password_hash, user_id) = user_results[0]

	if email_password_strategy:
		expected_fields = ['email', 'password']
		user_data = {"email" : login, "password": password}
		db.execute('select login from Kvantland.Student where email = %s and password = %s', (login, password_hash)) # получаем реальный логин
		(real_login, ) = db.fetchall()[0]
		login = real_login


	if pwhash.verify(password, password_hash) and login and user_id:
		access_key = config['keys']['access_key']
		refresh_key = config['keys']['refresh_key']
		resp['tokens']['access_token'] = jwt.encode(payload={'login': login, 'user_id': user_id}, key=access_key, algorithm='HS256')
		resp['tokens']['refresh_token'] = jwt.encode(payload={'login': login, 'user_id': user_id}, key=refresh_key, algorithm='HS256')
	else:
		resp['errors']['password'] = 'Неверный логин или пароль'

	resp['errors'].update(check_fields_format(data=user_data, expected_fields=expected_fields, pw_check=pw_check))
	print(resp['errors'], file=sys.stderr)
	
	if not(resp['errors']):
		resp['status'] = True
	return json.dumps(resp)
	
def check_token(request):
	auth_header = request.get_header('Authorization')
	if auth_header is None:
		return {'error': "Incorrect request format", 'login': ""}
	if 'Bearer' not in auth_header:
		return {'error': "No Bearer in header", 'login': ""}
	token = auth_header.replace('Bearer ', '')
	try:
		payload = jwt.decode(jwt=token, key=config['keys']['access_key'], algorithms=['HS256'])
		print(payload, file=sys.stderr)
	except:
		return {'error': "Not correct token", 'login': ""}
	user_login = payload['login']
	user_id = payload['user_id']
	return {'error': None, 'login': user_login, 'user_id': user_id}
