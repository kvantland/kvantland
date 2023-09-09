#!/usr/bin/python3

import random
from bottle import route, HTTPError

import nav
import user

@route('/town/<town:int>/')
def show_town(db, town):
	user_id = user.current_user()

	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	db.execute('select название from Город where город = %s', (town,))
	(название, ), = db.fetchall()
	yield f'<title>{название}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield from nav.display_breadcrumbs(('/', 'Квантландия'))
	yield f'<h1>{название}</h1>'
	yield '</div>'
	yield '<svg class="map" viewBox="0 0 1280 720">'
	yield f'<image href="/static/map/town-{town}.jpg" width="1280" height="720" preserveAspectRatio="xMidYMid meet" />'

	if user_id is not None:
		db.execute('select вариант, положение, баллы, название, ответ_верен from ДоступнаяЗадача join Вариант using (вариант) join Задача using (задача) where город = %s and ученик = %s', (town, user_id))
	else:
		db.execute('select null, положение, баллы, название, null from Задача where город = %s', (town,))
	for вариант, положение, баллы, название, ответ_верен in db.fetchall():
		try:
			x, y = положение
		except TypeError:
			μ, σ = 50.0, 15.0
			x = random.normalvariate(μ, σ)
			y = random.normalvariate(μ, σ)
		status = {
			None: 'open',
			True: 'solved',
			False: 'failed',
		}[ответ_верен]
		link = f'/problem/{вариант}/' if user_id is not None else f'/login?path=/town/{town}/'
		yield f'<a href="{link}" class="level level_{status}" transform="translate({x} {y})"><title>{название}</title>'
		yield f'<circle class="level-icon" r="0.65em" />'
		yield f'<text class="level-value">{баллы}</text>'
		yield f'</a>'
	yield '</svg>'
