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
	variants = []
	id = None
	
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
	
	current_town.add_problems([problem_1, ])
	

def Algorithms():
	global cur
	current_town = Town('Алгоритмы')


def Blocks():
	global cur
	current_town = Town('Блоки')

def Proga():
	global cur
	current_town = Town('Прога')


def update_positions_town(cur, town, problem_count):
	x0 = 1280 / 2
	y0 = 720 / 2
	R = 250
	base = 0.25
	cur.execute("select problem from Kvantland.Problem where town = %s and tournament = %s", (town, current_tournament))
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
