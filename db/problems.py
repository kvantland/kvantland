#!/bin/python3

import math
import random
import base64
import os
import sys
from pathlib import Path
import json
import psycopg
import sys
sys.path.insert(1, '../')
from config import config
random.seed(1337)

def read_file(name):
	with open(Path(__file__).parent / name, 'rb') as f:
		return f.read()

def get_type_id(cur, type_):
	cur.execute("select type_ from Kvantland.Type_ where code = %s", (type_, ))
	if rows := cur.fetchall():
		return rows[0][0]
	cur.execute("insert into Kvantland.Type_ (code) values (%s) returning type_", (type_, ))
	if rows := cur.fetchall():
		return rows[0][0]
	raise Exception(f"Couldnt add type_ {type_}")

def get_town_id(cur, name):
	cur.execute("select town from Kvantland.Town where name = %s", (name, ))
	(town,), = cur.fetchall()
	return town

def cmp(item):
	return item['points']

def add_problem_to_list(problems_list, cur, town, points, type_, name, hint=None, hint_cost=None, image=None):
	problems_list.append({
		'cur': cur,
		'town': town,
		'points': points,
		'type': type_,
		'name': name,
		'hint': hint,
		'hint_cost': hint_cost,
		'image': image
		})
	return problems_list

def add_variant_to_list(variants_list, name, description, content):
	try:
		variants_list[name]
		variants_list[name]['description'].append(description)
		variants_list[name]['content'].append(content)
	except KeyError:
		variants_list[name] = dict()
		variants_list[name]['description'] = [description]
		variants_list[name]['content'] = [content]
	return variants_list

def add_list(problems_list, variants_list):
	problems_list.sort(key=cmp)
	for problem in problems_list:
		cur = problem['cur']
		town = problem['town']
		points = problem['points']
		type_ = problem['type']
		name = problem['name']
		hint = problem['hint']
		hint_cost = problem['hint_cost']
		image = problem['image']
		problem = add_problem(cur, town, points, type_, name, hint, hint_cost, image)

		for i in range(len(variants_list[name]['description'])):
			description = variants_list[name]['description'][i]
			content = variants_list[name]['content'][i]
			add_variant(cur, problem, description, content)

def add_problem(cur, town, points, type_, name, hint=None, hint_cost=None, image=None, tournament=config["tournament"]["version"]):
	type_ = get_type_id(cur, type_)
	town = get_town_id(cur, town)
	name = f"{name}"
	cur.execute("insert into Kvantland.Problem (town, points, name, type_, image, tournament) values (%s, %s, %s, %s, %s, %s) returning problem", (town, points, name, type_, image, tournament))
	(problem,), = cur.fetchall()
	if hint:
		if not hint_cost:
			hint_cost = 1
		cur.execute("insert into Kvantland.Hint (problem, content, cost) values (%s, %s, %s)", (problem, hint, hint_cost))
	return problem


def add_variant(cur, problem, description, content):
	cur.execute("insert into Kvantland.Variant (problem, description, content) values (%s, %s, %s) returning variant", (problem, description, content))
	(variant,), = cur.fetchall()
	return variant


def IslandOfLiars3(cur):
	problems_list = []
	variants_list = dict()
	
	add_list(problems_list, variants_list)


def Chiselburg3(cur):
	problems_list = []
	variants_list = dict()

	add_list(problems_list, variants_list)

def Geom3(cur):
	problems_list = []
	variants_list = dict()
	
	add_list(problems_list, variants_list)


def make_chess_board(data):
	def format_cell(cell):
		if cell in {None, '', ' ', ' '}:
			return ''
		return f'<span class="label">{cell}</span>'
	return '<table class="grid chess">{0}</table>'.format(''.join(
			'<tr>{0}</tr>'.format(''.join(
			'<td>{0}</td>'.format(format_cell(cell))
			for cell in row)) for row in data))

def Golovolomsk3(cur):
	problems_list = []
	variants_list = dict()

	add_list(problems_list, variants_list)

def CombiRepublic3(cur):
	problems_list = []
	variants_list = dict()

	add_list(problems_list, variants_list)


def update_positions_town(cur, town, problem_count):
	x0 = 1280 / 2
	y0 = 720 / 2
	R = 250
	base = 0.25
	cur.execute("select problem from Kvantland.Problem where town = %s and tournament = %s", (town, config["tournament"]["version"]))
	if (problem_count == 1):
		(problem, ), = cur.fetchall()
		cur.execute("update Kvantland.Problem set position = point(%s, %s) where problem = %s", (x0, y0, problem))
	else:
		for k, (problem, ) in enumerate(cur.fetchall()):
			phi = 2 * math.pi * ((k // 2 + k % 2) / problem_count + base)
			if k % 2 == 1:
				x, y = x0 + R * math.cos(phi), y0 - R * math.sin(phi)
			else:
				x, y = x0 - R * math.cos(phi), y0 - R * math.sin(phi)
			cur.execute("update Kvantland.Problem set position = point(%s, %s) where problem = %s", (x, y, problem))

def update_positions(cur):
	cur.execute("select town, count(*) from Kvantland.Problem join Kvantland.Town using (town) where tournament = %s group by town", (config["tournament"]["version"],))
	for town, problem_count in cur.fetchall():
		update_positions_town(cur, town, problem_count)


db = 'postgres://kvantland:quant@127.0.0.1'
if len(sys.argv) > 1:
	db = sys.argv[1]
with psycopg.connect(db) as con:
	with con.transaction():
		with con.cursor() as cur:
			IslandOfLiars3(cur)
			Chiselburg3(cur)
			Geom3(cur)
			Golovolomsk3(cur)
			CombiRepublic3(cur)
			update_positions(cur)
