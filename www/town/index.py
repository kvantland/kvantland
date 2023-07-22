#!/usr/bin/python3

import json
import os
from sys import stdin
from urllib.parse import parse_qsl
from html import escape

data = stdin.read()
query = dict(parse_qsl(os.environ['QUERY_STRING']) + parse_qsl(data))

print('Content-Type: text/html; charset=utf-8')
print()
print('<!DOCTYPE html>')

def show_town(cur):
	cur.execute('select название from Город where город = %s', (город,))
	(название, ), = cur.fetchall()
	print(f'<title>{название}</title>')
	print('<link rel="stylesheet" type="text/css" href="/static/master.css">')
	print('<main>')
	print(f'<h1>{название}</h1>')
	cur.execute('select группа, положение, баллы from Группа where город = %s', (город,))
	for группа, положение, баллы in cur.fetchall():
		# TODO: положение
		print(f'<a href="/problem/next.py?group={группа}">{баллы}</a>')
	print('</main>')

try:
	import psycopg

	город = int(query['id'])

	with psycopg.connect('postgres://kvantland:quant@127.0.0.1') as con:
		with con.cursor() as cur:
			show_town(cur)
except Exception as e:
	print(f'<p>Exception of type <em>{escape(type(e).__name__)}</em> caught with message:</p>')
	print(f'<p>{escape(str(e))}</p>')

print(f'<p>{escape(str(query))}</p>')
