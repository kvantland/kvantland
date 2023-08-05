#!/usr/bin/python3

from bottle import route, request, redirect

import psycopg2
import json
import os
from sys import stdin
from importlib import import_module
from urllib.parse import parse_qsl
from html import escape

result_text = {
	True: 'Верно!',
	False: 'Неверно',
}

@route('/problem/<variant:int>/')
def show_question(db, variant):
	db.execute('select Тип.код, Задача.название, описание, содержание from Задача join Вариант using (задача) join Тип using (тип) where вариант = %s', (variant,))
	(тип, название, описание, содержание), = db.fetchall()
	typedesc = import_module(f'problem-types.{тип}')
	yield '<!DOCTYPE html>'
	yield f'<title>{название}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<main>'
	yield f'<h1>{название}</h1>'
	yield f'<p class="description">{описание}</p>'
	yield '<form method="post">'
	yield f'<div class="answer_area answer_area_{тип}">'
	yield from typedesc.entry_form(содержание)
	yield '</div>'
	yield '<div class="button_bar">'
	yield '<button type="submit">Отправить</button>'
	yield '</div>'
	yield '</form>'
	yield '</main>'

@route('/problem/<variant:int>/', method='POST')
def check_answer(db, variant):
	db.execute('select город, Тип.код, Задача.название, описание, содержание from Задача join Вариант using (задача) join Тип using (тип) where вариант = %s', (variant,))
	(город, тип, название, описание, содержание), = db.fetchall()
	typedesc = import_module(f'problem-types.{тип}')

	ответ = request.forms.answer
	ok = typedesc.validate(содержание, ответ)

	yield '<!DOCTYPE html>'
	yield f'<title>{название}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
	yield '<main>'
	yield f'<h1>{название}</h1>'
	yield f'<p class="description">{описание}</p>'
	yield f'<div class="result_area result_{ok}">'
	yield result_text[ok]
	yield '</div>'
	yield '<div class="button_bar">'
	yield f'<a href="/town/{город}/"><button>Вернуться в город</button></a>'
	yield '</div>'
	yield '</main>'

@route('/problem/next')
def next_problem(db):
	ученик = 1  # FIXME
	задача = int(request.query.problem)

	db.execute('select вариант from Вариант where задача = %s order by random() limit 1', (задача,))
	варианты = db.fetchall()
	if not варианты:
		yield 'Вариантов не найдено!'
		return
	(вариант, ), = варианты

	db.execute('insert into ЗакрытиеЗадачи (ученик, задача) values (%s, %s)', (ученик, задача))

	redirect(f'{вариант}/')
