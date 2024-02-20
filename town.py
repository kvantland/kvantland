#!/usr/bin/python3

import random
from bottle import route, HTTPError

import nav
import user
import footer

def require_user(db):
	user_id = user.current_user(db)
	if user_id:
		db.execute('select * from Kvantland.Student where student = %s', (user_id, ))
		(stats), = db.fetchall()
		if None in stats:
			return None
	return user_id

@route('/town/<town:int>/')
def show_town(db, town):
	user_id = require_user(db)
	if not user_id:
		redirect('/')

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

	if user_id is not None:
		db.execute('select variant, position, points, name, answer_true from Kvantland.AvailableProblem join Kvantland.Variant using (variant) join Kvantland.Problem using (problem) where town = %s and student = %s', (town, user_id))
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
		yield f'<a xlink:href="{link}" class="level level_{status}" transform="translate({x} {y})"><title>{name}</title>'
		yield f'<circle class="level-icon" r="0.65em" />'
		yield f'<text class="level-value">{points}</text>'
		yield f'</a>'
	yield '</svg>'
	yield '</div>'
	yield from footer.display_basement()
