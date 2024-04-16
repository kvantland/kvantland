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


def IslandOfLiars3(cur):
	problems_list = []
	variants_list = dict()

	problems_list = add_problem_to_list(problems_list, cur, "Остров Лжецов", 2, 'caskets', "Шкатулки", hint_cost=1, hint="""Выберите шкатулку и предположите, что там находится приз. Если оказалось, 
		что есть более одного истинного утверждения на записках, то приза в выбранной шкатулке быть не может.""")
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

	problems_list = add_problem_to_list(problems_list, cur, "Остров Лжецов", 3, 'integer', "За круглым столом", image="liar.png", hint_cost=1, hint="""Выберите рыцаря и посмотрите на трёх человек, сидящих за ним по часовой стрелке, а также на следующего за ними человека.""")
	for N, A in [
			('12 человек', 3),
			('16 человек', 4),
			('20 человек', 5),
			('24 человека', 6),
			]:
			desc = f"""За круглым столом сидят {N}, каждый из которых либо рыцарь (всегда говорит правду), либо лжец (всегда лжёт). 
			Каждый сказал, что среди трёх человек, сидящих за ним по часовой стрелке, ровно двое – рыцари. Сколько лжецов сидит за столом, если среди собравшихся точно есть рыцарь?"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "За круглым столом", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Остров Лжецов", 4, 'checkered_logic', "Гномы на клетках", hint_cost=1, hint="""Поставьте гномов по циклу (у каждого ровно два соседа) так, чтобы ни у какой свободной клетки не было двух соседних свободных.""")
	for A in [
			([[0,-1, 1, 1, 1, 0],
			  [1, 1, 1, 0, 1, 1],
			  [1, 0, 0, 0, 0, 1],
			  [1, 1, 0, 1, 1, 1],
			  [0, 1, 1, 1, 0,-1]]),
			([[0, 1, 1, 1, -1, 0],
			  [1, 1, 0, 1, 1, 1],
			  [1, 0, 0, 0, 0, 1],
			  [1, 1, 1, 0, 1, 1],
			  [0,-1, 1, 1, 1, 0]]),
			([[0, 1, 1, 1, -1, 0],
			  [1, 1, 0, 1, 1, 1],
			  [1, 0, 0, 0, 0, 1],
			  [1, 1, 1, 0, 1, 1],
			  [0, 0, 1, 1, 1,-1]]),
			([[0,-1, 1, 1, 1, 0],
			  [1, 1, 1, 0, 1, 1],
			  [1, 0, 0, 0, 0, 1],
			  [1, 1, 0, 1, 1, 1],
			  [-1, 1, 1, 1, 0, 0]]),
			]:
			desc = f"""На острове живут два племени гномов: рыцари (всегда говорят правду) и лжецы (всегда лгут). 
			Группа гномов встала в клетках клетчатой фигуры (в каждую свободную клетку на рисунке встал ровно один гном). 
			Соседями считаются те, кто стоит в клетках с общей стороной. На вопрос «Верно ли, что ровно двое из твоих соседей из твоего племени?» каждый ответил «Да». 
			Где должны стоять рыцари (расставьте их), если во всех остальных клетках будут стоять лжецы? Нажимая на нужную клетку, вы ставите туда гнома. Нажимая второй раз, вы убираете его."""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Гномы на клетках", desc, json.dumps(cont))	

	add_list(problems_list, variants_list)


def Chiselburg3(cur):
	problems_list = []
	variants_list = dict()

	problems_list = add_problem_to_list(problems_list, cur, "Чиселбург", 2, 'integer', "Хороший стимул", image="boy1.png", hint_cost=1, hint="""Пусть Вовочка в итоге получил n двоек, m троек и k пятёрок. 
		Тогда среднее равно (2n + 3m + 5k)/(n + m + k). Нужно, чтобы это число было не меньше 3,5.""")
	for N, M, A in [
			(5, 6, 7),
			(6, 5, 8),
			(6, 7, 9),
			(8, 6, 10),
			]:
			desc = f"""Вовочка получил {N} двоек и {M} троек по математике (других оценок не было). 
			Папа пообещал купить ему новый ноутбук, если он сможет закончить год с итоговой оценкой 4. 
			Какое наименьшее количество пятёрок необходимо получить Вовочке для этого, если учительница выводит оценку за год, округляя среднее значение до ближайшего целого числа
			(среднее 4,5 она округляет до оценки 5, а среднее 3,5 — до оценки 4)?"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Хороший стимул", desc, json.dumps(cont))	


	problems_list = add_problem_to_list(problems_list, cur, "Чиселбург", 3, 'kvantik_play', "Ноутик и Квантик развлекаются", hint_cost=1, hint="""Произведение цифр делится на 25, и среди цифр нет нуля. 
		Значит, первая и последняя цифра – пятёрки.""")
	for N, A in [
			(5400, 5943215),
			(4800, 5843215),
			(8400, 5873215),
			(4200, 5743215),
			]:
			desc = f"""Ноутик заменил буквы цифрами в слове КВАНТИК (разным буквам соответствуют разные цифры, одинаковым – одинаковые цифры). 
			Какое наибольшее число могло у него получиться, если произведение цифр этого числа оказалось равно {N}?"""
			cont = {
				'word': 'КВАНТИК',
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Ноутик и Квантик развлекаются", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Чиселбург", 4, 'sums_on_cube', "Равные суммы на кубе", hint_cost=1, hint="""Рассмотрите возможные остатки при делении на 3 чисел на невидимых гранях.""")
	for a, b, c, ans in [
			[12, 8, 22, 75],
			[17, 13, 21, 72],
			[16, 6, 20, 69],
			[11, 9, 19, 66],
			]:
			desc = f"""На каждой грани куба написано натуральное число. Три из них — {a}, {b} и {c} — показаны на рисунке, 
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
	
	problems_list = add_problem_to_list(problems_list, cur, "Геома", 2, 'tunnel', "Как построить тоннель?", hint_cost=1, hint="""Кратчайший путь представляет собой цепочку из 13 клеток.""")
	for f, A in [
		([	
		[33, 21, 21, 42, 33, 21, 21],
		[12, 12, 12, 10, 33, 21, 40],
		[10, 12, 12, 00, 10, 12, 12],
		[00, 33, 21, 23, 21, 21, 42],
		[00, 12, 31, 42, 33, 21, 40],
		[00, 10, 12, 00, 12, 31, 21],
		[00, 31, 21, 21, 42, 00, 00]], '0,3,4'),
		([	
		[33, 21, 21, 42, 33, 21, 21],
		[12, 12, 12, 10, 10, 00, 31],
		[10, 12, 31, 21, 21, 42, 12],
		[00, 33, 21, 23, 21, 21, 42],
		[00, 12, 31, 42, 33, 21, 40],
		[00, 10, 00, 10, 12, 31, 21],
		[00, 31, 21, 21, 42, 00, 00]], '0,6,4'),
		([	
		[33, 21, 21, 42, 33, 21, 21],
		[12, 00, 12, 10, 10, 31, 21],
		[12, 12, 12, 31, 21, 21, 42],
		[10, 33, 23, 42, 00, 00, 12],
		[00, 12, 12, 12, 33, 23, 40],
		[00, 10, 12, 10, 12, 31, 42],
		[00, 31, 21, 40, 10, 00, 10]], '1,3,2'),
		([	
		[33, 23, 21, 42, 31, 21, 21],
		[12, 12, 12, 10, 31, 42, 31],
		[10, 12, 31, 21, 21, 21, 42],
		[00, 12, 31, 23, 21, 40, 12],
		[00, 12, 00, 12, 33, 21, 40],
		[00, 31, 40, 10, 12, 31, 21],
		[00, 31, 21, 21, 42, 00, 00]], '0,6,3'),
			]:
			desc = f"""Одна из горных частей Квантландии имеет размеры 80×80 км (см. карту ниже, перегородки показывают расположение гор). 
			Где нужно сделать тоннель (сквозь перегородку между соседними клетками), чтобы путь из A в B по клеткам был наименьшим? Отметьте перегородку, которую нужно удалить."""
			cont = {
				'board': f,
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Как построить тоннель?", desc, json.dumps(cont))

	problems_list = add_problem_to_list(problems_list, cur, "Геома", 4, 'integer', "Прямоугольный треугольник", image="geoma3_3.svg", hint_cost=1, hint="""Докажите, что треугольник DCE равнобедренный.""")
	for x, y, z, A in [
			(40, 10, 5, 85),
			(39, 12, 6, 84),
			(38, 14, 7, 83),
			(37, 16, 8, 82),
			]:
			desc = f"""На гипотенузе AB прямоугольного треугольника ABC отметили точку D, а на катете BC – точку E. Чему равен угол EDC, если ∠B = {x}°, ∠BCD = {y}° и ∠BAE = {z}°?"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Прямоугольный треугольник", desc, json.dumps(cont))

	problems_list = add_problem_to_list(problems_list, cur, "Геома", 3, 'integer', "Часы со стрелкой", image="clock_with_hand.png", hint_cost=1, hint="""Сектор в один час – это 360/12 = 30 градусов. Если минутная стрелка смещается на 10 минут (то есть 1/6 часа), 
		то часовая поворачивается на 30/6 = 5 градусов.""")
	for hour, minute, ans in [
			(14, 20, 50),
			(16, 40, 100),
			(20, 50, 35),
			(23, 10, 85),
			]:
			desc = f"""Какой угол образуют часовая и минутная стрелка ровно в {hour}:{minute}?
					Ответ дайте в градусах."""
			cont = {
				'correct': ans,
			}
			variants_list = add_variant_to_list(variants_list, "Часы со стрелкой", desc, json.dumps(cont))

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

	problems_list = add_problem_to_list(problems_list, cur, "Головоломск", 4, 'kid_and_carlson', "Малыш и Карлсон", hint_cost=1, hint="""Одна из частей должна переходить в другую при повороте на 180 градусов относительно центра торта. 
		Поэтому если в какой-то клетке есть вишенка, то симметричная ей относительно центра клетка должна достаться Малышу.""")
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
			[[1, 0, 0, 0, 0, 0],
			[1, 1, 1, 1, 0, 0],
			[1, 1, 1, 0, 0, 0],
			[1, 1, 0, 0, 0, 0],
			[1, 1, 1, 1, 1, 0]],
			[[0, 1, 1, 1, 1, 1],
			[0, 1, 0, 0, 1, 1],
			[0, 0, 0, 1, 1, 1],
			[0, 0, 1, 1, 0, 1],
			[0, 0, 0, 0, 0, 1]],
			[[1, 0, 0, 0, 0, 0],
			[1, 0, 1, 1, 0, 0],
			[1, 1, 1, 0, 0, 0],
			[1, 1, 0, 0, 1, 0],
			[1, 1, 1, 1, 1, 0]]]),


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
			[[1, 1, 1, 1, 1, 1],
			[0, 1, 0, 0, 0, 1],
			[0, 1, 0, 1, 0, 1],
			[0, 1, 1, 1, 0, 1],
			[0, 0, 0, 0, 0, 0]],
			[[1, 0, 0, 0, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 1, 1, 1, 0]],
			[[0, 1, 1, 1, 1, 1],
			[0, 1, 0, 0, 0, 1],
			[0, 1, 0, 1, 0, 1],
			[0, 1, 1, 1, 0, 1],
			[0, 0, 0, 0, 0, 1]]]),


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
			[[1, 1, 1, 1, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 1, 0, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 0, 0, 0, 0, 0]],
			[[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 0, 1],
			[0, 1, 0, 1, 0, 1],
			[0, 1, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1]],
			[[1, 1, 1, 1, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 0, 0, 0, 0, 0]],
			[[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1],
			[0, 0, 0, 1, 1, 1],
			[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1]],
			[[1, 1, 1, 1, 1, 0],
			[1, 0, 0, 0, 0, 0],
			[1, 1, 1, 0, 0, 0],
			[1, 1, 1, 1, 1, 0],
			[1, 0, 0, 0, 0, 0]],
			[[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1],
			[0, 1, 0, 1, 0, 1],
			[0, 0, 0, 0, 0, 1],
			[0, 1, 1, 1, 1, 1]],
			[[1, 1, 1, 1, 1, 0],
			[1, 0, 0, 0, 0, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 1, 1, 1, 1, 0],
			[1, 0, 0, 0, 0, 0]]]),


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
			[[0, 1, 1, 1, 1, 1],
			[0, 1, 0, 0, 0, 1],
			[0, 1, 0, 1, 0, 1],
			[0, 1, 1, 1, 0, 1],
			[0, 0, 0, 0, 0, 1]],
			[[1, 0, 0, 0, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 1, 1, 0, 0, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 1, 1, 1, 0]],
			[[0, 1, 1, 1, 1, 1],
			[0, 1, 0, 0, 0, 1],
			[0, 0, 0, 1, 1, 1],
			[0, 1, 1, 1, 0, 1],
			[0, 0, 0, 0, 0, 1]],
			[[1, 1, 1, 0, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 1, 0, 0, 0]],
			[[0, 0, 0, 1, 1, 1],
			[0, 1, 0, 0, 0, 1],
			[0, 1, 0, 1, 0, 1],
			[0, 1, 1, 1, 0, 1],
			[0, 0, 0, 1, 1, 1]],
			[[1, 1, 1, 1, 0, 0],
			[1, 0, 1, 1, 1, 0],
			[1, 0, 1, 0, 1, 0],
			[1, 0, 0, 0, 1, 0],
			[1, 1, 0, 0, 0, 0]],
			[[0, 0, 0, 0, 1, 1],
			[0, 1, 0, 0, 0, 1],
			[0, 1, 0, 1, 0, 1],
			[0, 1, 1, 1, 0, 1],
			[0, 0, 1, 1, 1, 1]]])
			]:
			desc = f"""Малышу на день рождения испекли торт, украшенный вишенками. Карлсон разрезал торт 
			на две одинаковые по форме и размеру части так, что все вишенки достались ему. Попробуйте и вы это сделать."""
			cont = {
				'field': field,
				'correct': correct,
			}
			variants_list = add_variant_to_list(variants_list, "Малыш и Карлсон", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Головоломск", 3, 'five_knights_checkmate', "Мат пятью конями", hint_cost=1, hint="""Кони должны атаковать все 9 клеток квадрата 3×3, в центре которого стоит король. При этом каждый из них может атаковать максимум две из этих клеток. 
		Стоящий на доске конь атакует только одну клетку, поэтому все остальные кони должны атаковать по две клетки.""")
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
		['', '', '', '', '', '', '', '']],
		[
		['', '', '', '', '', '', '', ''],
		['', '', '', 1,  '', '', '', ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', 1,  '', '', '', '', ''],
		['', '', '', '', '', '', '', '']]]),
	([5, 4], [3, 1], 
		[[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', 1,  '', '', '', '', '', ''],
		['', '', 1,  '', '', '', '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', '', '', '', '']],
		[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', 1,  '', '', '', '', '', ''],
		['', '', '', '', '', '', 1,  ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', '', '', '', '']]]),
	([5, 4], [2, 6], 
		[[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', 1,  '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', 1,  '', '', '', '', ''],
		['', 1,  '', '', '', '', '', ''],
		['', '', '', '', '', '', '', '']],
		[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', 1,  '', '', '', '', ''],
		['', 1,  '', '', '', '', '', ''],
		['', '', '', 1,  '', '', '', '']]]),
	([5, 4], [7, 7], 
		[[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', 1,  '', '', '', '', '', ''],
		['', '', 1,  '', '', '', '', ''],
		['', '', '', '', 1,  '', '', ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', '']],
		[
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', ''],
		['', 1,  '', '', '', '', '', ''],
		['', '', 1,  '', '', '', '', ''],
		[1,  '', '', '', '', '', '', ''],
		['', '', '', '', '', 1,  '', ''],
		['', '', '', '', '', '', '', ''],
		['', '', '', '', '', '', '', '']]])
	]:
		desc = f"""На шахматной доске стоят белый король и чёрный конь (см. рисунок). Поставьте на доску ещё четырёх чёрных коней так, 
		чтобы все кони стояли в разных горизонталях и в разных вертикалях, а в полученной позиции королю был мат 
		(то есть король должен находиться под боем одного из коней, и куда бы ни сходил король, его должен атаковать какой-то конь)."""
		cont = {
			'king_pos': king_pos,
			'horse_pos': horse_pos,
			'correct': correct,
		}
		variants_list = add_variant_to_list(variants_list, "Мат пятью конями", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Головоломск", 2, 'equality_of_matches', "Равенство из спичек", hint_cost=1, hint="""Ваше действие должно изменить один из сомножителей. Подумайте, как его можно поменять, чтобы получилась другая цифра.""")
	for nums, sgn, correct in [
		([8, 4, 6, 8], ['*', '+', '='], [0, 4, 8, 8]),
		([2, 9, 8, 7], ['*', '-', '='], [2, 8, 9, 7]),
		([8, 5, 5, 6], ['*', '+', '='], [0, 5, 6, 6]),
		([9, 2, 2, 6], ['*', '+', '='], [3, 2, 2, 8])
		]:
		desc = "Из спичек выложено неверное равенство. Переложите одну спичку так, чтобы равенство стало верным."
		cont = {
			'nums': nums,
			'sgn': sgn,
			'correct': correct,
			'step': 0
		}
		variants_list = add_variant_to_list(variants_list, "Равенство из спичек", desc, json.dumps(cont))		
	
	add_list(problems_list, variants_list)

def CombiRepublic3(cur):
	problems_list = []
	variants_list = dict()

	problems_list = add_problem_to_list(problems_list, cur, "Республика Комби", 3, 'integer', "Васин досуг", image="boy2.png", hint_cost=1, hint="""Подсчитайте, какое наименьшее количество раз мог Вася играть в футбол при таких условиях. 
		После этого попробуйте понять, какие два занятия он выбирал в те дни, когда теоретически мог бы заниматься тремя делами.""")
	for a, b, c, d, A in [
			(2, 4, 6, 3, 15),
			(3, 5, 6, 4, 10),
			(3, 4, 8, 2, 10),
			(3, 4, 6, 3, 10),
			]:
			desc = f"""Вася решил разнообразить свой досуг. Каждое утро он смотрит в календарь. Если сегодняшнее число делится на {a}, то в этот день Вася читает книги, если делится на {b} – решает задачи, 
			а если делится на {c} – играет в футбол. Но делать все три дела в один день у Васи не получается – если число делится и на {a}, и на {b}, и на {c}, то в такой день Вася выбирает любые два занятия из трёх. 
			В результате в июле Вася играл в футбол {d} раза. А сколько раз он в июле читал книги?"""
			cont = {
				'correct': A,
			}
			variants_list = add_variant_to_list(variants_list, "Васин досуг", desc, json.dumps(cont))	

	problems_list = add_problem_to_list(problems_list, cur, "Республика Комби", 4, 'integer', "Футбольный турнир", image="director.png", hint_cost=1, hint="""В каждой игре команды набирают в сумме либо 2, либо 3 очка. А всего n команд проводят в однокруговом турнире n(n − 1)/2 игр. 
		Учитывая это, подумайте, сколько команд принимало участие в турнире.""")
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

	problems_list = add_problem_to_list(problems_list, cur, "Республика Комби", 2, 'greedy_dwarfs', "Жадные гномы", hint_cost=1, hint="""Первым действием переправляются 3 гнома, потом один из них возвращается.""")
	for start_conf, conf, start_time, remain_time, trip_time, bag_weight, dwarf_weight, remain_weight, start_weight, step, side, start_side in [
			[{'left': {'dwarf': 0, 'bag': 0},
			'right': {'dwarf': 5, 'bag': 1}},
			{'left': {'dwarf': 0, 'bag': 0},
			'right': {'dwarf': 5, 'bag': 1}
			}, 30, 30, 6, 50, 20, 70, 70, 0, 'right', 'right']
			]:
			desc = f"""После долгого путешествия на одном берегу реки остановились пять гномов, 
			которые тащат с собой большой мешок с золотом. В их распоряжении имеется одна лодка 
			грузоподъёмностью {start_weight} кг, которая проплывает от одного берега до другого за {trip_time} минут 
			(вне зависимости от нагрузки). Известно, что каждый из гномов весит {dwarf_weight} кг, 
			а мешок с золотом – {bag_weight} кг. Помогите гномам переправиться через реку за {start_time} минут. 
			Нажав кнопку ↻, можно получить исходное состояние."""
			cont = {
				'start_conf': start_conf,
				'conf': conf,
				'remain_time': remain_time,
				'trip_time': trip_time,
				'bag_weight': bag_weight,
				'dwarf_weight': dwarf_weight,
				'remain_weight': remain_weight,
				'start_weight': start_weight,
				'side': side,
				'start_side': start_side,
				'step': step,
				'start_time': start_time,
			}
			variants_list = add_variant_to_list(variants_list, "Жадные гномы", desc, json.dumps(cont))	

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
