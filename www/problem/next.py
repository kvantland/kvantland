#!/usr/bin/python3

import psycopg2
import json
import os
import sys
import io
from importlib import import_module
from urllib.parse import parse_qsl
from html import escape

out = sys.stdout
headers = {}
body = io.StringIO()
sys.stdout = body

headers['Content-Type'] = 'text/plain; charset=utf-8'

data = sys.stdin.read()
query = dict(parse_qsl(os.environ['QUERY_STRING']) + parse_qsl(data))

def next_problem(cur):
	cur.execute('select задача from Задача where группа = %s and видимость order by random() limit 1', (группа,))
	задачи = cur.fetchall()
	if not задачи:
		print('Задач не найдено!')
		return
	(задача, ), = задачи

	cur.execute('select вариант from Вариант where задача = %s order by random() limit 1', (задача,))
	варианты = cur.fetchall()
	if not варианты:
		print('Вариантов не найдено!')
		return
	(вариант, ), = варианты

	headers['Status'] = 303
	headers['Location'] = f'index.py?id={вариант}'

try:
	группа = int(query['group'])

	with psycopg2.connect('postgres://kvantland:quant@127.0.0.1') as con:
		with con.cursor() as cur:
			next_problem(cur)
except Exception as e:
	headers['Content-Type'] = 'text/plain; charset=utf-8'
	print(f'Exception of type {type(e).__name__} caught with message:')
	print(e)

print(query)

for header, value in headers.items():
	out.write(f'{header}: {value}\n')
out.write('\n')
out.write(body.getvalue())
