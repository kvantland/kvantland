#!/usr/bin/python3

from bottle import route, request, redirect, HTTPError
from enum import Enum, auto
from importlib import import_module
from pathlib import Path
import psycopg

import nav
import user

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
		with open(path, 'r') as f:
			return f.read()
	except OSError:
		return None

def show_submit_button(**kwargs):
	yield '<button type="submit" form="problem_form">Отправить</button>'

def show_hint_button(*, hint_mode: HintMode, стоимость_подсказки: int, **kwargs):
	if hint_mode == HintMode.AFFORDABLE:
		yield f'<form action="hint" method="post" class="hint"><button type="submit" title="Получить подсказку (стоимость: {стоимость_подсказки})">Подсказка</button></form>'
	elif hint_mode == HintMode.TOO_EXPENSIVE:
		yield f'<button type="button" disabled title="Недостаточно квантиков (стоимость: {стоимость_подсказки})">Подсказка</button>'

def show_buttons(**kwargs):
	yield from show_submit_button(**kwargs)
	yield from show_hint_button(**kwargs)

def show_question(db, variant, hint_mode):
	db.execute('select город, Город.название, Тип.код, Задача.название, описание, содержание, Подсказка.текст, Подсказка.стоимость from Задача join Вариант using (задача) join Тип using (тип) join Город using (город) left join Подсказка using (задача) where вариант = %s', (variant,))
	(город, название_города, тип, название, описание, содержание, подсказка, стоимость_подсказки), = db.fetchall()
	kwargs = {'hint_mode': hint_mode, 'стоимость_подсказки': стоимость_подсказки}
	typedesc = import_module(f'problem-types.{тип}')
	script = try_read_file(f'problem-types/{тип}.js')
	style = try_read_file(f'problem-types/{тип}.css')
	yield '<!DOCTYPE html>'
	yield f'<title>{название}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<script type="module" src="/static/master.js"></script>'
	if script:
		yield f'<script type="text/ecmascript">{script}</script>'
	if style:
		yield f'<style type="text/css">{style}</style>'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield from nav.display_breadcrumbs(('/', 'Квантландия'), (f'/town/{город}/', название_города))
	yield '<main>'
	yield f'<h1>{название}</h1>'
	yield f'<p class="description">{описание}</p>'
	if hint_mode == HintMode.SHOW:
		yield '<section class="hint">'
		yield '<h2>Подсказка</h2>'
		yield f'<p>{подсказка}</p>'
		yield '</section>'
	yield f'<form method="post" id="problem_form" class="problem answer_area answer_area_{тип}">'
	yield from typedesc.entry_form(содержание, kwargs)
	yield '</form>'
	try:
		show_default_buttons = not typedesc.CUSTOM_BUTTONS
	except AttributeError:
		show_default_buttons = True
	if show_default_buttons:
		yield '<div class="button_bar">'
		yield from show_buttons(**kwargs)
		yield '</div>'
	yield '</main>'
	yield '</div>'

def check_answer(db, var_id, answer):
	db.execute('select Тип.код, содержание from Задача join Вариант using (задача) join Тип using (тип) where вариант = %s', (var_id,))
	(тип, содержание), = db.fetchall()
	typedesc = import_module(f'problem-types.{тип}')
	return typedesc.validate(содержание, answer)

def _display_result(db, var_id, ok):
	db.execute('select город, Город.название, Задача.название, описание from Задача join Вариант using (задача) join Город using (город) where вариант = %s', (var_id,))
	(город, название_города, название, описание), = db.fetchall()

	yield '<!DOCTYPE html>'
	yield f'<title>{название}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<div class="content_wrapper">'
	yield from user.display_banner(db)
	yield from nav.display_breadcrumbs(('/', 'Квантландия'), (f'/town/{город}/', название_города))
	yield '<main>'
	yield f'<h1>{название}</h1>'
	yield f'<p class="description">{описание}</p>'
	yield f'<div class="result_area result_{ok}">'
	yield result_text[ok]
	yield '</div>'
	yield '</main>'
	yield '</div>'

def require_user():
	if (user_id := user.current_user()) == None:
		raise HTTPError(403, 'Требуется вход')
	return user_id

def has_current_problem(db, user):
	db.execute('select exists(select 1 from ТекущаяЗадача where ученик = %s)', (user, ))
	(has, ), = db.fetchall()
	return has

def get_past_answer_correctness(db, user_id, var_id):
	db.execute('select ответ_верен from ДоступнаяЗадача where вариант = %s and ученик = %s', (var_id, user_id))
	try:
		(is_answer_correct, ), = db.fetchall()
	except ValueError:
		raise HTTPError(403, 'Задача недоступна')
	return is_answer_correct

@route('/problem/<var_id:int>/')
def problem_show(db, var_id):
	user_id = require_user()
	is_answer_correct = get_past_answer_correctness(db, user_id, var_id)
	if is_answer_correct is not None:
		return _display_result(db, var_id, is_answer_correct)

	db.execute('select подсказка_взята from ДоступнаяЗадача where вариант = %s and ученик = %s', (var_id, user_id))
	(hinted, ), = db.fetchall()
	if hinted:
		hint_mode = HintMode.SHOW
	else:
		db.execute('select счёт >= стоимость from Подсказка join Вариант using (задача), Ученик where вариант = %s and ученик = %s', (var_id, user_id))
		try:
			(can_afford_hint, ), =db.fetchall()
			hint_mode = HintMode.AFFORDABLE if can_afford_hint else HintMode.TOO_EXPENSIVE
		except ValueError:
			hint_mode = HintMode.NONE
	return show_question(db, var_id, hint_mode)

@route('/problem/<var_id:int>/', method='POST')
def problem_answer(db, var_id):
	user_id = require_user()
	is_answer_correct = get_past_answer_correctness(db, user_id, var_id)
	if is_answer_correct is not None:
		redirect('')

	answer = request.forms.answer
	is_answer_correct = check_answer(db, var_id, answer)
	db.execute('update ДоступнаяЗадача set ответ_верен=%s where вариант = %s and ученик = %s', (is_answer_correct, var_id, user_id))
	if is_answer_correct:
		db.execute('update Ученик set счёт=счёт + (select баллы from Вариант join Задача using (задача) where вариант = %s) where ученик = %s', (var_id, user_id))
	yield from _display_result(db, var_id, is_answer_correct)


def _request_hint(db, var_id):
	user_id = require_user()
	is_answer_correct = get_past_answer_correctness(db, user_id, var_id)
	if is_answer_correct is not None:
		return

	db.execute('select подсказка_взята from ДоступнаяЗадача where вариант = %s and ученик = %s', (var_id, user_id))
	(hinted, ), = db.fetchall()
	if hinted:
		return

	db.execute('update ДоступнаяЗадача set подсказка_взята=true where вариант = %s and ученик = %s', (var_id, user_id))
	try:
		db.execute('update Ученик set счёт=счёт - (select стоимость from Подсказка join Вариант using (задача) where вариант = %s) where ученик = %s', (var_id, user_id))
	except psycopg.errors.CheckViolation:
		pass

@route('/problem/<var_id:int>/hint', method='POST')
def problem_request_hint(db, var_id):
	_request_hint(db, var_id)
	redirect('.')
