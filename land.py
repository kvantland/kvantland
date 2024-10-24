#!/usr/bin/python3

from config import config
from bottle import route, request, response
import json
import sys
from login import check_token

MODE = config['tournament']['mode']

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

def finished(db, user_id):
	if user_id == None:
		return False
	db.execute('select is_finished from Kvantland.Student where student=%s', (user_id, ))
	(finish, ), = db.fetchall()
	return finish


@route('/api/rules_crumbs')
def get_rules_breadcrumbs():
	rules_crumbs = [
		{   'name': "Квантландия",
            'link':  "/"},
        {   'name': "Правила",
            'link':  "/rules"},]
	return json.dumps(rules_crumbs)

@route('/api/rules_info')
def get_rules_info():
	rules_info = [
		{   
			'normal': """Игрок путешествует по стране Квантландия, оказываясь 
						в разных городах и областях и зарабатывает виртуальную валюту 
						«квантик» за решение задач соответствующей темы.""",
            'bold': "Цель игры — получить как можно больше квантиков."
		},

        {
			'normal': """В начале игры каждому дается 10 квантиков, которые можно 
		                тратить на подсказки к задачам. Для того чтобы получить задачу, нужно выбрать 
		                одну из монет в соответствующем городе или области (кликнуть на монету). 
		                На монете указывается количество квантиков, которое дается за ее правильное решение.""",
            'bold': "Есть задачи проще (1 или 2 квантика за решение) и сложнее (3, 4 или 5 квантиков за решение)."
		},

        {   
			'normal': """Можно свободно возвращаться к карте города или страны. Но если вы 
			            уже давали ответ на задачу, то задача становится неактивной и пройти ее 
						повторно нельзя.""",
            'bold': "Поэтому не торопитесь и внимательно проверяйте, прежде чем отправить ответ."
		},

        {   
			'normal': """Обратите внимание, что некоторые задачи интерактивны. В них требуется 
			            произвести действия, которые описаны в условии, чтобы получить нужный 
						результат.""",
            'bold': "Читайте условия внимательно!"
		},

        {   
			'normal': """Для решения задач вам понадобится компьютер и компьютерная мышь или 
			            ноутбук с тачпадом (не планшет), чтобы перетаскивать и выделять объекты.""",
            'bold': f"""Если возникла техническая проблема, то можно написать в техподдержку
			        <u><a href='mailto:{config['contacts']['support_email']}'>{config['contacts']['support_email']}</a></u>
					с описанием проблемы и скриншотом компьютера."""
		},
		
        {
			'normal': """Выберите время в любой день до окончания турнира, чтобы вас ничего не отвлекало. 
			            Итоги соревнования подводятся по числу квантиков, которое у вас на счету к концу 
						игры. Это число всегда отображается в вверху экрана по центру. Удачи!""",
        },

	]
	return json.dumps(rules_info)

@route('/api/land_crumbs')
def get_land_breadcrumbs():
	land_crumbs = [
		{   'name': "Квантландия",
            'link':  "/"},]
	return json.dumps(land_crumbs)

def get_user_id(db): 
	token_check_status = check_token(request)
	if token_check_status['error']:
		response.status = 400
		return json.dumps({'error': token_check_status['error']})
	else:
		user_login = token_check_status['login']
	try:
		db.execute('select student from Kvantland.Student where login=%s', (user_login, ))
	except:
		print("Login does not exist", file=sys.stderr)
	(user_id, ), = db.fetchall()
	return user_id

@route('/api/towns_info')
def get_towns_info(db):
	user_id = get_user_id(db)
	if user_id is not None:
		db.execute('select town, name, position, exists(select 1 from Kvantland.AvailableProblem join Kvantland.Variant using (variant) join Kvantland.Problem using (problem) where town = Kvantland.Town.town and student = %s and answer_given = false and tournament = %s) from Kvantland.Town', (user_id, config["tournament"]["version"]))
	else:
		db.execute('select town, name, position, true from Kvantland.Town')
	resp = []
	for town, name, (x, y), opened in db.fetchall():
		resp.append({"townID": town, "name": name, "x": x, "y": y, "opened": opened})
	return json.dumps(resp)
