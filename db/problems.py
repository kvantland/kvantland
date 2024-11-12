#!/bin/python3

import math
from pathlib import Path
import json
import psycopg

import os
import sys
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_path)
sys.path.append(project_root)
from config import config

current_tournament = config['tournament']['version']
current_problem_num = 1


class Town:
	problems = []

	def __init__(self, name=''):
		self.name = name
		self.id = self.get_town_id(name)
	
	def get_town_id(self, name):
		cur.execute("select town from Kvantland.Town where name = %s", (name, ))
		(town,), = cur.fetchall()
		return town
	
	def add_problem(self, problem):
		global current_problem_num, current_tournament
		cur.execute("insert into Kvantland.Problem (town, points, name, type_, image, tournament) values (%s, %s, %s, %s, %s, %s) returning problem", 
			(self.id, problem.points, problem.name, problem.type_id, problem.image, current_tournament))
		(problem.id, ), = cur.fetchall()
		if problem.hint:
			cur.execute("insert into Kvantland.Hint (problem, content, cost) values (%s, %s, %s)", (problem.id, problem.hint, problem.hint_cost))
		for variant in problem.variants:
			try:
				description = variant['description']
			except:
				description = ''
			variant_num = current_tournament * 1000 + current_problem_num
			cur.execute("insert into Kvantland.Variant (variant, problem, description, content) overriding system value values (%s, %s, %s, %s)", (variant_num, problem.id, description, json.dumps(variant['content'])))	
			current_problem_num += 1

	def add_problems(self, problem_list):
		for problem in problem_list:
			self.add_problem(problem)


class Problem:
	
	def __init__(self, name='', points=0, type_='', hint=None, hint_cost=None, image=None):
		self.name = name
		self.points = points
		self.type_ = type_
		self.hint = hint
		if hint_cost:
			self.hint_cost = hint_cost
		else:
			self.hint_cost = 1
		self.image = image
		self.type_id = self.get_type_id(type_)
		self.variants = []
		self.id = None

	def get_type_id(self, type_):
		cur.execute("select type_ from Kvantland.Type_ where code = %s", (type_, ))
		if rows := cur.fetchall():
			return rows[0][0]
		cur.execute("insert into Kvantland.Type_ (code) values (%s) returning type_", (type_, ))
		if rows := cur.fetchall():
			return rows[0][0]
		raise Exception(f"Couldnt add type_ {type_}")
		
	def add_variant(self, variant):
		self.variants.append(variant)
	
		
def read_file(name):
	with open(Path(__file__).parent / name, 'rb') as f:
		return f.read()
	

def Liars_Island():
	global cur
	current_town = Town('Остров Лжецов')

	problem_1 = Problem(
		name="Мёд в сотах",
		points=3,
		type_='honey_in_honeycombs'
	)

	for honeycombsConfig in [
		[
			['', 2, '', ''],
			[2, '', '', 4, ''],
			['', '', '', '', ''],
			[2, '', '', 3, '', ''],
			['', 4, '', '', 2],
			['', 1, 1, '']
		],
		[
			['', '', 2, ''],
			['', 2, '', '', ''],
			['', '', 2, '', 3],
			['', 4, '', '', '', ''],
			['', '', 1, 4, ''],
			['', '', '', '']
		]
	]:
		problem_1.add_variant({
			'content': {
				'amount': 12,
				'honeycombsConfig': honeycombsConfig,
				'componentType': "honeyInHoneycombs",
				'inputType': "InteractiveTypeInput",
			}
		})

	current_town.add_problems([problem_1, ])
	

def Chiselburg():
	global cur
	current_town = Town('Чиселбург')
	problem_1 = Problem(
		name='Хитрая таблица',
		points=3,
		type_='tricky_table',
	)
	for number_value in [36, 98, 50, 28]:
		problem_1.add_variant({
			'content': {
				'inputType': "InteractiveTypeInput",
				'componentType': "trickyTable",
				'numberValue': number_value,
			}
		})
	current_town.add_problems([problem_1])


