#!/usr/bin/python3

import random
from bottle import route, request
import json
from config import config
from login import check_token
import sys

MODE = config['tournament']['mode']

@route('/api/town_data', method="POST")
def get_town_data(db):
	print('===================')
	print()
	print()
	print('get town data:')
	resp = {
		'status': False,
		'towns': []
	}
	try:
		town = json.loads(request.body.read())['town']
		classes = json.loads(request.body.read())['classes']
	except:
		return json.dumps(resp)
	print('town: ', town)
	print('classes: ', classes)

	token_status = check_token(request)
	if token_status['error']:
		return json.dumps(resp)
	user_id = token_status['user_id']
	try:
		db.execute('''select variant, position, curr_points, points, variant_points, name, answer_true from Kvantland.AvailableProblem 
			join Kvantland.Variant using (variant) join Kvantland.Problem using (problem) 
			where town = %s and student = %s and tournament = %s and (classes = %s or classes = 'all')''', 
			(town, user_id, config["tournament"]["version"], classes))
		for variant, position, curr_points, points, variant_points, name, ans_true in db.fetchall():
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
			if variant_points:
				send_points = variant_points
			elif curr_points:
				send_points = curr_points
			else:
				send_points = points
			resp['towns'].append({"variantID": variant, "x": x, "y": y, "points": send_points, "name": name, "status": status})
	except:
		return json.dumps(resp)

	resp['status'] = True
	print('resp: ', resp, file=sys.stderr)
	return json.dumps(resp)
