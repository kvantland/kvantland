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

	problems_list = add_problem_to_list(problems_list, cur, "Остров Лжецов", 2, 'caskets', "Шкатулки")
	for tmp, ans in [
			[['here', 'near', 'near', 'near', 'no'], 5],
			[['here', 'near', 'no', 'near', 'near'], 2],
			[['no', 'near', 'near', 'near', 'here'], 1],
			[['near', 'near', 'no', 'near', 'here'], 4]
			]:
			desc = f"""Перед вами стоят в ряд 5 шкатулок, в одной из них лежит приз. К шкатулкам прикреплены записки с утверждениями.
			Известно, что ровно одно из утверждений истинно. Откройте шкатулку, в которой лежит приз. У вас всего одна попытка.
			"""
			cont = {
				'tmp': tmp,
				'correct': ans
			}
			variants_list = add_variant_to_list(variants_list, "Шкатулки", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Остров Лжецов", 3, 'integer', "За круглым столом")
	for N, A in [
			(12, 3),
			(16, 4),
			(20, 5),
			(24, 6),
			]:
			desc = f"""За круглым столом сидят {N} человек, каждый из которых либо рыцарь (всегда говорит правду), либо лжец (всегда лжёт). 
			Каждый из сидящих сказал, что среди трёх его соседей по часовой стрелке ровно двое – рыцари. Сколько лжецов сидит за столом, если среди собравшихся точно есть рыцарь?"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "За круглым столом", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Остров Лжецов", 4, 'checkered_logic', "Клетчатая логика")
	for N, A in [
			('клетчатом квадрате 5×5', [
			[0, 1, 1, 1, 0],
			[1, 1, 0, 1, 1],
			[1, 0, 0, 0, 1],
			[1, 1, 0, 1, 1],
			[0, 1, 1, 1, 0]]),
			]:
			desc = f"""На острове живут два племени гномов: рыцари (всегда говорят правду) и лжецы (всегда лгут). Группа гномов встала в клетках клетчатой фигуры. 
			Соседями считаются те, кто стоит в клетках с общей стороной. На вопрос «Верно ли, что ровно двое из твоих соседей из твоего племени?» каждый ответил «Да». Найдите такую расстановку на {N}"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Клетчатая логика", desc, json.dumps(cont))	

	add_list(problems_list, variants_list)


def Chiselburg3(cur):
	problems_list = []
	variants_list = dict()

	problems_list = add_problem_to_list(problems_list, cur, "Чиселбург", 2, 'integer', "Хороший стимул")
	for N, M, A in [
			(5, 6, 7),
			(6, 5, 8),
			(6, 7, 9),
			(8, 6, 10),
			]:
			desc = f"""Вовочка получил {N} двоек и {M} троек по математике (других оценок не было). Папа пообещал купить ему новый ноутбук, если он сможет закончить год с итоговой оценкой 4. 
			Какое наименьшее количество пятерок необходимо получить Вовочке для этого, если учительница выводит оценку за год, округляя среднее значение до ближайшего целого числа 
			(среднее 4,5 она округляет до оценки 5, а среднее 3,5 до оценки 4)."""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Хороший стимул", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Чиселбург", 3, 'sums_on_cube', "Равные суммы на кубе")
	for a, b, c, ans in [
			[12, 8, 22, 75],
			[17, 13, 21, 72],
			[16, 6, 20, 69],
			[11, 9, 19, 66],
			]:
			desc = f"""На каждой грани куба написано натуральное число. Три из них показаны на рисунке, 
					а про остальные три известно, что они простые. Кроме того, суммы чисел на противоположных 
					гранях равны. Чему равна сумма всех чисел на кубе?"""
			cont = {
				'a': a,
				'b': b,
				'c': c,
				'correct': ans,
			}
			variants_list = add_variant_to_list(variants_list, "Равные суммы на кубе", desc, json.dumps(cont))	

	add_list(problems_list, variants_list)

