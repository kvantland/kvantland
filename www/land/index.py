#!/usr/bin/python3

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

def show_land(cur):
	cur.execute('select город, название, положение from Город')
	print(f'<title>Квантландия</title>')
	print('<link rel="stylesheet" type="text/css" href="/static/master.css">')
	print('<main>')
	print(f'<h1>Квантландия</h1>')
	print('<svg class="map" viewBox="0 0 100 100">')
	print(f'<image href="/static/map/land.jpg" width="100" height="100" />')
	for город, название, (x, y) in cur.fetchall():
		print(f'<a class="town" transform="translate({x} {y})" href="/town/index.py?id={город}">')
		print(f'<circle class="town-icon" r="0.3em" fill="none" stroke="currentColor" stroke-width="0.2em" />')
		print(f'<text class="town-name" text-anchor="middle" y="1.2em">{название}</text>')
		print(f'</a>')
	print('</svg>')
	print('</main>')

try:
	import psycopg
	from psycopg.types.composite import CompositeInfo, register_composite

	with psycopg.connect('postgres://kvantland:quant@127.0.0.1') as con:
		register_composite(CompositeInfo('point', 600, 1017, field_names=('x', 'y'), field_types=(701, 701)))
		with con.cursor() as cur:
			show_land(cur)
except Exception as e:
	print(f'<p>Exception of type <em>{escape(type(e).__name__)}</em> caught with message:</p>')
	print(f'<p>{escape(str(e))}</p>')

print(f'<p>{escape(str(query))}</p>')
