#!/usr/bin/python3

from bottle import route, request, redirect, HTTPError
from importlib import import_module
from pathlib import Path

import user

result_text = {
	True: 'Верно!',
	False: 'Неверно',
}

def try_read_file(path):
	path = Path(__file__).parent / path
	try:
		with open(path, 'r') as f:
			return f.read()
	except OSError:
		return None

def show_question(db, variant):
	db.execute('select город, Тип.код, Задача.название, описание, содержание from Задача join Вариант using (задача) join Тип using (тип) where вариант = %s', (variant,))
	(город, тип, название, описание, содержание), = db.fetchall()
	typedesc = import_module(f'problem-types.{тип}')
	script = try_read_file(f'problem-types/{тип}.js')
	yield '<!DOCTYPE html>'
	yield f'<title>{название}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<script type="module" src="/static/master.js"></script>'
	if script:
		yield f'<script type="text/ecmascript" defer>{script}</script>'
	yield from user.display_banner(db)
	yield '<main>'
	yield f'<h1>{название}</h1>'
	yield f'<p class="description">{описание}</p>'
	yield '<form method="post">'
	yield f'<div class="answer_area answer_area_{тип}">'
	yield from typedesc.entry_form(содержание)
	yield '</div>'
	yield '<div class="button_bar">'
	yield '<button type="submit">Отправить</button>'
	yield f'<a href="/town/{город}/"><button type="button">Вернуться в город</button></a>'
	yield '</div>'
	yield '</form>'
	yield '</main>'

def check_answer(db, var_id, answer):
	db.execute('select Тип.код, содержание from Задача join Вариант using (задача) join Тип using (тип) where вариант = %s', (var_id,))
	(тип, содержание), = db.fetchall()
	typedesc = import_module(f'problem-types.{тип}')
	return typedesc.validate(содержание, answer)

def _display_result(db, var_id, ok):
	db.execute('select город, название, описание from Задача join Вариант using (задача) where вариант = %s', (var_id,))
	(город, название, описание), = db.fetchall()

	yield '<!DOCTYPE html>'
	yield f'<title>{название}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield from user.display_banner(db)
	yield '<main>'
	yield f'<h1>{название}</h1>'
	yield f'<p class="description">{описание}</p>'
	yield f'<div class="result_area result_{ok}">'
	yield result_text[ok]
	yield '</div>'
	yield '<div class="button_bar">'
	yield f'<a href="/town/{город}/"><button type="button">Вернуться в город</button></a>'
	yield '</div>'
	yield '</main>'

def has_current_problem(db, user):
	db.execute('select exists(select 1 from ТекущаяЗадача where ученик = %s)', (user, ))
	(has, ), = db.fetchall()
	return has

@route('/problem/<var_id:int>/')
def problem_show(db, var_id):
	if (user_id := user.current_user()) == None:
		raise HTTPError(403, 'Требуется вход')
	db.execute('select ответ_верен from ДоступнаяЗадача where вариант = %s and ученик = %s', (var_id, user_id))
	try:
		(is_answer_correct, ), = db.fetchall()
	except ValueError:
		raise HTTPError(403, 'Задача недоступна')
	if is_answer_correct is not None:
		return _display_result(db, var_id, is_answer_correct)
	return show_question(db, var_id)

@route('/problem/<var_id:int>/', method='POST')
def problem_answer(db, var_id):
	if (user_id := user.current_user()) == None:
		raise HTTPError(403, 'Требуется вход')
	db.execute('select ответ_верен from ДоступнаяЗадача where вариант = %s and ученик = %s', (var_id, user_id))
	try:
		(is_answer_correct, ), = db.fetchall()
	except ValueError:
		raise HTTPError(403, 'Задача недоступна')
	if is_answer_correct is not None:
		redirect('')

	answer = request.forms.answer
	is_answer_correct = check_answer(db, var_id, answer)
	db.execute('update ДоступнаяЗадача set ответ_верен=%s where вариант = %s and ученик = %s', (is_answer_correct, var_id, user_id))
	if is_answer_correct:
		db.execute('update Ученик set счёт=счёт + (select баллы from Вариант join Задача using (задача) where вариант = %s) where ученик = %s', (var_id, user_id))
	yield from _display_result(db, var_id, is_answer_correct)
