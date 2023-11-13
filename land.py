#!/usr/bin/python3

from bottle import route

import nav
import user

@route('/')
def show_land(db):
	user_id = user.current_user()

	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	yield f'<title>Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield f'<h1 class="title">Квантландия</h1>'
	yield '</div>'
	yield '<svg class="map" viewBox="0 0 1280 720">'
	yield f'<image href="/static/map/land.jpg" width="1280" height="720" preserveAspectRatio="xMinYMin meet" />'
	if user_id is not None:
		db.execute('select город, название, положение, exists(select 1 from ДоступнаяЗадача join Вариант using (вариант) join Задача using (задача) where город = Город.город and ученик = %s and ответ_дан = false) from Город', (user_id, ))
	else:
		db.execute('select город, название, положение, true from Город')
	for город, название, (x, y), открыт in db.fetchall():
		clazz = "town"
		if not открыт:
			clazz += " town_completed"
		yield f'<a class="{clazz}" transform="translate({x} {y})" href="/town/{город}/">'
		yield f'<circle class="town-icon" r="0.3em" fill="rgba(0, 0, 0, 0)" stroke="currentColor" stroke-width="0.2em" />'
		yield f'<text class="town-name" text-anchor="middle" y="1.2em">{название}</text>'
		yield f'</a>'
	yield '</svg>'

@route('/rules')
def show_land(db):
	yield '<!DOCTYPE html>'
	yield '<html lang="ru">'  # TODO поместить в общий шаблон
	yield f'<title>Правила — Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield from nav.display_breadcrumbs(('/', 'Квантландия'))
	yield '<main class="rules">'
	yield '<h1>Правила</h1>'
	yield '<p>Игрок путешествует по стране Квантландия, оказываясь в разных городах и областях (Головоломск, Остров Лжецов, Республика Комби, Чиселбург, Геома) и зарабатывает виртуальную валюту «квантик» за решение задач соответствующей темы: Головоломки, Логика, Комбинаторика, Арифметика, Геометрия. Цель игры — получить как можно больше квантиков.'
	yield '<p>В начале игры каждому дается 10 квантиков, которые можно тратить на подсказки к задачам (стоимость каждой подсказки 1 квантик). Для того, чтобы получить задачу, нужно выбрать одну из монет в соответствующем городе или области (кликнуть на монету). На монете указывается количество квантиков, которые даются за её правильное решение. Есть задачи проще (1 или 2 квантика за решение) и сложнее (3 или 4 квантика за решение).'
	yield '<p>Можно свободно возвращаться к карте города или страны. Но если вы уже давали ответ на задачу, то задача становится неактивной и пройти её повторно нельзя. Поэтому не торопитесь и внимательно проверяйте, прежде чем отправить ответ.'
	yield '<p>Обратите внимание, что некоторые задачи интерактивны. В них требуется произвести действия, которые описаны в условии, чтобы получить нужный результат. Читайте условия внимательно!'
	yield '<p>На Турнир вам даётся 90 минут. Оставшееся время отображается на таймере в углу экрана. Итоги соревнования подводятся по числу квантиков, которые у вас на счету к концу игры. Это число всегда отображается в правом верхнем углу экрана. Удачи!'
	yield '</main>'
	yield '</div>'
