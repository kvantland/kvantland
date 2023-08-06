#!/usr/bin/python3

from bottle import route

import user

@route('/')
def show_land(db):
	yield '<!DOCTYPE html>'
	yield f'<title>Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield from user.display_banner(db)
	yield '<main>'
	yield f'<h1>Квантландия</h1>'
	yield '<svg class="map" viewBox="0 0 100 100">'
	yield f'<image href="/static/map/land.jpg" width="100" height="100" />'
	db.execute('select город, название, положение from Город')
	for город, название, (x, y) in db.fetchall():
		yield f'<a class="town" transform="translate({x} {y})" href="/town/{город}/">'
		yield f'<circle class="town-icon" r="0.3em" fill="none" stroke="currentColor" stroke-width="0.2em" />'
		yield f'<text class="town-name" text-anchor="middle" y="1.2em">{название}</text>'
		yield f'</a>'
	yield '</svg>'
	yield '</main>'
