#!/usr/bin/python3

import random
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
	print('<svg class="map" viewBox="0 0 100 100">')
	print(f'<image href="/static/map/town-{город}.jpg" width="100" height="100" />')
	cur.execute('select группа, положение, баллы from Группа where город = %s and exists(select 1 from Задача where Задача.группа = Группа.группа)', (город,))
	for группа, положение, баллы in cur.fetchall():
		try:
			x, y = положение
		except TypeError:
			μ, σ = 50.0, 15.0
			x = random.normalvariate(μ, σ)
			y = random.normalvariate(μ, σ)
		print(f'<a class="level" transform="translate({x} {y})" href="/problem/next.py?group={группа}">')
		print(f'<circle class="level-icon" r="0.65em" />')
		print(f'<text class="level-value">{баллы}</text>')
		print(f'</a>')
	print('</svg>')
	print('</main>')

try:
	import psycopg
	from psycopg.types.composite import CompositeInfo, register_composite

	город = int(query['id'])

	with psycopg.connect('postgres://kvantland:quant@127.0.0.1') as con:
		register_composite(CompositeInfo('point', 600, 1017, field_names=('x', 'y'), field_types=(701, 701)))
		with con.cursor() as cur:
			show_town(cur)
except Exception as e:
	print(f'<p>Exception of type <em>{escape(type(e).__name__)}</em> caught with message:</p>')
	print(f'<p>{escape(str(e))}</p>')

print(f'<p>{escape(str(query))}</p>')
