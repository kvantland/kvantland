#!/usr/bin/python3

import psycopg2
import json
import os
from sys import stdin
from importlib import import_module
from urllib.parse import parse_qsl
from html import escape

data = stdin.read()
query = dict(parse_qsl(os.environ['QUERY_STRING']) + parse_qsl(data))

print('Content-Type: text/html; charset=utf-8')
print()
print('<!DOCTYPE html>')

def show_question(cur):
	cur.execute('select Тип.код, Задача.название, описание, содержание from Задача join Вариант using (задача) join Тип using (тип) where вариант = %s', (вариант,))
	(тип, название, описание, содержание), = cur.fetchall()
	typedesc = import_module(f'problem-types.{тип}')
	print(f'<title>{название}</title>')
	print(f'<h1>{название}</h1>')
	print(f'<p class="description">{описание}</p>')
	print('<form method="post">')
	print('<div class="answer_area">')
	typedesc.entry_form(содержание)
	print('</div>')
	print('<div class="button_bar">')
	print('<button type="submit">Отправить</button>')
	print('</div>')
	print('</form>')

def check_answer(cur):
	cur.execute('select Тип.код, Задача.название, описание, содержание from Задача join Вариант using (задача) join Тип using (тип) where вариант = %s', (вариант,))
	(тип, название, описание, содержание), = cur.fetchall()
	typedesc = import_module(f'problem-types.{тип}')
	print(f'<title>{название}</title>')
	print(f'<h1>{название}</h1>')
	print(f'<p class="description">{описание}</p>')
	print('<div class="result_area">')
	print(typedesc.validate(содержание, ответ))
	print('</div>')

try:
	вариант = int(query['id'])
	ответ = query.get('answer')

	with psycopg2.connect('postgres://kvantland:quant@127.0.0.1') as con:
		with con.cursor() as cur:
			if ответ is not None:
				check_answer(cur)
			else:
				show_question(cur)
except Exception as e:
	print(f'<p>Exception of type <em>{escape(type(e).__name__)}</em> caught with message:</p>')
	print(f'<p>{escape(str(e))}</p>')

print(f'<p>{escape(str(query))}</p>')
