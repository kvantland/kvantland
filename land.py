#!/usr/bin/python3

from config import config
from bottle import route, redirect, response

import nav
import user

def do_logout():
	response.set_cookie('user', '', path='/', max_age=0, httponly=True, samesite='lax')

def lang_form(score):
	if score % 100 >= 10 and score % 100 < 20:
		return 'квантиков'
	else:
		if score % 10 in [2, 3, 4]:
			return 'квантика'
		elif score % 10 == 1:
			return 'квантик'
		else:
			return 'квантиков'

@route('/')
def show_land(db):
	do_logout()
	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	yield f'<title>Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from user.display_banner()
	yield f'<h1 class="title">Квантландия</h1>'
	yield '</div>'
	yield '<svg class="map" version="1.1" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield f'<image href="/static/map/land.jpg" width="1280" height="720" preserveAspectRatio="xMinYMin meet" />'

	db.execute('select город, название, положение, true from Город')
	for город, название, (x, y), открыт in db.fetchall():
		clazz = "town"
		yield f'<a class="{clazz}" transform="translate({x} {y})" xlink:href="/town/{город}/">'
		yield f'<circle class="town-icon" r="0.3em" fill="rgba(0, 0, 0, 0)" stroke="currentColor" stroke-width="0.2em" />'
		yield f'<text class="town-name" text-anchor="middle" y="1.2em">{название}</text>'
		yield f'</a>'
	yield '</svg>'
	yield '<div class="contacts_block">'
	yield '<h2 class="contacts_header"> Контакты: </h2>'
	yield f'<p class="contact"> Техническая поддержка: <a href="mailto:{config["contacts"]["support_email"]}">{config["contacts"]["support_email"]}</a> </p>'
	yield '</div>'
	yield '<script type="module" src="/static/results.js"></script>'

@route('/rules')
def show_land():
	do_logout()
	yield '<!DOCTYPE html>'
	yield '<html lang="ru">'  # TODO поместить в общий шаблон
	yield f'<title>Правила — Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from user.display_banner()
	yield from nav.display_breadcrumbs(('/', 'Квантландия'))
	yield '<main class="rules">'
	yield '<h1>Правила</h1>'
	yield '<p>Игрок путешествует по стране Квантландия, оказываясь в разных городах и областях (Головоломск, Остров Лжецов, Республика Комби, Чиселбург, Геома) и зарабатывает виртуальную валюту «квантик» за решение задач соответствующей темы: Головоломки, Логика, Комбинаторика, Арифметика, Геометрия. Цель игры — получить как можно больше квантиков.'
	yield '<p>В начале игры каждому дается 10 квантиков, которые можно тратить на подсказки к задачам (стоимость каждой подсказки 1 квантик). Для того, чтобы получить задачу, нужно выбрать одну из монет в соответствующем городе или области (кликнуть на монету). На монете указывается количество квантиков, которые даются за её правильное решение. Есть задачи проще (1 или 2 квантика за решение) и сложнее (3 или 4 квантика за решение).'
	yield '<p>Можно свободно возвращаться к карте города или страны. Но если вы уже давали ответ на задачу, то задача становится неактивной и пройти её повторно нельзя. Поэтому не торопитесь и внимательно проверяйте, прежде чем отправить ответ.'
	yield f'<p>Обратите внимание, что некоторые задачи интерактивны. В них требуется произвести действия, которые описаны в условии, чтобы получить нужный результат. Читайте условия внимательно! Для решения задач вам понадобится компьютер и компьютерная мышь или ноутбук с тачпадом (не планшет), чтобы перетаскивать и выделять объекты. Если возникла техническая проблема, то можно написать в техподдержку <a href="mailto:{config["contacts"]["support_email"]}">{config["contacts"]["support_email"]}</a> с описанием проблемы и скриншотом компьютера.'
	yield '<p>Выберите время в течение месяца, чтобы вас ничего не отвлекало. Итоги соревнования подводятся по числу квантиков, которые у вас на счету к концу игры. Это число всегда отображается в правом верхнем углу экрана. Удачи!'
	yield '</main>'
	yield '</div>'