def Geom3(cur):
	problems_list = []
	variants_list = dict()
	
	problems_list = add_problem_to_list(problems_list, cur, "Геома", 4, 'integer', "Прямоугольный треугольник")
	for x, y, z, A in [
			(40, 10, 5, 85),
			(39, 12, 6, 84),
			(38, 14, 7, 83),
			(37, 16, 8, 82),
			]:
			desc = f"""На гипотенузе AB прямоугольного треугольника ABC отметили точку D, а на катете BC – точку E. Чему равен угол EDC, если ∠B = {x}°, ∠BCD = {y}° и ∠BAE = {z}°?
"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Прямоугольный треугольник", desc, json.dumps(cont))

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

	problems_list = add_problem_to_list(problems_list, cur, "Головоломск", 3, 'kid_and_carlson', "Малыш и Карлсон")
	for field, correct in [
			([
			[0, 1, 0, 1, 0, 0],
			[0, 0, 0, 0, 1, 0],
			[0, 0, 0, 1, 0, 0],
			[0, 0, 1, 1, 0, 0],
			[0, 0, 0, 0, 0, 1]], 

			[[[0, 1, 1, 1, 1, 1],
			[0, 0, 0, 0, 1, 1],
			[0, 0, 0, 1, 1, 1],
			[0, 0, 1, 1, 1, 1],
			[0, 0, 0, 0, 0, 1]],
			[[0, 1, 1, 1, 1, 1],
			[0, 1, 0, 0, 1, 1],
			[0, 0, 0, 1, 1, 1],
			[0, 0, 1, 1, 0, 1],
			[0, 0, 0, 0, 0, 1]]]),


			([
			[0, 0, 0, 0, 0, 0],
			[1, 0, 0, 1, 0, 0],
			[0, 0, 1, 0, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[0, 0, 0, 1, 0, 0]],

			[[[0, 0, 0, 0, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 1, 1, 1, 1]],
			[[1, 0, 0, 0, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 1, 1, 1, 0]]]),


			([
			[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 0, 0, 0],
			[0, 0, 0, 1, 0, 0],
			[0, 0, 0, 0, 0, 1],
			[0, 1, 0, 1, 1, 0]],

			[[[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 0, 1],
			[0, 0, 0, 1, 1, 1],
			[0, 1, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1]],
			[[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 0, 1],
			[0, 1, 0, 1, 0, 1],
			[0, 1, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1]],
			[[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1],
			[0, 0, 0, 1, 1, 1],
			[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1]],
			[[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1],
			[0, 1, 0, 1, 0, 1],
			[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1]]]),


			([
			[1, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 1, 0],
			[0, 0, 1, 0, 0, 0],
			[1, 0, 0, 0, 1, 0],
			[0, 1, 0, 0, 0, 0]],

			[[[1, 0, 0, 0, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 1, 1, 1, 0]],
			[[1, 0, 0, 0, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 1, 1, 0, 0, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 1, 1, 1, 0]],
			[[1, 1, 1, 0, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 1, 0, 0, 0]],
			[[1, 1, 1, 1, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 0, 0, 0, 0]]])
			]:
			desc = f"""Малышу на день рождения испекли торт, украшенный вишенками. Карлсон разрезал торт 
			на две одинаковые по форме и размеру части так, что все вишенки достались ему. Попробуйте и вы это сделать."""
			cont = {
				'field': field,
				'correct': correct,
			}
			variants_list = add_variant_to_list(variants_list, "Малыш и Карлсон", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Головоломск", 1, 'five_knights_checkmate', "Мат пятью конями")
	for king_pos, horse_pos, correct in [
	([5, 4], [8, 2], 
		[[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', 1,  '', '', '', ''],
		['', '', 1,  '', '', '', '', ''],
		['', '', '', '', '', '', '', '']]]),
	([5, 4], [5, 3], 
		[[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		[1,  '', '', '', '', '', '', ''],
		['', 1,  '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', '', '', '', '']],
		[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', 1,  '', '', '', '', '', ''],
		[1,  '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', '']]]),
	([5, 4], [6, 3], 
		[[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', 1,  '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', 1,  '', '', '', '', '', ''],
		['', '', '', '', '', '', '', '']],
		[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', 1,  ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', 1,  '', '', '', '', '', ''],
		['', '', '', '', '', '', '', '']]]),
	([5, 4], [3, 2], 
		[[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', 1,  '', '', '', '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', '', '', 1,  ''],
		['', '', '', '', '', '', '', '']],
		[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', 1,  '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', 1,  '', '', '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', 1,  '', '']]])
	]:
		desc = f"""На шахматной доске стоят чёрный король и белый конь (см. рисунок). 
					Поставьте на доску ещё четырёх белых коней так, чтобы все кони стояли в разных горизонталях и в разных 
					вертикалях, а в полученной позиции королю был мат (т.е. король должен находиться под боем одного из коней,
					 и куда бы ни сходил король, его должен атаковать какой-то другой конь)."""
		cont = {
			'king_pos': king_pos,
			'horse_pos': horse_pos,
			'correct': correct,
		}
		variants_list = add_variant_to_list(variants_list, "Мат пятью конями", desc, json.dumps(cont))	
	add_list(problems_list, variants_list)

def CombiRepublic3(cur):
	problems_list = []
	variants_list = dict()

	problems_list = add_problem_to_list(problems_list, cur, "Республика Комби", 3, 'integer', "Васин досуг")
	for a, b, c, d, A in [
			(2, 4, 6, 3, 15),
			(3, 5, 6, 4, 10),
			(3, 4, 8, 2, 10),
			(3, 4, 6, 3, 10),
			]:
			desc = f"""Вася решил разнообразить свой досуг. Каждое утро он смотрит в календарь. Если сегодняшнее число делится на {a}, то в этот день Вася читает книги, если делится на {b} – решает задачи, 
			а если делится на {c} – играет в футбол. Но делать все три дела в один день у Васи не получается – если число делится и на {a}, и на {b}, и на {c}, то в такой день Вася выбирает любые два занятия из трёх. 
			В результате в июле Вася играл в футбол {d} раз. А сколько раз он в июле читал книги?"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Васин досуг", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Республика Комби", 4, 'integer', "Футбольный турнир")
	for N, A in [
			(65, 19),
			(70, 14),
			(85, 23),
			(88, 20),
			]:
			desc = f"""Футбольный турнир проходил в один круг (каждая команда с каждой сыграла один раз). За победу дают 3 очка, а за ничью — одно. В итоге оказалось, что все команды вместе набрали {N} очков. 
			Сколько ничьих было в этом турнире?"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Футбольный турнир", desc, json.dumps(cont))	

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