def Geoma():
	global cur
	current_town = Town('Геома')

	problem_1 = Problem(
		name="Созвездие 'Квадрат'",
		points=2,
		type_='constellation_Square'
	)
	for map in [
		[
			'..S..S',
			'.S.S..',
			'.....S',
			'.S...S',
			'..S...',
			'S..SS.'
		],
		[
			'..S..S',
			'.S....',
			'S...S.',
			'..S..S',
			'..S...',
			'S..SS.'
		],
		[
			'..S...',
			'..S...',
			'S.S.S.',
			'S...SS',
			'......',
			'S.S.S.'
		],
		[
			'..SS..',
			'......',
			'.SS..S',
			'S....S',
			'.S.S..',
			'S...S.'
		]
	]:
		problem_1.add_variant({
			'content': {
				'componentType': "constellationSquare",
				'inputType': "InteractiveTypeInput",
				'skyMap': map
			}
		})
	
	problem_2 = Problem(
		name="Периметр пятиугольника",
		points=2,
		type_='integer',
		image='perimeter_of_pentagon.svg'
	)
	problem_2.add_variant({
		'content': {
			'correct': 25,
		},
		'description': """Пятиугольник, стороны которого равны, разрезали по 
				диагоналям на несколько фигур (см. рисунок). Сумма периметров белых 
				фигур на 5 см больше суммы периметров чёрных фигур. Чему равен 
				периметр пятиугольника?"""

	})

	problem_3 = Problem(
		name="Кубики с рисунками",
		points=1,
		type_="cubes_with_images"
	)
	for cube_list in [
		[1, 2, 3, 4, 5],
		[2, 3, 4, 5, 1],
		[3, 4, 5, 1, 2],
		[4, 5, 1, 2, 3]
	]:
		problem_3.add_variant({
			'content': {
				'cubeList': cube_list,
				'componentType': "cubesWithImages",
				'inputType': "InteractiveTypeInput",
				'correct': 1,
			}
	})

	current_town.add_problems([problem_1, problem_2, problem_3])


