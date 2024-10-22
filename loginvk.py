#!/usr/bin/python3

from bottle import route, request, response

from config import config
import json
import jwt
import urllib.request as urllib2
from passlib.hash import pbkdf2_sha256 as pwhash
import pkce

import certifi
from urllib.error import HTTPError, URLError

import urllib.parse

import string
import secrets
import random

import sys

client_secret = config['vk']['client_secret']
redirect_uri = config['vk']['redirect_uri']
client_id = config['vk']['client_id']
token_url = config['vk']['token_url']
info_url = config['vk']['info_url']


@route('/api/vk_PKCE', method=["OPTIONS"])
def resp():
	response.iter_headers(
		('Allow', 'POST'),
		('Access-Control-Allow-Origin', config['client']['url']),
		('Access-Control-Allow-Methods', ['POST', 'OPTIONS']),
	)
	response.status = 200


@route('/api/vk_PKCE', method=["POST"])
def generate_vk_PKCE():
	code_verifier = pkce.generate_code_verifier(length=128)
	code_challenge = pkce.get_code_challenge(code_verifier)
	print(code_verifier, code_challenge)
	return json.dumps({
			'code_verifier': code_verifier,
			'code_challenge': code_challenge,
			})


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
	code = data['code']
	code_verifier = data['code_verifier']
	device_id = data['device_id']
	state = data['state']
	
	print(code, device_id, file=sys.stderr)
	
	access_info = get_vk_access_token(code=code, code_verifier=code_verifier, device_id=device_id, state=state)
	access_token = access_info['access_token']
	user_id = access_info['user_id']

	user = get_user_vk_info(access_token, user_id)
	print('user info: ', user, file=sys.stderr)
	resp = {
		'user_info': {
			'login': "",
			'name': "",
			'surname': "",
			'town': "",
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
			resp['user_info']['town'] = user['city']['title']
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

	print(resp, file=sys.stderr)
	return json.dumps(resp)


def get_vk_access_token(code, code_verifier, device_id, state):
	params = {
		'grant_type': "authorization_code",
		'code_verifier': code_verifier,
		'redirect_uri': config['client']['url'],
		'code': code,
		'client_id': client_id,
		'device_id': device_id,
		'state': state,
	}
	request = urllib2.Request(url=token_url, data=urllib.parse.urlencode(params).encode('utf-8'), 
						   headers={'Content-Type': "application/x-www-form-urlencoded"}, method='POST')
	try:
		cont = urllib2.urlopen(request, cafile=certifi.where())
	except HTTPError as e:
		print(f"HTTP Error: {e.code}")
	except URLError as e:
		print(f"URL Error: {e.reason}")
	response = json.loads(cont.read())
	print(response, file=sys.stderr)
	
	return {'access_token': response['access_token'], 'user_id': response['user_id']}


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
	print(user_info, file=sys.stderr)
	
	return user_info['response'][0]

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

