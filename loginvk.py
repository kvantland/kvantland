#!/usr/bin/python3

from bottle import route, request, response, redirect

from config import config
import json
import jwt
import urllib.request as urllib2
from login import do_login, current_user
from passlib.hash import pbkdf2_sha256 as pwhash
import certifi
from urllib.error import HTTPError, URLError

import urllib.parse

import sys

client_secret = config['vk']['client_secret']
redirect_uri = config['vk']['redirect_uri']
client_id = config['vk']['client_id']
token_url = config['vk']['token_url']
info_url = config['vk']['info_url']

@route('/api/vk_auth', method=["OPTIONS"])
def resp():
	print(dict(request.headers), file=sys.stderr)
	response.iter_headers(
		('Allow', 'POST'),
		('Access-Control-Allow-Origin', config['client']['url']),
		('Access-Control-Allow-Methods', ['POST', 'OPTIONS']),
	)
	response.status = 200

@route('/api/vk_auth', method=["POST"])
def vk_auth(db):
	data =  json.loads(request.body.read().decode('utf-8'))
	print(data, file=sys.stderr)
	access_token = data['token']
	user_id = data['user_id']
	print(access_token, user_id, file=sys.stderr)

	user = get_user_vk_info(access_token, user_id)
	print('user info: ', user, file=sys.stderr)
	resp = {
		'user_info': {
			'login': "",
			'name': "",
			'surname': "",
			'city': "",
			'school': "",
		},
		'user_exists': False,
		'tokens': {
			'access_token': "",
			'refresh_token': "",
		}
	}

	resp['user_info']['login'] = 'vk#' + str(user['id'])
	#password, name, surname, city, school = ('some', None, None, None, None)
	if 'first_name' in user.keys():
		resp['user_info']['name'] = user['first_name']
	if 'last_name' in user.keys():
		resp['user_info']['surname'] = user['last_name']
	if 'city' in user.keys():
		if 'title' in user['city'].keys():
			resp['user_info']['city'] = user['city']['title']
	if 'schools' in user.keys():
		if len(user['schools']) > 0:
			resp['user_info']['school'] = user['schools'][0]['name']
		
	login = resp['user_info']['login']
	if (user := vk_check_login(db, login )) != None:	
		resp['user_exists'] = True 
		access_key = config['keys']['access_key']
		refresh_key = config['keys']['refresh_key']
		resp['tokens']['access_token'] = jwt.encode(payload={'login': login, 'user_id': user}, key=access_key, algorithm='HS256')
		resp['tokens']['refresh_token'] = jwt.encode(payload={'login': login, 'user_id': user}, key=refresh_key, algorithm='HS256')

	return json.dumps(resp)


def get_user_vk_info(access_token, user_id):
	params = {
		'user_ids': user_id,
		'fields': 'uid, first_name, last_name, city, schools',
		'access_token': access_token,
		'v': '5.131',
	}
	info_path = info_url + '?' + urllib.parse.urlencode(params)
	try:
		cont = urllib2.urlopen(info_path, cafile=certifi.where())
	except HTTPError as e:
		print(f"HTTP Error: {e.code}")
	except URLError as e:
		print(f"URL Error: {e.reason}")
	user_info = json.loads(cont.read())

	return user_info['response'][0]


@route('/login/vk')	
def login_attempt(db):
	user = get_user()
	login = 'vk#' + str(user['id'])
	password, name, surname, city, school = ('some', None, None, None, None)
	try:
		name = user['first_name']
	except KeyError:
		pass
	try:
		surname = user['last_name']
	except KeyError:
		pass
	try:
		city = user['city']['title']
	except KeyError:
		pass
	if user['schools']:
		try:
			school = user['schools'][0]['name']
		except KeyError:
			pass
	if (user := vk_check_login(db, login)) != None:	
		do_login(user, login)
	else:
		user = add_user(login, name, surname, city, school, password, db)
		do_login(user, login)
	redirect('/')

def vk_check_login(db, user_name):
	db.execute('select student from Kvantland.Student where login = %s', (user_name, ))
	try:
		(user, ), = db.fetchall()
	except ValueError:
		return None
	return int(user)

def get_token():
	if request.query['code']:
		params = {'client_id': client_id,
		'client_secret': client_secret,
		'code': request.query['code'],
		'redirect_uri': config['client']['url'] + '/api/vk_auth'}
		token_path = token_url + '?' + urllib.parse.urlencode(params)
		try:
			cont = urllib2.urlopen(token_path)
			token = json.loads(cont.read())
			return token
		except:
			print('Something went wrong', file=sys.stderr)
		return ''

def get_info(token):
	if token['access_token']:
		params = {'user_ids': token['user_id'],
		'fields': 'uid, first_name, last_name, city, schools',
		'access_token': token['access_token'],
		'v': '5.131' 
		}
		info_path = info_url + '?' + urllib.parse.urlencode(params)
		cont = urllib2.urlopen(info_path)
		user_info = json.loads(cont.read())
		return user_info

def convert(info):
	return info['response'][0]

def get_user():
	return convert(get_info(get_token()))

def add_user(login, name, surname, city, school, password, db):
	db.execute("insert into Kvantland.Student (login, name, surname, town, school, password) values (%s, %s, %s, %s, %s, %s) returning student", (login, name, surname, city, school, pwhash.hash(password)))
	(user, ), = db.fetchall()
	db.execute("insert into Kvantland.AvailableProblem (student, variant) select distinct on (problem) %s, variant from Kvantland.Variant order by problem, random();", (user, ))
	db.execute("insert into Kvantland.Score (student, tournament) values (%s, %s)", (user, config["tournament"]["version"]))
	return user
