#!/bin/python3

import math
import random
import base64
from pathlib import Path
import json
import psycopg

import os
import sys
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_path)
sys.path.append(project_root)
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


def IslandOfLiars4(cur):
	problems_list = []
	variants_list = dict()

	problems_list = add_problem_to_list(problems_list, cur, "Остров Лжецов", 3, 'integer', "Соседи лжецы")
	for N, A in [
			('12', 8),
			('15', 10),
			('18', 12),
			('21', 14),
			]:
			desc = f"""За круглым столом сидят {N} человек, каждый из которых либо рыцарь (всегда говорит правду), либо лжец (всегда лжёт). 
			Каждый из сидящих сказал, что хотя бы один его сосед – лжец. Какое наибольшее количество рыцарей может быть за столом?"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Соседи лжецы", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Остров Лжецов", 4, 'radio', "Трёхцветные колпаки")
	for a, b, c, A in [
			("«Я знаю, что на мне красный колпак»", "«А я так и не знаю, какого цвета на мне колпак»", "«А на мне точно жёлтый колпак».", 2),
			("«Я знаю, что на мне жёлтый колпак»", "«А я так и не знаю, какого цвета на мне колпак»", "«А на мне точно зелёный колпак»", 0),
			("«Я знаю, что на мне зелёный колпак»", "«А я так и не знаю, какого цвета на мне колпак»", "«А на мне точно красный колпак»", 1),
			("«Я знаю, что на мне зелёный колпак»", "«А я так и не знаю, какого цвета на мне колпак»", "«А на мне точно жёлтый колпак»", 0),
		]:
		desc = f"""Вам и шести вашим друзьям-математикам надели на голову по колпаку. Каждый из вас видит колпаки всех остальных друзей, но не видит свой. 
		Вам всем сообщили, что всего было по три красных, жёлтых и зелёных колпака, но два из них спрятали. Ваши друзья стали по очереди произносить следующие фразы:<br>
		Первый: «Я не знаю, какого цвета на мне колпак».<br>
		Второй: «Я тоже не знаю, какого цвета на мне колпак».<br>
		Третий: «И я не знаю, какого цвета на мне колпак».<br>
		Четвёртый: {a}.<br>
		Пятый: {b}.<br>
		Шестой: {c}.<br>
		Можете ли вы определить, какой колпак у вас на голове?"""
		cont = {
			'answers': [
				"Да, красный",
				"Да, жёлтый",
				"Да, зелёный",
				"Не могу",
			],
			'correct': A,
		}
		variants_list = add_variant_to_list(variants_list, "Трёхцветные колпаки", desc, json.dumps(cont))

	add_list(problems_list, variants_list)


def Chiselburg4(cur):
	problems_list = []
	variants_list = dict()
	problems_list = add_problem_to_list(problems_list, cur, "Чиселбург", 1, 'lock_code', "Код замка")
	for combinations, correct in [
		([512, 317, 587], [3, 8, 2]),
		([748, 142, 762], [1, 6, 8]),
		([294, 796, 256], [7, 5, 4]),
		([149, 546, 136], [5, 3, 9]),
		]:
		desc = f"""Код замка состоит из трёх цифр. Петя попытался 
				его подобрать и попробовал комбинации {combinations[0]}, {combinations[1]}, 
				{combinations[2]}. Оказалось, что в каждом варианте он верно набрал ровно 
				одну цифру. Какой код у замка?"""
		cont = {
			'correct': correct,
			'start_values': ['*', '*', '*'],
			'componentType': 'lockCode',
			'inputType': 'InteractiveTypeInput',
		}
		variants_list = add_variant_to_list(variants_list, "Код замка", desc, json.dumps(cont))

	problems_list = add_problem_to_list(problems_list, cur, "Чиселбург", 3, 'unusual_number', "Необычное число")
	for X, Y, A in [
			(6, 9, 53999),
			(9, 3, 49999),
			(15, 9, 23999),
			(18, 3, 29999),
			]:
		desc = f"""Напишите пятизначное число, у которого первая цифра в {X} раз меньше суммы всех цифр справа от неё, а вторая цифра в {Y} раз меньше суммы всех цифр справа от неё."""
		cont = {
				'inputType': "InteractiveTypeInput",
				'componentType': "unusualNumber",
				'fieldsAmount': 5,
				'correct': A,
		}
		variants_list = add_variant_to_list(variants_list, "Необычное число", desc, json.dumps(cont))	

	add_list(problems_list, variants_list)

def Geom4(cur):
	problems_list = []
	variants_list = dict()
	
	problems_list = add_problem_to_list(problems_list, cur, "Геома", 2, 'partition_restore', "Восстановите разбиение")
	for start_board, correct in [
		(
			[
				[ 8, '', '', '', ''],
				[ 6,  8, '', '',  8],
				['', '',  8, '', ''],
				[ 4, '', '', '',  6],
				['',  8,  8,  6, '']
			],
			[[
				[1, 1, 1, 2, 2],
				[3, 4, 4, 5, 2],
				[3, 4, 5, 5, 6],
				[7, 8, 9, 9, 6],
				[8, 8, 9, 0, 0]
			]]
   		),
		(
			[
				[ 6, '',  8, '', ''],
				[ 6, '', '', '', ''],
				['',  4, '', '',  8],
				['', '',  4,  6, ''],
				['',  8, '', '',  8]
			],
			[[
				[1, 1, 2, 3, 3],
				[4, 2, 2, 3, 3],
				[4, 5, 6, 6, 6],
				[7, 7, 8, 9, 9],
				[7, 7, 0, 0, 0]
			]]
		),
		(
			[
				['', '',  8,  6, ''],
				[ 4, '', '',  8, ''],
				['',  8, '', '', ''],
				[ 6, '', '', '',  6],
				['',  8,  6, '',  8]
			],
			[[
				[1, 1, 1, 2, 2],
				[3, 4, 4, 5, 5],
				[6, 4, 4, 5, 0],
				[6, 7, 8, 9, 0],
				[7, 7, 8, 9, 9]
			]]
		),
		(
			[
				['', '', '', '',  4],
				[ 8, '',  8, '', ''],
				['', '',  8,  6,  6],
				[ 4, '', '', '',  8],
				['',  6,  8, '', '']
			],
			[[
				[1, 1, 2, 2, 3],
				[1, 1, 2, 4, 5],
				[6, 6, 6, 4, 5],
				[7, 8, 8, 9, 9],
				[0, 0, 8, 9, 9]
			]]
		)
	]:
		desc = '''Квадрат 5×5 разбили на 10 фигурок и в одной из клеток каждой фигуры 
				записали её периметр. Восстановите разбиение. Используйте 10 цветов справа 
				в произвольном порядке, чтобы выделить клетки разных фигур. '''
		cont = {
			'start_board': start_board,
			'inputType': "InteractiveTypeInput",
			'componentType': "partitionRestore",
			'correct': correct,
		}
		variants_list = add_variant_to_list(variants_list, "Восстановите разбиение", desc, json.dumps(cont))

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

def Golovolomsk4(cur):
	problems_list = []
	variants_list = dict()
	
	problems_list = add_problem_to_list(problems_list, cur, "Головоломск", 2, 'lamps_on_hexagonal_panel', "Лампочки на шестиугольном табло")
	for lamps_in_line, side in [    
		(2, 5),
	]:
		desc = f'''На табло расположены лампочки в форме «шестиугольника». Каждое нажатие 
				на лампочку меняет её состояние (включает или выключает). Включите несколько 
				лампочек так, чтобы в каждом ряду, параллельном стороне «шестиугольника», 
				{['горела одна лампочка', 'горели две лампочки', 'горели три лампочки'][lamps_in_line - 1]}.'''
		cont = {
			'lamps_in_line': lamps_in_line,
			'side': side,
			'inputType': "InteractiveTypeInput",
			'componentType': "lampsOnHexagonalPanel"
		}
		variants_list = add_variant_to_list(variants_list, "Лампочки на шестиугольном табло", desc, json.dumps(cont))

	add_list(problems_list, variants_list)

def CombiRepublic4(cur):
	problems_list = []
	variants_list = dict()

	problems_list = add_problem_to_list(problems_list, cur, "Республика Комби", 2, 'integer', "Числа без палиндромов")
	for N, A in [
			('111', 6),
			('222', 6),
			('333', 6),
			('123', 6),
			]:
			desc = f"""Сколько существует {N}-значных чисел, в записи которых участвуют только цифры 1, 2, 3 и которые не содержат палиндромов длины более 1?"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Числа без палиндромов", desc, json.dumps(cont))	
			

	problems_list = add_problem_to_list(problems_list, cur, "Республика Комби", 4, 'rearranged_weights', "Переставленные гирьки")
	for changed_weights in [
			[1, 2],
			[3, 4],
			[6, 7],
			[8, 9]
			]:
			desc = """На столе были выставлены в ряд внешне одинаковые гирьки 
					весом 101 г, 102 г, …, 110 г. Кто-то поменял местами две соседние гирьки. 
					За два взвешивания определите, какие именно гирьки были переставлены."""
			cont = {
				'weightings_amount': 2,
				'correct': changed_weights,
				'componentType': "rearrangedWeights",
				'inputType': "InteractiveTypeInput",
			}
			variants_list = add_variant_to_list(variants_list, "Переставленные гирьки", desc, json.dumps(cont))	

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
			IslandOfLiars4(cur)
			Chiselburg4(cur)
			Geom4(cur)
			Golovolomsk4(cur)
			CombiRepublic4(cur)
			update_positions(cur)
