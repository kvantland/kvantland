#!/bin/python3

import math
import random
import base64
import os
import sys
from pathlib import Path
import json
import psycopg

random.seed(1337)

def read_file(name):
	with open(Path(__file__).parent / name, 'rb') as f:
		return f.read()

def get_type_id(cur, type_):
	cur.execute("select тип from Тип where код = %s", (type_, ))
	if rows := cur.fetchall():
		return rows[0][0]
	cur.execute("insert into Тип (код) values (%s) returning тип", (type_, ))
	if rows := cur.fetchall():
		return rows[0][0]
	raise Exception(f"Не удалось добавить тип {type_}")

def get_town_id(cur, name):
	cur.execute("select город from Город where название = %s", (name, ))
	(town,), = cur.fetchall()
	return town

def lang_form(score):
	if score % 100 >= 10 and score % 100 < 20:
		return 'квантиков'
	else:
		if score % 10 in [2, 3, 4]:
			return 'квантика'
		elif score % 10 == 1:
			return 'квантик'
		else:
			return 'квантиков'

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

def add_problem(cur, town, points, type_, name, hint=None, hint_cost=None, image=None):
	type_ = get_type_id(cur, type_)
	town = get_town_id(cur, town)
	name = f"{name} ({points} {lang_form(points)})"
	cur.execute("insert into Задача (город, баллы, название, тип, изображение) values (%s, %s, %s, %s, %s) returning задача", (town, points, name, type_, image))
	(problem,), = cur.fetchall()
	if hint:
		if not hint_cost:
			hint_cost = 1
		cur.execute("insert into Подсказка (задача, текст, стоимость) values (%s, %s, %s)", (problem, hint, hint_cost))
	return problem


def add_variant(cur, problem, description, content):
	cur.execute("insert into Вариант (задача, описание, содержание) values (%s, %s, %s) returning вариант", (problem, description, content))
	(variant,), = cur.fetchall()
	return variant


def IslandOfLiars2(cur):
	problems_list = []
	variants_list = dict()
	
	add_list(problems_list, variants_list)


def Chiselburg2(cur):
	problems_list = []
	variants_list = dict()
	
	add_list(problems_list, variants_list)

def Geom2(cur):
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


def Golovolomsk2(cur):
	problems_list = []
	variants_list = dict()

	add_list(problems_list, variants_list)

def CombiRepublic2(cur):
	problems_list = []
	variants_list = dict()

	add_list(problems_list, variants_list)


def update_positions_town(cur, town, problem_count):
	x0 = 1280 / 2
	y0 = 720 / 2
	R = 250
	base = 0.25
	y0 += 0.5 * R * (1 - math.cos(math.pi / problem_count))
	cur.execute("select задача from Задача where город = %s", (town,))
	for k, (problem, ) in enumerate(cur.fetchall()):
		phi = 2 * math.pi * ((k // 2 + k % 2) / problem_count + base)
		if k % 2 == 1:
			x, y = x0 + R * math.cos(phi), y0 - R * math.sin(phi)
		else:
			x, y = x0 - R * math.cos(phi), y0 - R * math.sin(phi)
		cur.execute("update Задача set положение = point(%s, %s) where задача = %s", (x, y, problem))

def update_positions(cur):
	cur.execute("select город, count(*) from Задача join Город using (город) group by город")
	for town, problem_count in cur.fetchall():
		update_positions_town(cur, town, problem_count)


db = 'postgres://kvantland:quant@127.0.0.1'
if len(sys.argv) > 1:
	db = sys.argv[1]
with psycopg.connect(db) as con:
	with con.transaction():
		with con.cursor() as cur:
			IslandOfLiars2(cur)
			Chiselburg2(cur)
			Geom2(cur)
			Golovolomsk2(cur)
			CombiRepublic2(cur)
			update_positions(cur)
