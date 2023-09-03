#!/usr/bin/python3

from bottle import route

import user

@route('/')
def show_land(db):
	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	yield f'<title>Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield from user.display_banner(db)
	yield '<main>'
	yield f'<h1 class="title">Квантландия</h1>'
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

@route('/rules')
def show_land(db):
	yield '<!DOCTYPE html>'
	yield '<html lang="ru">'  # TODO поместить в общий шаблон
	yield f'<title>Правила — Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield from user.display_banner(db)
	yield '<main class="rules">'
	yield '<h1>Правила</h1>'
	yield '<p>Игрок путешествует по стране Квантландия, оказываясь в разных городах и областях (Головоломск, Остров Лжецов, Республика Комби, Чиселбург, Геома) и зарабатывает виртуальную валюту «квантик» за решение задач соответствующей темы: Головоломки, Логика, Комбинаторика, Арифметика, Геометрия. Цель игры — получить как можно больше квантиков.'
	yield '<p>В начале игры каждому дается 10 квантиков, которые можно тратить на подсказки к задачам (стоимость каждой подсказки 1 квантик). Для того, чтобы получить задачу, нужно выбрать одну из монет в соответствующем городе или области (кликнуть на монету). На монете указывается количество квантиков, которые даются за её правильное решение. Есть задачи проще (2 квантика за решение) и сложнее (4 квантика за решение).'
	yield '<p>Можно свободно возвращаться к карте города или страны. Но если вы уже давали ответ на задачу, то задача становится неактивной и пройти её повторно нельзя. Поэтому не торопитесь и внимательно проверяйте, прежде чем отправить ответ.'
	yield '<p>Обратите внимание, что некоторые задачи интерактивны. В них требуется произвести действия, которые описаны в условии, чтобы получить нужный результат. Читайте условия внимательно!'
	yield '<p>На Турнир вам даётся 90 минут. Оставшееся время отображается на таймере в углу экрана. Итоги соревнования подводятся по числу квантиков, которые у вас на счету к концу игры. Это число всегда отображается в правом верхнем углу экрана. Удачи!'
	yield '</main>'