def Golovolomsk():
	global cur
	current_town = Town('Головоломск')

	problem_1 = Problem(
		name="Суперсудоку",
		points=3,
		type_="supersudoky",
	)
	for plot, start_numbers in [
		[
			[
			[0, 0, 0, 1, 1, 1],
			[0, 2, 0, 1, 1, 1],
			[2, 2, 0, 3, 3, 3],
			[2, 2, 2, 4, 3, 3],
			[5, 5, 5, 4, 3, 4],
			[5, 5, 5, 4, 4, 4]
			],
			[
			[4, 3, 0, 0, 0, 1],
			[0, 5, 0, 2, 3, 4],
			[0, 2, 0, 0, 0, 0],
			[0, 0, 0, 0, 5, 0],
			[2, 4, 3, 0, 1, 0],
			[5, 0, 0, 0, 2, 3]
			],
		],
		[
			[
			[0, 1, 1, 1, 1, 1],
			[0, 2, 2, 2, 2, 1],
			[0, 0, 0, 2, 2, 3],
			[0, 4, 4, 3, 3, 3],
			[5, 4, 4, 4, 4, 3],
			[5, 5, 5, 5, 5, 3]
			],
			[
			[6, 0, 0, 2, 0, 5],
			[0, 0, 0, 3, 0, 0],
			[3, 5, 0, 0, 0, 0],
			[0, 0, 0, 0, 6, 4],
			[0, 0, 1, 0, 0, 0],
			[5, 0, 6, 0, 0, 2]
			],
		],
		[
			[
			[0, 0, 0, 1, 1, 2],
			[0, 0, 1, 1, 2, 2],
			[0, 1, 1, 2, 2, 2],
			[6, 6, 6, 5, 5, 4],
			[6, 6, 5, 5, 4, 4],
			[6, 5, 5, 4, 4, 4]
			],
			[
			[1, 2, 6, 0, 0, 4],
			[0, 0, 1, 0, 0, 3],
			[0, 0, 0, 0, 6, 1],
			[5, 3, 0, 0, 0, 0],
			[6, 0, 0, 4, 0, 0],
			[2, 0, 0, 1, 4, 5]
			],
		],
		[
			[
			[0, 0, 0, 1, 1, 1],
			[0, 0, 0, 1, 2, 1],
			[3, 3, 2, 2, 2, 1],
			[5, 3, 3, 3, 2, 2],
			[5, 3, 5, 4, 4, 4],
			[5, 5, 5, 4, 4, 4]
			],
			[
			[5, 2, 1, 0, 0, 0],
			[4, 0, 0, 5, 0, 1],
			[0, 0, 4, 0, 0, 0],
			[0, 0, 0, 4, 0, 0],
			[6, 0, 5, 0, 0, 4],
			[0, 0, 0, 1, 6, 5]
			],
		],
	]:
		problem_1.add_variant({
			'content': {
				'plot': plot,
				'start_numbers': start_numbers,
				'componentType': "supersudoky",
				'inputType': "InteractiveTypeInput"
			},
		})
	
	problem_2 = Problem(
		name="Фермер и петушок",
		points=2,
		type_="farmer_and_cockerel"
	)
	
	for board_width, board_height in [
		(8, 10),
		(8, 12),
		(10, 10),
		(10, 12)
	]:
		problem_2.add_variant({
		'content': {
			'board_width': board_width,
			'board_height': board_height,
			'remaining_moves': 50,
			'turn': None,
			'farmer_coordinates': [board_height - 1, 0],
			'cockerel_coordinates': [0, board_width - 1],
			'componentType': "farmerAndCockerel",
			'inputType': "InteractiveTypeInput"
		}
	})
	current_town.add_problems([problem_1, problem_2, ])


def Kombi():
	global cur
	current_town = Town('Республика Комби')

	problem_1 = Problem(
		name='Расстояние между фальшивыми',
		points=4,
		type_="distanse_between_fake"
	)

	for position_1,  position_2 in [
		(0, 1),
		(1, 3),
		(2, 4),
		(0, 4)
	]:
		problem_1.add_variant({
			'content': {
				'weightings_amount': 2,
				'correct': {'position_1': position_1, 'position_2': position_2},
				'componentType': "distanseBetweenFake",
				'inputType': "IntegerTypeInput"
			}
		})

	problem_2 = Problem(
		name="Шахматные фигуры",
		type_="chess_figures",
		points=3
	)

	for positions in [
		[[1, 5], [2, 7]],
		[[3, 2], [5, 4]],
		[[1, 5], [5, 4]],
		[[2, 7], [3, 2]]
	]:
		problem_2.add_variant({
			'content': {
				'positions': positions,
				'componentType': "chessFigures",
				'inputType': "InteractiveTypeInput"
			}
		})
	
	current_town.add_problems([problem_1, problem_2])


def update_positions_town(cur, town, problem_count):
	x0 = 1280 / 2
	y0 = 720 / 2
	R = 250
	base = 0.25
	cur.execute("select problem from Kvantland.Problem where town = %s and tournament = %s order by points", (town, current_tournament))
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

def update_positions():
	global cur
	cur.execute("select town, count(*) from Kvantland.Problem join Kvantland.Town using (town) where tournament = %s group by town", (current_tournament,))
	for town, problem_count in cur.fetchall():
		update_positions_town(cur, town, problem_count)


db = 'postgres://kvantland:quant@127.0.0.1'
if len(sys.argv) > 1:
	db = sys.argv[1]
with psycopg.connect(db) as con:
	with con.transaction():
		with con.cursor() as cur:
			Liars_Island()
			Golovolomsk()
			Geoma()
			Chiselburg()
			Kombi()
			update_positions()
