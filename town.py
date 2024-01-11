#!/usr/bin/python3

import random
from bottle import route, HTTPError

import nav
import user

@route('/town/<town:int>/')
def show_town(db, town):
	user_id = user.current_user(db)

	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	db.execute('select название from Город where город = %s', (town,))
	(name, ), = db.fetchall()
	yield f'<title>{name}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield from nav.display_breadcrumbs(('/', 'Квантландия'))
	yield f'<h1>{name}</h1>'
	yield '</div>'
	yield '<svg version="1.1" class="map" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield f'<image href="/static/map/town-{town}.jpg" width="1280" height="720" preserveAspectRatio="xMidYMid meet" />'

	db.execute('select вариант, положение, баллы, название, ответ_верен from ДоступнаяЗадача join Вариант using (вариант) join Задача using (задача) where город = %s', (town, ))
	
	cur_position = []
	for variant, position, points, name, ans_true in db.fetchall():
		try:
			x, y = position
			if cur_position == position:
				continue
			cur_position = position
		except TypeError:
			μ, σ = 50.0, 15.0
			x = random.normalvariate(μ, σ)
			y = random.normalvariate(μ, σ)
		status = {
			None: 'open',
			True: 'solved',
			False: 'failed',
		}[ans_true]
		link = f'/problem/{variant}/0/' 
		yield f'<a xlink:href="{link}" class="level level_{status}" transform="translate({x} {y})"><title>{name}</title>'
		yield f'<circle class="level-icon" r="0.65em" />'
		yield f'<text class="level-value">{points}</text>'
		yield f'</a>'
	yield '</svg>'
