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


def get_class_content(content: dict, classes: str):
	class_content = {}
	for key in content.keys():
		try:
			class_content[key] = content[key][classes]
		except:
			class_content[key] = content[key]
	return class_content


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

			try:
				classes = variant['classes']
			except:
				classes = ['all']

			for possible_class in classes:
				current_problem_num += 1
				variant_num = current_tournament * 1000 + current_problem_num

				try:
					variant_points = variant['points'][possible_class]
				except:
					variant_points = problem.points

				cur.execute("""insert into Kvantland.Variant 
								(variant, problem, description, content, classes, variant_points) overriding system value 
								values (%s, %s, %s, %s, %s, %s)""", 
								(variant_num, problem.id, description, json.dumps(get_class_content(variant['content'], possible_class)), possible_class, variant_points))


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

	current_town.add_problems([])
	

def Chiselburg():
	global cur
	current_town = Town('Чиселбург')

	current_town.add_problems([])


def Geoma():
	global cur
	current_town = Town('Геома')

	current_town.add_problems([])


def Golovolomsk():
	global cur
	current_town = Town('Головоломск')

	current_town.add_problems([])


def Kombi():
	global cur
	current_town = Town('Республика Комби')

	current_town.add_problems([])


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
