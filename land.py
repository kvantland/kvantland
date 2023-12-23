#!/usr/bin/python3

from config import config
from bottle import route, redirect

import nav
import user

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

def tournament_completed(db, user_id):
	not_completed = False
	if user_id is not None:
		db.execute('select town, exists(select 1 from Kvantland.AvailableProblem join Kvantland.Variant using (variant) join Kvantland.Problem using (problem) where town = Kvantland.Town.town and student = %s and answer_given = false) from Kvantland.Town', (user_id, ))
	else:
		db.execute('select town, true from Kvantland.Town')
	for town, opened in db.fetchall():
		if opened:
			not_completed = True
	return not not_completed

def finished(db, user_id):
	if user_id == None:
		return False
	db.execute('select is_finished from Kvantland.Student where student=%s', (user_id, ))
	(finish, ), = db.fetchall()
	return finish

@route('/')
def show_land(db):
	user_id = user.current_user(db)
	if finished(db, user_id):
		redirect("/final_page")
	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	yield f'<title>Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield f'<h1 class="title">Квантландия</h1>'
	yield '</div>'
	yield '<svg class="map" version="1.1" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield f'<image href="/static/map/land.png" width="1280" height="720" preserveAspectRatio="xMinYMin meet" />'
	if tournament_completed(db, user_id):
		yield '<a transform="translate(640 0)" href="/final_page">' 
		yield '<text class="town-name to_results" font-size="2em" text-anchor="middle" y="2em"> Завершить турнир </text>'
		yield '</a>'
	if user_id is not None:
		db.execute('select town, name, position, exists(select 1 from Kvantland.AvailableProblem join Kvantland.Variant using (variant) join Kvantland.Problem using (problem) where town = Kvantland.Town.town and student = %s and answer_given = false) from Kvantland.Town', (user_id, ))
	else:
		db.execute('select town, name, position, true from Kvantland.Town')
	for town, name, (x, y), opened in db.fetchall():
		clazz = "town"
		if not opened:
			clazz += " town_completed"
		yield f'<a class="{clazz}" transform="translate({x} {y})" xlink:href="/town/{town}/">'
		yield f'<circle class="town-icon" r="30px" fill="rgba(0, 0, 0, 0)" stroke="currentColor" stroke-width="0.2em" />'
		yield f'<text class="town-name" text-anchor="middle" y="60px">{name}</text>'
		yield f'</a>'
	yield '</svg>'
	yield '<div class="contacts_block">'
	yield '<h2 class="contacts_header"> Контакты: </h2>'
	yield f'<p class="contact"> Техническая поддержка: <a href="mailto:{config["contacts"]["support_email"]}">{config["contacts"]["support_email"]}</a> </p>'
	yield '</div>'
	yield '<script type="module" src="/static/results.js"></script>'

@route('/rules')
def show_land(db):
	user_id = user.current_user(db)
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
	yield '<p>В начале игры каждому дается 10 квантиков, которые можно тратить на подсказки к задачам (стоимость каждой подсказки 1 квантик). Для того, чтобы получить задачу, нужно выбрать одну из монет в соответствующем townе или области (кликнуть на монету). На монете указывается количество квантиков, которые даются за её правильное решение. Есть задачи проще (1 или 2 квантика за решение) и сложнее (3 или 4 квантика за решение).'
	yield '<p>Можно свободно возвращаться к карте города или страны. Но если вы уже давали ответ на задачу, то задача становится неактивной и пройти её повторно нельзя. Поэтому не торопитесь и внимательно проверяйте, прежде чем отправить ответ.'
	yield f'<p>Обратите внимание, что некоторые задачи интерактивны. В них требуется произвести действия, которые описаны в условии, чтобы получить нужный результат. Читайте условия внимательно! Для решения задач вам понадобится компьютер и компьютерная мышь или ноутбук с тачпадом (не планшет), чтобы перетаскивать и выделять объекты. Если возникла техническая проблема, то можно написать в техподдержку <a href="mailto:{config["contacts"]["support_email"]}">{config["contacts"]["support_email"]}</a> с описанием проблемы и скриншотом компьютера.'
	yield '<p>Выберите время в течение месяца, чтобы вас ничего не отвлекало. Итоги соревнования подводятся по числу квантиков, которые у вас на счету к концу игры. Это число всегда отображается в правом верхнем углу экрана. Удачи!'
	yield '</main>'
	yield '</div>'

@route('/final_page')
def show_result(db):
	user_id = user.current_user(db)
	db.execute('update Kvantland.Student set is_finished=true where student=%s', (user_id, ))
	db.execute('select score from Kvantland.Student where student= %s', (user_id, ))
	(score, ), = db.fetchall()
	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	yield f'<title>Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield '</div>'
	yield '<svg class="map final_result_area" version="1.1" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield f'<image href="/static/map/land.jpg" width="1280" height="720" preserveAspectRatio="xMinYMin meet" />'
	yield '<text text-anchor="middle" x="640" y="4em"> Поздравляем! </text>'
	yield '<text text-anchor="middle" x="640" y="6em"> Вы успешно завершили турнир. </text>'
	yield f'<text text-anchor="middle" x="640" y="8em"> Ваш результат составляет {score} {lang_form(score)}. </text>'
	yield '</svg>'