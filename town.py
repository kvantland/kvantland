#!/usr/bin/python3

import random
from bottle import route, HTTPError

import user

@route('/town/<town:int>/')
def show_town(db, town):
	if (user_id := user.current_user()) == None:
		raise HTTPError(403)
	yield '<!DOCTYPE html>'
	db.execute('select название from Город where город = %s', (town,))
	(название, ), = db.fetchall()
	yield f'<title>{название}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield from user.display_banner(db)
	yield '<main class="map">'
	yield f'<h1>{название}</h1>'
	yield '<svg class="map" viewBox="0 0 100 100">'
	yield f'<image href="/static/map/town-{town}.jpg" width="100" height="100" />'
	db.execute('select вариант, положение, баллы, название, ответ is null открыта from ДоступнаяЗадача join Вариант using (вариант) join Задача using (задача) where город = %s and ученик = %s', (town, user_id))
	for вариант, положение, баллы, название, открыта in db.fetchall():
		try:
			x, y = положение
		except TypeError:
			μ, σ = 50.0, 15.0
			x = random.normalvariate(μ, σ)
			y = random.normalvariate(μ, σ)
		tag = 'a' if открыта else 'g'
		yield f'<{tag} href="/problem/{вариант}/" class="level" transform="translate({x} {y})"><title>{название}</title>'
		yield f'<circle class="level-icon" r="0.65em" />'
		yield f'<text class="level-value">{баллы}</text>'
		yield f'</{tag}>'
	yield '</svg>'
	yield '<div class="button_bar">'
	yield f'<a href="/"><button>К карте Квантландии</button></a>'
	yield '</div>'
	yield '</main>'
