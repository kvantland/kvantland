#!/usr/bin/python3
import sys 

from bottle import route, request, redirect, HTTPError, response
import json
from enum import Enum, auto
from importlib import import_module
from pathlib import Path
import psycopg
from answer_area import show_answer_area

import nav
import user

from config import config

_key = config['keys']['cookie']

result_text = {
	True: 'Верно!',
	False: 'Неверно',
}

class HintMode(Enum):
	NONE = auto()
	SHOW = auto()
	AFFORDABLE = auto()
	TOO_EXPENSIVE = auto()

def try_read_file(path):
	path = Path(__file__).parent / path
	try:
		with open(path, 'r',encoding="utf-8") as f:
			return f.read()
	except OSError:
		return None

def show_submit_button(**kwargs):
	yield '<button id="send" type="submit" form="problem_form">Отправить</button>'

def show_hint_button(*, hint_mode: HintMode, hint_cost: int, **kwargs):
	if hint_mode == HintMode.AFFORDABLE:
		yield f'<form id="hint" action="hint" method="post" class="hint"><button form="hint" type="submit" title="Получить подсказку (стоимость: {hint_cost})">Подсказка</button></form>'
	elif hint_mode == HintMode.TOO_EXPENSIVE:
		yield f'<button type="button" disabled title="Недостаточно квантиков (стоимость: {hint_cost})">Подсказка</button>'

def show_buttons(**kwargs):
	yield from show_submit_button(**kwargs)
	yield from show_hint_button(**kwargs)

def show_question(db, variant, hint_mode):
	user_id = require_user(db)
	if user_id == None:
		redirect('/')
	db.execute('select town, Kvantland.Town.name, Kvantland.Type_.code, Kvantland.Problem.name, description, image, Kvantland.Variant.content, Kvantland.Hint.content, Kvantland.Hint.cost from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) join Kvantland.Town using (town) left join Kvantland.Hint using (problem) where variant = %s', (variant,))
	(town, town_name, type_, name, description, image, content, hint, hint_cost), = db.fetchall()
	db.execute('select xhr_amount from Kvantland.AvailableProblem where variant = %s and student = %s', (variant, user_id))
	(step, ), = db.fetchall()
	kwargs = {'hint_mode': hint_mode, 'hint_cost': hint_cost, 'step': step}
	typedesc = import_module(f'problem-types.{type_}')
	script = try_read_file(f'problem-types/{type_}.js')
	style = try_read_file(f'problem-types/{type_}.css')
	yield '<!DOCTYPE html>'
	yield f'<title>{name}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<script type="module" src="/static/master.js"></script>'
	if style:
		yield f'<style type="text/css">{style}</style>'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield from nav.display_breadcrumbs(('/', 'Квантландия'), (f'/town/{town}/', town_name))
	yield '<main>'
	yield f'<h1>{name}</h1>'
	yield f'<p class="description">{description}</p>'
	if hint_mode == HintMode.SHOW:
		yield '<section class="hint">'
		yield '<h2>Подсказка</h2>'
		yield f'<p>{hint}</p>'
		yield '</section>'
	try:
		save_progress = typedesc.SAVE_PROGRESS
	except AttributeError:
		save_progress = True

	try:
		show_default_buttons = not typedesc.CUSTOM_BUTTONS
	except AttributeError:
		show_default_buttons = True

	try:
		hybrid = typedesc.HYBRID
	except AttributeError:
		hybrid = False

	try:
		without_buttons = typedesc.WITHOUT_BUTTONS
	except AttributeError:
		without_buttons = False
		
	if save_progress:
		if hybrid:
			yield f'<div id="interactive_problem_form">'
		else:
			yield f'<form method="post" id="problem_form" class="problem answer_area answer_area_{type_}">'
	yield from typedesc.entry_form(content, kwargs)
	if save_progress and not hybrid:
		yield '</form>'
	elif hybrid:
		yield '</div>'

	if image:
		yield f'<img class="picture" src="/static/problem/{image}">'
	
	if not without_buttons:
		if show_default_buttons:
			yield from show_answer_area(content, 'without_input', kwargs)
		else:
			yield from show_answer_area(content, 'with_input', kwargs)
	
	yield '</main>'
	yield '</div>'
	yield '<script type="text/ecmascript" src="/static/save_hint_results.js"></script>'
	if script:
		yield f'<script type="text/ecmascript">{script}</script>'

