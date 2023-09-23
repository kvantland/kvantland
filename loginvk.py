#!/usr/bin/python3

from bottle import route, request, response, redirect

from config import config
import json
import urllib.request as urllib2
from login import do_login, current_user

import urllib.parse

client_secret = config['vk']['client_secret']
redirect_uri = config['vk']['redirect_uri']
client_id = config['vk']['client_id']
token_url = config['vk']['token_url']
info_url = config['vk']['info_url']

@route('/login/vk')	
def login_attempt(db):
	user = get_user()
	login = 'vk#' + str(user['id'])
	password = None
	name = user['first_name'] + ' ' + user['last_name']
	if (user := vk_check_login(db, login)) != None:
		do_login(user)
	else:
		add_user(login, name, password, db)
		user = vk_check_login(db, login)
		do_login(user)
	redirect('/')

def vk_check_login(db, user_name):
	db.execute('select ученик from Ученик where логин = %s', (user_name, ))
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
		'redirect_uri': redirect_uri}
		token_path = token_url + '?' + urllib.parse.urlencode(params)
		try:
			cont = urllib2.urlopen(token_path)
			token = json.loads(cont.read())
			return token
		except HTTPError:
			pass
		return ''

def get_info(token):
	if token['access_token']:
		params = {'user_ids': token['user_id'],
		'fields': 'uid,first_name,last_name,screen_name,sex,bdate',
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

def add_user(логин, имя, пароль, db):
	db.execute("insert into Ученик (логин, пароль, имя) values (%s, %s, %s)", (логин, пароль, имя))