#!/usr/bin/python3

from bottle import route, request, response, redirect

from config import config
import json
import urllib.request as urllib2
from login import do_login, current_user
from passlib.hash import pbkdf2_sha256 as pwhash

import urllib.parse

import sys

client_secret = config['vk']['client_secret']
redirect_uri = config['vk']['redirect_uri']
client_id = config['vk']['client_id']
token_url = config['vk']['token_url']
info_url = config['vk']['info_url']

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
