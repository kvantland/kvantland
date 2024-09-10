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
			cur.execute("insert into Kvantland.Variant (problem, description, content) values (%s, %s, %s)", (problem.id, description, json.dumps(variant['content'])))	

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
	

def Games():
	global cur
	current_town = Town('Игры')

	problem_1 = Problem(
		name = 'Ход ферзём',
		points = 2,
		type_ = 'queen_move',
	)
	for horse_config in [
		[
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', 'H', ' ', ' ', ' ', ' ', ' ', ' ', 'H', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', 'H', ' ', ' ', 'H', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'H', ' '],
		[' ', ' ', ' ', ' ', 'H', ' ', ' ', ' ', ' ', ' '],
		],

		[
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', 'H', ' ', ' ', ' ', 'H', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', 'H', ' ', ' ', 'H', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'H', ' '],
		[' ', ' ', ' ', ' ', 'H', ' ', ' ', ' ', ' ', ' '],
		],

		[
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', 'H', ' ', ' ', ' ', ' ', 'H', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', 'H', ' ', ' ', 'H', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'H', ' '],
		[' ', ' ', ' ', ' ', 'H', ' ', ' ', ' ', ' ', ' '],
		],

		[
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', 'H', ' ', ' ', ' ', ' ', ' ', 'H', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', 'H', ' ', ' ', 'H', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'H', ' '],
		[' ', ' ', ' ', ' ', 'H', ' ', ' ', ' ', ' ', ' '],
		],
	]:
		problem_1.add_variant({
			'content': {
				'remaining_tries': 3,
				'turn': None,
				'horse_config': horse_config,
				'queen_position': [9, 0], 
				'componentType': 'queenMove',
				'inputType': 'HintOnlyInput',
			}
		})

	problem_2 = Problem(
		name = 'Звёздные войны',
		points = 3,
		type_ = 'star_wars',
	)

	for dron_amount, board_side, correct in [
		(7, 10, [2, 2]),
		(7, 10, [3, 7]),
		(7, 10, [1, 9]),
		(7, 10, [5, 6]),
	]:
		problem_2.add_variant({
			'content': {
				'result': [],
				'board': [['#E8E8E8' for i in range(board_side)] for j in range(board_side)],
				'correct': correct,
				'search_num': 0,
				'dron_amount': dron_amount,
				'board_side': board_side,
				'componentType': "starWars",
				'inputType': "InteractiveTypeInput",
			}
		})
	
	current_town.add_problems([problem_1, problem_2, ])
	

def Algorithms():
	global cur
	current_town = Town('Алгоритмы')
	
	problem_1 = Problem(
		name="Иннокентий и логика",
		points=1,
		type_="Innocent_and_logic",
	)

	for blocks in [
		['Жарко', 'Светит солнце', 'Дует ветер', 'Идёт дождь']
	]:
		problem_1.add_variant({
			'content': {
				'blocks': blocks,
				'translation': {
					'Жарко': "A",
					'Светит солнце': "B",
					'Дует ветер': "C",
					'Идёт дождь': "D",
					'XOR': " ^ ",
					'НЕ': "-~",
					'ИЛИ': " | ",
					'И': " & ",
					'(': "(",
					')': ")",
				},
				'componentType': "InnocentAndLogic",
				'inputType': "InteractiveTypeInput",
				'correct': [
					"A & (B & -~(C & D))",
					"-~A & (B |  -~C) & -~(B & -~C)"
				],
			}
		})

	current_town.add_problems([problem_1, ])


def Blocks():
	global cur
	current_town = Town('Блоки')
	
	problem_1 = Problem(
		name='Соберите Решето',
		points=2,
		type_='assemble_the_sieve',
	)
	for correct_permutations in [
		[[2, 1, 4, 0, 6, 3, 5],
		[2, 1, 4, 6, 0, 3, 5],],
	]:
		problem_1.add_variant({
			'content': {
				'correct': correct_permutations,
				'componentType': "assembleTheSieve",
				'inputType': "InteractiveTypeInput",
			},

		})
		
	problem_2 = Problem(
		name='Ассемблирует компайлер',
		points=3,
		type_='assembling_the_compailer',
	)
	problem_2.add_variant({
		'content': {
			'max_lines_amount': 10,
			'blockTypes': ["Add", "Sub", "ShiftLeft", "ShiftRight", "Move"],
			'componentType': "assemblingTheCompiler",
			'inputType': "InteractiveTypeInput",
		}
	})

	problem_3 = Problem(
		name='Робот в лабиринте',
		points=4,
		type_='robot_in_maze',
	)
	for maze, start_position, start_diraction, end_position in [
		([
			'._._._._._._._.',
			'| | . | . . . |',
			'| ._._. ._._. |',
			'| | . | | . . |',
			'| . ._._| | . |',
			'| . | ._._| . |',
			'| . . | . . ._|',
			'|_._._|_._._._|'
		], [6, 0], 'right', [0, 6]),
		([
			'._._._._._._._.',
			'| | . | . . . |',
			'| ._._. ._._. |',
			'| | . | | . . |',
			'| . ._._| | . |',
			'| . | ._._| . |',
			'| . . | . . ._|',
			'|_._._|_._._._|'
		], [0, 6], 'left', [6, 0]),
		([
			'._._._._._._._.',
			'| . . . | . | |',
			'| ._._. ._._. |',
			'| . . | | . | |',
			'| . | |_._. . |',
			'| . |_._. | . |',
			'|_. . . | . . |',
			'|_._._._|_._._|'
		], [6, 6], 'left', [0, 0]),
		([
			'._._._._._._._.',
			'| . . . | . | |',
			'| ._._. ._._. |',
			'| . . | | . | |',
			'| . | |_._. . |',
			'| . |_._. | . |',
			'|_. . . | . . |',
			'|_._._._|_._._|'	
		], [0, 0], 'right', [6, 6]),
	]:
		problem_3.add_variant({
			'content': {
				'action_allowed': True,
				'allowed_blocks_amount': 7,
				'componentType': "robotInMaze",
				'inputType': "InteractiveTypeInput",
				'maze': maze,
				'current_position': start_position,
				'end_position': end_position,
				'current_direction': start_diraction,
				'commands': [
					{'text': "Повернуть влево", 'type': 'usual'},
					{'text': "Повернуть вправо", 'type': "usual"},
					{'text': "Пройти вперед на 1 клетку", 'type': "usual"},
					{'text': "Пока нет препятствия", 'type': "cycle"},
				],
			}
		})

	current_town.add_problems([problem_1, problem_2, problem_3, ])

def Proga():
	global cur
	current_town = Town('Прога')


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
			Games()
			Algorithms()
			Blocks()
			Proga()
			update_positions()