def check_answer(db, var_id, answer):
	db.execute('select Kvantland.Type_.code, content from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (var_id,))
	(type_, content), = db.fetchall()
	typedesc = import_module(f'problem-types.{type_}')
	return typedesc.validate(content, answer)

def _display_result(db, var_id, ok, answer=None, solution=None):
	db.execute('select Kvantland.Type_.code from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (var_id,))
	(type_, ), = db.fetchall()
	db.execute('select town, Kvantland.Town.name, Kvantland.Problem.name, description, image from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Town using (town) where variant = %s', (var_id,))
	(town, town_name, name, description, image), = db.fetchall()
	
	typedesc = import_module(f'problem-types.{type_}')
	style = try_read_file(f'problem-types/{type_}.css')

	try:
		show_default_buttons = not typedesc.CUSTOM_BUTTONS
	except AttributeError:
		show_default_buttons = True

	try:
		save_progress = typedesc.SAVE_PROGRESS
	except AttributeError:
		save_progress = True

	yield '<!DOCTYPE html>'
	yield f'<title>{name}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	if style:
		yield f'<style type="text/css">{style}</style>'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield from nav.display_breadcrumbs(('/', 'Квантландия'), (f'/town/{town}/', town_name))
	yield '<main>'
	yield f'<h1>{name}</h1>'
	yield f'<p class="description">{description}</p>'
	yield '<div class="save_zone_wrapper" style="z-index: -1">'
	if save_progress:
		yield solution
	if not show_default_buttons:
		yield '<div class="answer_bar">'
		yield 'Введите ответ:'
		yield f'<input name="answer" type="number" value="{answer}" readonly/>'
		yield '</div>'
	yield '</div>'
	yield f'<div class="result_area result_{ok}">'
	yield result_text[ok]
	yield '</div>'
	if image:
		yield f'<img class="picture" src="/static/problem/{image}">'
	yield '</main>'
	yield '</div>'

def require_user(db):
	user_id = user.current_user(db)
	return user_id

def has_current_problem(db, user):
	db.execute('select exists(select 1 from Kvantland.CurrentProblem where student = %s)', (user, ))
	(has, ), = db.fetchall()
	return has

def get_past_answer_correctness(db, user_id, var_id):
	db.execute('select answer_true from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
	try:
		(is_answer_correct, ), = db.fetchall()
	except ValueError:
		return None
	return is_answer_correct

@route('/problem/<var_id:int>/')
def problem_show(db, var_id):
	user_id = require_user(db)
	if user_id == None:
		redirect('/')
	is_answer_correct = get_past_answer_correctness(db, user_id, var_id)
	if is_answer_correct is not None:
		db.execute('select answer, solution from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
		(answer, solution, ), = db.fetchall()
		print(answer, solution, file=sys.stderr)
		return _display_result(db, var_id, is_answer_correct, answer, solution)

	db.execute('select hint_taken from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
	(hinted, ), = db.fetchall()
	if hinted:
		hint_mode = HintMode.SHOW
	else:
		db.execute('select score >= cost from Kvantland.Hint join Kvantland.Variant using (problem), Kvantland.Student where variant = %s and student = %s', (var_id, user_id))
		try:
			(can_afford_hint, ), =db.fetchall()
			hint_mode = HintMode.AFFORDABLE if can_afford_hint else HintMode.TOO_EXPENSIVE
		except ValueError:
			hint_mode = HintMode.NONE
	return show_question(db, var_id, hint_mode)

@route('/problem/<var_id:int>/', method='POST')
def problem_answer(db, var_id):
	db.execute('select Kvantland.Type_.code from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (var_id,))
	type_ = db.fetchall()[0][0]
	
	user_id = require_user(db)
	if user_id == None:
		redirect('/')
	is_answer_correct = get_past_answer_correctness(db, user_id, var_id)
	if is_answer_correct is not None:
		redirect('')

	answer = request.forms.answer
	solution = request.forms.progress

	typedesc = import_module(f'problem-types.{type_}')

	try:
		save_progress = typedesc.SAVE_PROGRESS
	except AttributeError:
		save_progress = True

	is_answer_correct = check_answer(db, var_id, answer)
	if save_progress:
		db.execute('update Kvantland.AvailableProblem set answer_true=%s, solution=%s, answer=%s where variant = %s and student = %s', (is_answer_correct, solution, answer, var_id, user_id))
	else:
		db.execute('update Kvantland.AvailableProblem set answer_true=%s, answer=%s where variant = %s and student = %s', (is_answer_correct, answer, var_id, user_id))
	if is_answer_correct:
		db.execute('update Kvantland.Student set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s', (var_id, user_id))
	
	yield from _display_result(db, var_id, is_answer_correct, answer, solution)


def _request_hint(db, var_id):
	user_id = require_user(db)
	if user_id == None:
		redirect('/')
	is_answer_correct = get_past_answer_correctness(db, user_id, var_id)
	if is_answer_correct is not None:
		return

	db.execute('select hint_taken from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
	(hinted, ), = db.fetchall()
	if hinted:
		return

	db.execute('update Kvantland.AvailableProblem set hint_taken=true where variant = %s and student = %s', (var_id, user_id))
	try:
		db.execute('update Kvantland.Student set score=score - (select cost from Kvantland.Hint join Kvantland.Variant using (problem) where variant = %s) where student = %s', (var_id, user_id))
	except psycopg.errors.CheckViolation:
		pass

@route('/problem/<var_id:int>/hint', method='POST')
def problem_request_hint(db, var_id):
	_request_hint(db, var_id)
	redirect('.')

@route('/problem/<var_id:int>/xhr', method='GET')
def xhr_req(db, var_id):
	user_id = require_user(db)
	if user_id == None:
		redirect('/')
	db.execute('update Kvantland.AvailableProblem set xhr_amount = xhr_amount + 1 where variant = %s and student = %s returning xhr_amount', (var_id, user_id))
	(xhr_amount, ), = db.fetchall()
	db.execute('select Kvantland.Type_.code from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (var_id,))
	(type_, ), = db.fetchall()
	db.execute('select content from Kvantland.Variant where variant = %s', (var_id,))
	(cont, ), = db.fetchall()
	params = request.query
	typedesc = import_module(f'problem-types.{type_}')
	resp = typedesc.steps(xhr_amount, params, cont)
	try: 
		db.execute('update Kvantland.Variant set content = %s where variant = %s', (json.dumps(resp['data_update']), var_id,))
	except KeyError:
		pass
	return resp['answer']