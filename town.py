#!/usr/bin/python3

import random
from bottle import route, HTTPError
from config import config
import nav
import user

@route('/town/<town:int>/')
def show_town(db, town):
	user_id = user.current_user(db)

	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	db.execute('select name from Kvantland.Town where town = %s', (town,))
	(name, ), = db.fetchall()
	yield f'<title>{name}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield from nav.display_breadcrumbs(('/', 'Квантландия'))
	yield f'<h1>{name}</h1>'
	yield '</div>'
	yield '<svg version="1.1" class="map" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield f'<image href="/static/map/town-{town}.png" width="1280" height="720" preserveAspectRatio="xMidYMid meet" />'

	if user_id is not None:
		db.execute('select variant, position, points, name, answer_true from Kvantland.AvailableProblem join Kvantland.Variant using (variant) join Kvantland.Problem using (problem) where town = %s and student = %s and tournament = %s', (town, user_id, config["tournament"]["version"]))
	else:
		db.execute('select null, position, points, name, null from Kvantland.Problem where town = %s', (town,))
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
		link = f'/problem/{variant}/' if user_id is not None else f'/login?path=/town/{town}/'
		yield f'<a xlink:href="{link}">'
		yield f'<g class="level level_{status}" transform="translate({x} {y})">'
		yield f'<title>{name}</title>'
		yield f'<circle class="level-icon" r="0.65em" cx="0" cy="0" />'
		yield f'<text class="level-value" x="0" y="20px">{points}</text>'
		yield '</g>'
		yield f'</a>'
	yield '</svg>'
