#!/usr/bin/python3

import random
from bottle import route, request
import json
from config import config
from login import check_token
import sys

MODE = config['tournament']['mode']

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
		db.execute('''select variant, position, curr_points, name, answer_true from Kvantland.AvailableProblem 
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
