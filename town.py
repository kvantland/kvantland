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
	db.execute('select задача, положение, баллы, название, ученик is null открыта from Задача left join (select * from ЗакрытиеЗадачи where ученик = %s) Закрытие using (задача) where город = %s', (1, town))
	for задача, положение, баллы, название, открыта in db.fetchall():
		try:
			x, y = положение
		except TypeError:
			μ, σ = 50.0, 15.0
			x = random.normalvariate(μ, σ)
			y = random.normalvariate(μ, σ)
		tag = 'a' if открыта else 'g'
		yield f'<{tag} href="/problem/next?problem={задача}" class="level" transform="translate({x} {y})"><title>{название}</title>'
		yield f'<circle class="level-icon" r="0.65em" />'
		yield f'<text class="level-value">{баллы}</text>'
		yield f'</{tag}>'
	yield '</svg>'
	yield '<div class="button_bar">'
	yield f'<a href="/"><button>К карте Квантландии</button></a>'
	yield '</div>'
	yield '</main>'
