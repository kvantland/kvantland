#!/usr/bin/python3
from bottle import route, request, response, redirect

from config import config
import nav
import json
import urllib.request as urllib2
import http.cookiejar as cookielib
from login import check_login, do_redirect, do_login, current_user

import urllib.parse
from urllib.error import HTTPError


client_id = 51749604
redirect_uri = 'http://localhost:8080/login/vk'
client_secret = 'oGUIYzsB2dsk7hwp6GBI'
auth_url = 'http://oauth.vk.com/authorize'
token_url = 'https://oauth.vk.com/access_token'
info_url = 'https://api.vk.com/method/users.get'

@route('/login/vk')	
def login_attempt(db):
	user = get_user()
	login = 'vk#' + str(user['id'])
	password = None
	name = user['first_name'] + ' ' + user['last_name']
	password = ''
	if (user := check_login(db, login, password)) != None:
		do_login(user)
	else:
		add_user(login, name, password, db)
		user = check_login(db, login, password)
		do_login(user)
	yield '<!DOCTYPE html>'

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
		access_token = token['access_token'][6:]
		params = {'user_ids': token['user_id'],
		'fields': 'uid,first_name,last_name,screen_name,sex,bdate',
		'access_token': token['access_token'],
		'v': 5.131 
		}
		info_path = info_url + '?' + urllib.parse.urlencode(params)
		try:
			cont = urllib2.urlopen(info_path)
			user_info = json.loads(cont.read())
			return user_info
		except HTTPError:
			return {}

def vk_current_user():
	curr_user = request.get_cookie('user', secret=key)
	yield '<p>' + str(curr_user) + '</p>'
	try:
		return int(curr_user)
	except Exception:
		return None

def convert(info):
	try:
		if info['response']:
			return info['response'][0]
	except KeyError:
		return 'Error'

def get_user():
	return convert(get_info(get_token()))

def add_user(логин, имя, пароль, db):
	db.execute("insert into Ученик (логин, пароль, имя) values (%s, %s, %s)", (логин, пароль, имя))