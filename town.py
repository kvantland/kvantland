#!/usr/bin/python3

import random
from bottle import route, HTTPError, redirect, request, response
import json
from config import config
from login import do_logout, check_token
import nav
import sys
import user
import footer

MODE = config['tournament']['mode']

def require_user(db):
	user_id = user.current_user(db)
	if user_id:
		db.execute('select * from Kvantland.Student where student = %s', (user_id, ))
		(stats), = db.fetchall()
		if None in stats:
			return None
	return user_id

@route('/api/town_breadcrumbs', method="POST")
def get_town_breadcrumbs(db):
	resp = {
		'status': False,
		'breadcrumbs': [],
	}
	try:
		town = json.loads(request.body.read())['town']
		print('town: ', town, file=sys.stderr)
	except:
		return json.dumps(resp)
	try:
		db.execute('''select Kvantland.Town.name
				from Kvantland.Town where town = %s''', (town,))
		(town_name, ), = db.fetchall()
		resp['breadcrumbs'].append({'name': 'Квантландия', 'link': '/land'})
		resp['breadcrumbs'].append({'name': town_name, 'link': f'/town/{town}'})
	except:
		print('bad db', resp, file=sys.stderr)
		return json.dumps(resp)
	
	print('resp: ', resp, file=sys.stderr)
	resp['status'] = True
	return json.dumps(resp)

@route('/api/town_data', method="POST")
def get_town_data(db):
	resp = {
		'status': False,
		'towns': []
	}
	try:
		town = json.loads(request.body.read())['town']
	except:
		return json.dumps(resp)

	token_status = check_token(request)
	if token_status['error']:
		return json.dumps(resp)
	user_id = token_status['user_id']
	try:
		db.execute('''select variant, position, points, name, answer_true from Kvantland.AvailableProblem 
			join Kvantland.Variant using (variant) join Kvantland.Problem using (problem) 
			where town = %s and student = %s and tournament = %s''', (town, user_id, config["tournament"]["version"]))
		for variant, position, points, name, ans_true in db.fetchall():
			try:
				x, y = position
			except TypeError:
				μ, σ = 50.0, 15.0
				x = random.normalvariate(μ, σ)
				y = random.normalvariate(μ, σ)
			status = {
				None: 'open',
				True: 'solved',
				False: 'failed',
			}[ans_true]
			resp['towns'].append({"variantID": variant, "x": x, "y": y, "points": points, "name": name, "status": status})
	except:
		return json.dumps(resp)

	resp['status'] = True
	print('resp: ', resp, file=sys.stderr)
	return json.dumps(resp)


@route('/town/<town:int>/')
def show_town(db, town):
	if MODE == 'private':
		user_id = require_user(db)
		if not user_id:
			redirect('/')
	elif MODE == 'public':
		user_id = None
		do_logout()

	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	db.execute('select name from Kvantland.Town where town = %s', (town,))
	(name, ), = db.fetchall()
	yield f'<title>{name}</title>'
	yield '<link rel="icon" href="/static/design/icons/logo.svg">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/nav.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/town.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/footer.css">'
	yield '<script type="module" src="/static/design/user.js"></script>'
	yield from user.display_banner_tournament(db)
	yield '<div class="content_wrapper">'
	yield from nav.display_breadcrumbs(('/land', 'Квантландия'), (f'/town/{town}/', f'{name}'))
	yield '<svg version="1.1" class="map" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield '<defs>'
	yield '<clipPath id="map_border">'
	yield f'''<path stroke="#1E8B93" stroke-width="3px" fill="none" d="
		M 1.5 21.5
		v 676
		a 20 20 0 0 0 20 20
		h 1237
		a 20 20 0 0 0 20 -20
		v -676
		a 20 20 0 0 0 -20 -20
		h -1237
		a 20 20 0 0 0 -20 20
		z" />'''
	yield '</clipPath>'
	yield '</defs>'


	yield f'<image href="/static/map/town-{town}.png" width="1280" height="720"preserveAspectRatio="xMidYMid" clip-path="url(#map_border)" meet />'
	yield f'''<path stroke="#1E8B93" stroke-width="3px" fill="none" d="
		M 1.5 21.5
		v 676
		a 20 20 0 0 0 20 20
		h 1237
		a 20 20 0 0 0 20 -20
		v -676
		a 20 20 0 0 0 -20 -20
		h -1237
		a 20 20 0 0 0 -20 20
		z" />'''

	if MODE == 'private':
		if user_id is not None:
			db.execute('select variant, position, points, name, answer_true from Kvantland.AvailableProblem join Kvantland.Variant using (variant) join Kvantland.Problem using (problem) where town = %s and student = %s and tournament = %s', (town, user_id, config["tournament"]["version"]))
		else:
			db.execute('select null, position, points, name, null from Kvantland.Problem where town = %s', (town,))
	elif MODE == 'public':
		db.execute('select variant, position, points, name, answer_true from Kvantland.AvailableProblem join Kvantland.Variant using (variant) join Kvantland.Problem using (problem) where town = %s and tournament = %s', (town, config["tournament"]["version"]))
	for variant, position, points, name, ans_true in db.fetchall():
		try:
			x, y = position
		except TypeError:
			μ, σ = 50.0, 15.0
			x = random.normalvariate(μ, σ)
			y = random.normalvariate(μ, σ)
		status = {
			None: 'open',
			True: 'solved',
			False: 'failed',
		}[ans_true]
		if MODE == 'private':
			link = f'/problem/{variant}/' if user_id is not None else f'/login?path=/town/{town}/'
		elif MODE == 'public':
			link = f'/problem/{variant}/'
		yield f'<a xlink:href="{link}" class="level level_{status}" transform="translate({x} {y})"><title>{name}</title>'
		yield f'<circle class="level-icon" r="0.65em" />'
		yield f'<text class="level-value">{points}</text>'
		yield f'</a>'
	yield '</svg>'
	yield '</div>'
	yield from footer.display_basement()
