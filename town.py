#!/usr/bin/python3

from bottle import route

import random

@route('/town/<town:int>/')
def show_town(db, town):
	yield '<!DOCTYPE html>'
	db.execute('select название from Город where город = %s', (town,))
	(название, ), = db.fetchall()
	yield f'<title>{название}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<main>'
	yield f'<h1>{название}</h1>'
	yield '<svg class="map" viewBox="0 0 100 100">'
	yield f'<image href="/static/map/town-{town}.jpg" width="100" height="100" />'
	db.execute('select группа, положение, баллы from Группа where город = %s and exists(select 1 from Задача where Задача.группа = Группа.группа)', (town,))
	for группа, положение, баллы in db.fetchall():
		try:
			x, y = положение
		except TypeError:
			μ, σ = 50.0, 15.0
			x = random.normalvariate(μ, σ)
			y = random.normalvariate(μ, σ)
		yield f'<a class="level" transform="translate({x} {y})" href="/problem/next?group={группа}">'
		yield f'<circle class="level-icon" r="0.65em" />'
		yield f'<text class="level-value">{баллы}</text>'
		yield f'</a>'
	yield '</svg>'
	yield '<div class="button_bar">'
	yield f'<a href="/"><button>К карте Квантландии</button></a>'
	yield '</div>'
	yield '</main>'
