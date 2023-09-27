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

def get_type_id(cur, тип):
	cur.execute("select тип from Тип where код = %s", (тип, ))
	(тип,), = cur.fetchall()
	return тип


# def get_group_id(cur, город, баллы):
# 	cur.execute("select группа from Группа join Город using (город) where Город.название = %s and баллы = %s", (город, баллы))
# 	(группа,), = cur.fetchall()
# 	return группа
#
#
# def add_problem(cur, город, баллы, тип, название):
# 	группа = get_group_id(cur, город, баллы)
# 	тип = get_type_id(cur, тип)
# 	cur.execute("insert into Задача (группа, название, тип) values (%s, %s, %s) returning задача", (группа, название, тип))
# 	(задача,), = cur.fetchall()
# 	return задача


def get_town_id(cur, название):
	cur.execute("select город from Город where название = %s", (название, ))
	(город,), = cur.fetchall()
	return город


def add_problem(cur, город, баллы, тип, название, подсказка=None, стоимость_подсказки=None, изображение=None):
	тип = get_type_id(cur, тип)
	город = get_town_id(cur, город)
	cur.execute("insert into Задача (город, баллы, название, тип, изображение) values (%s, %s, %s, %s, %s) returning задача", (город, баллы, название, тип, изображение))
	(задача,), = cur.fetchall()
	if подсказка:
		if not стоимость_подсказки:
			стоимость_подсказки = (баллы + 1) // 2
		cur.execute("insert into Подсказка (задача, текст, стоимость) values (%s, %s, %s)", (задача, подсказка, стоимость_подсказки))
	return задача


def add_variant(cur, задача, описание, содержание):
	cur.execute("insert into Вариант (задача, описание, содержание) values (%s, %s, %s) returning вариант", (задача, описание, содержание))
	(вариант,), = cur.fetchall()
	return вариант


def ОстровЛжецов(cur):
	# задача = add_problem(cur, "Остров Лжецов", 2, 'radio', "Выборы мэра острова")
	# for N in [15, 17, 19, 21]:
	# 	desc = f"Каждый кандидат в мэры острова либо лжец, либо правдолюб. Лжецы всегда лгут, правдолюбы всегда говорят правду, и все кандидаты знают, кто есть кто. В начале дебатов каждый из {N} кандидатов заявил: «Среди остальных присутствующих  лжецов больше, чем правдолюбов». После того как подошёл опоздавший {N+1}-й кандидат, каждый из кандидатов повторил своё заявление. Кто опоздавший: лжец или правдолюб?"
	# 	cont = {
	# 		'answers': [
	# 			"Лжец",
	# 			"Правдолюб",
	# 			"Нельзя однозначно определить",
	# 		],
	# 		'correct': 1,
	# 	}
	# 	add_variant(cur, задача, desc, json.dumps(cont))

	# Задача "Игра с лампочками"
	# Вариации:
	# variations = [
	# 	[[[0, 1], [1, 1]], [[0, 1], [1, 0]], [[0, 0], [1, 1]], [[1, 1], [0, 1]], [[1, 0], [1, 1]]],
	# 	[[[1, 1], [1, 0]], [[0, 1], [1, 0]], [[1, 1], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [1, 1]]],
	# 	[[[0, 1], [1, 0]], [[1, 1], [1, 0]], [[1, 0], [1, 1]], [[1, 1], [0, 1]], [[1, 1], [0, 0]]],
	# 	[[[0, 1], [1, 0]], [[0, 1], [1, 1]], [[1, 0], [1, 1]], [[1, 1], [0, 1]], [[0, 0], [1, 1]]]
	# ]
	# Ответы: [
	# 	[[1, 2, 3, 4], [1, 3, 5]],
	# 	[[1, 3, 4], [1, 2, 3, 5]],
	# 	[[1, 2, 3, 5], [2, 4, 5]],
	# 	[[2, 3, 5], [1, 2, 4, 5]]
	# ]

	задача = add_problem(cur, "Остров Лжецов", 3, 'liars', "Лжецы и хитрецы", "Возьмите какого-нибудь правдолюба (П), рядом с ним по условию должны сидеть хитрец (Х) и лжец (Л).  Докажите, что рядом с лжецом сидит ещё один правдолюб.")
	for N, A in [(10, "STLTSSTLTS"), (11, "STLTSSTLTSS"), (15, "STLTSSTLTSSTLTS"), (16, "STLTSSTLTSSTLTSS")]:
		assert len(A) == N
		desc = f"""За круглым столом сидят {N} человек, каждый из которых либо правдолюб (всегда говорит
			правду), либо лжец (всегда лжёт), либо хитрец (из двух его утверждений одно
			истина, а другое — ложь). Каждый из сидящих заявил «рядом со мной сидит лжец» и
			«рядом со мной сидит хитрец». Какое наименьшее число хитрецов может быть за столом?
			<p>Требуется рассадить всех на стульях так, чтобы условие задачи было выполнено, а хитрецов было как можно меньше."""
		rotations = {A[k:] + A[:k] for k in range(N)}
		cont = {
			'chairs': N,
			'correct': list(rotations),
		}
		add_variant(cur, задача, desc, json.dumps(cont))
 #
	# задача = add_problem(cur, "Остров Лжецов", 1, 'integer', "За круглым столом")
	# for N, A in [(12, 8), (15, 10), (18, 12), (21, 14)]:
	# 	desc = f"За круглым столом сидят {N} человек, каждый из которых либо рыцарь (всегда говорит правду), либо лжец (всегда лжёт). Каждый из сидящих сказал, что хотя бы один его сосед — лжец. Какое наибольшее количество рыцарей могло быть за столом?"
	# 	cont = {
	# 		'correct': A,
	# 	}
	# 	add_variant(cur, задача, desc, json.dumps(cont))
 #
	# задача = add_problem(cur, "Остров Лжецов", 2, 'integer', "Король и два придворных мудреца")
	# for S, m, n, A in [(60, 5, 3, 18), (72, 6, 4, 21), (73, 6, 3, 16), (72, 7, 3, 15)]:
	# 	desc = f"Король решил проверить своих мудрецов: первый должен в тайне от второго записать {m} различных натуральных чисел с суммой {S} и сообщить второму мудрецу лишь {n}-е по величине из загаданных чисел. После чего второй мудрец должен назвать все записанные числа. У мудрецов не было возможности сговориться, но тем не менее они справились с заданием. Какое число сообщил первый?"
	# 	cont = {
	# 		'correct': A,
	# 	}
	# 	add_variant(cur, задача, desc, json.dumps(cont))

	задача = add_problem(cur, "Остров Лжецов", 2, 'radio', "Дело о краже кораллов", изображение="thieves.jpg", подсказка="Предположите по очереди, что один из них сказал правду. Посмотрите, получается противоречие или нет. Результаты удобно отражать в таблице.")
	for a, b, c, A in [
			("Я не крал. Карл украл.", "Карл не крал. Алекс украл.", "Я не крал. Бен не крал.", 0),
			("Я не крал. Карл не крал.", "Я не крал. Алекс украл.", "Алекс не крал. Бен украл.", 1),
			("Бен не крал. Карл украл.", "Я не крал. Алекс не крал.", "Я не крал. Бен украл.", 2),
			("Я не крал. Бен украл.", "Я не крал. Карл не крал.", "Я не крал. Алекс украл.", 0),
		]:
		desc = f"Детектив расследовал дело о краже кораллов у Клары. Трое подозреваемых Алекс, Бен и Карл дали следующие показания:<p>Алекс: «{a}»<br>Бен: «{b}»<br>Карл: «{c}»<p>Было установлено, что двое сказали правду, а третий дважды солгал. Кто украл кораллы?"
		cont = {
			'answers': [
				"Алекс",
				"Бен",
				"Карл",
				"Нельзя однозначно определить",
			],
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))


def Чиселбург(cur):
	# Задача "Равенство"
	# Вариации: [[97, 98, 99, 100],
	# 			 [98, 99, 100, 101],
	# 			 [99, 100, 101, 102],
	# 			 [100, 101, 102, 103]]
	# Ответ один и тот же:
	# [['-', '+', '*', '+', '*', '+'],
	#  ['+', '-', '*', '-', '*', '-'],
	#  ['+', '*', '+', '-', '+', '*'],
	#  ['-', '*', '-', '+', '-', '*']]


	задача = add_problem(cur, "Чиселбург", 2, 'integer', "На перемене", изображение="during_a_break.jpg", подсказка="В любой день число уроков на один больше числа партий, которые Петя сыграл в этот день.")
	for N, A in [
		(22, 28),
		(32, 38),
		(23, 29),
		(24, 30),
		]:
		desc = f"""На этой неделе Петя был в школе каждый день с понедельника по субботу. Каждую
				перемену между уроками он сыграл одну партию в крестики-нолики с соседом по парте.
				Сколько всего уроков было на этой неделе, если в итоге Петя сыграл {N} партий?"""
		cont = {
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))


	задача = add_problem(cur, "Чиселбург", 2, 'integer', "Вычёркиваем цифры", "Наибольшее число должно начинаться на три тройки.")
	for N, A in [(123123123123123, 33323123), (321321321321321, 33332321), (231231231231231, 33331231), (213213213213213, 33323213)]:
		desc = f"Какое наибольшее число можно получить, вычеркнув 7 цифр из числа {N}?"
		cont = {
			'range': {'min': 10000000, 'max': 99999999},
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))
 #
	# # TODO: Рядом в ряд таблички с цветными буквами, из которых выложено слово КВАНТИК (буквы К одного цвета). Когда игрок нажимает на какую-нибудь букву, она заменяется на окошко, в которое можно ввести цифру.
	# задача = add_problem(cur, "Чиселбург", 2, 'integer', "Ноутик и Квантик развлекаются")
	# for N, A in [(5400, 5943215), (4800, 5843215), (8400, 5873215), (4200, 5743215)]:
	# 	desc = f"Ноутик заменил буквы цифрами в слове КВАНТИК (разным буквам соответствуют разные цифры, одинаковым — одинаковые цифры). Какое наибольшее число могло у него получиться, если произведение его цифр оказалось равно {N}?"
	# 	cont = {
	# 		'correct': A,
	# 	}
	# 	add_variant(cur, задача, desc, json.dumps(cont))
 #
	# задача = add_problem(cur, "Чиселбург", 3, 'integer', "Необычное число")
	# for X, Y, A in [(6, 9, 53999), (9, 3, 49999), (15, 9, 23999), (18, 3, 29999)]:
	# 	desc = f"Напишите пятизначное число, у которого первая цифра в {X} раз меньше суммы всех цифр справа от неё и вторая цифра в {Y} раз меньше суммы всех цифр справа от неё."
	# 	cont = {
	# 		'correct': A,
	# 	}
	# 	add_variant(cur, задача, desc, json.dumps(cont))

	задача = add_problem(cur, "Чиселбург", 4, 'integer', "Магический квадрат", "Сначала рассмотрите две линии из трёх клеток, в которых известны почти все числа и которые пересекаются по клетке <i>x</i>. Приравнивая две суммы, можно определить одно из стёртых чисел. Затем выразите некоторые другие числа через <i>x</i> и составьте уравнение на <i>x</i>, приравняв две суммы.")
	_ = ' '
	x = '<i>x</i>'
	for T, A in [(((_, _, _), (_, 15, _), (18, x, 16)), 11),
				(((_, _, 22), (_, 25, x), (_, _, 26)), 27),
				(((_, _, _), (33, x, 37), (38, _, _)), 35),
				(((_, _, 16), (19, x, 15), (_, _, _)), 17)]:
		table = "<table class=\"number_square\">{0}</table>".format(''.join("<tr>{0}</tr>".format(''.join("<td>{0}</td>".format(cell) for cell in row)) for row in T))
		desc = f"Таблица 3×3, заполненная целыми числами, называется <em>магическим квадратом</em>, если суммы чисел по всем строкам, столбцам и двум главным диагоналям одинаковы. На рисунке ниже изображён магический квадрат, в котором все числа, кроме некоторых, стёрты. Чему равно число, обозначенное как {x}?{table}"
		cont = {
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))
 #
	# задача = add_problem(cur, "Чиселбург", 1, 'radio', "Дни недели")
	# for text, A in [
	# 		("В июне было больше воскресных дней, чем в июле того же года. Каким днём недели было 1 августа этого года?", 4),
	# 		("В апреле было больше четвергов, чем в мае того же года. Каким днём недели было 2 июня этого года?", 2),
	# 		("В сентябре было больше пятниц, чем в октябре того же года. Каким днём недели было 31 октября этого года?", 1),
	# 		("В ноябре было больше суббот, чем в декабре того же года. Каким днём недели было 22 декабря этого года?", 0),
	# 	]:
	# 	desc = text
	# 	cont = {
	# 		'answers': [
	# 			"Понедельник",
	# 			"Вторник",
	# 			"Среда",
	# 			"Четверг",
	# 			"Пятница",
	# 			"Суббота",
	# 			"Воскресенье",
	# 			"Нельзя однозначно определить",
	# 		],
	# 		'correct': A,
	# 	}
	# 	add_variant(cur, задача, desc, json.dumps(cont))

	задача = add_problem(cur, "Чиселбург", 2, 'integer', "Как такое возможно?", изображение="birthday.jpg", подсказка="Такое возможно, если цена книги больше, чем значение, при котором доставка бесплатна, но если применить скидку, то придётся платить за доставку. Пусть <i>х</i> — цена книги. Тогда цена книги со скидкой <nobr>0,9·<i>х</i></nobr>. Составьте уравнение относительно <i>х</i>.")
	for N, M, D, A in [
			(250, 750, 170, 800),
			(300, 800, 214, 860),
			(250, 900, 155, 950),
			(300, 700, 227, 730),
		]:
		desc = f"Стоимость доставки в онлайн-магазине составляет {N} рублей, но если сумма заказа не менее {M} рублей, то доставка бесплатна. И Ваня, и Маша купили с доставкой одну и ту же книгу. Но в честь ее дня рождения, Маше предоставили скидку 10%. Маша была крайне удивлена, обнаружив, что она заплатила на {D} рублей больше, чем Ваня. Какова была цена книги?"
		cont = {
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))

	# задача = add_problem(cur, "Чиселбург", 2, 'integer', "Числовой ребус")
	# for N, A in [(6101, 20), (6505, 24), (9151, 30), (9262, 21)]:
	# 	desc = f"Ненулевые различные цифры A, B, C таковы, что <nobr>C⋅<u>ABAB</u>+<u>CA</u>={N}</nobr>, где запись вида <u>xy</u> обозначает двузначное число, в разряде единиц которого стоит цифра y, а в разряде десятков — x (аналогично, <u>xyzt</u> — четырехзначное число, в разряде единиц которого стоит t, десятков — z, сотен — у, тысяч — x). Чему равно произведение цифр A, B, C?"
	# 	cont = {
	# 		'correct': A,
	# 	}
	# 	add_variant(cur, задача, desc, json.dumps(cont))
 #

def Геома(cur):
	def check_mask(mask, w, h):
		rows = mask.split('\n')
		assert len(rows) == h
		assert all(len(row) == w for row in rows)
		assert all(c in {'x', '-'} for row in rows for c in row)
	swapper = {('\n', '\n'): '\n', ('-', '-'): '-', ('x', '-'): 'x', ('x', 'x'): '-'}

	задача = add_problem(cur, "Геома", 2, 'field', "Раздел участка", "Попробуйте разделить на две фигуры, которые можно совместить при повороте и/или симметрии. Фигуры должны состоять из одинакового числа клеток.")
	for w, h, mask, correct in [
			(5, 4, 'x----\nxxxxx\nxxxxx\nxxxxx', ['x----\nx----\nxxx--\nxxx--']),
			(5, 6, 'x----\nx----\nx----\nxxxxx\nxxxxx\nxxxxx', ['x----\nx----\nx----\nxxx--\nxxx--\n-----']),
			(6, 4, 'x-----\nxxxxx-\nxxxxxx\nxxxxxx', ['x-----\nxxx---\nxxx---\nxx----']),
			(6, 4, '----xx\n--xxxx\nxxxxxx\nxxxxxx', ['------\n--x---\nxxxx--\nxxxx--']),
		]:
		desc = "Двум братьям достался участок земли неправильной формы, схема которого ниже. Братья хотят разделить его на две равные по форме и размеру части. Помогите им это сделать (выделите клетки участка одного из братьев)."
		check_mask(mask, w, h)
		n = mask.count('x')
		for c in correct:
			check_mask(c, w, h)
			assert c.count('x') == n / 2
		inverses = []
		for c in correct:
			inverses.append(''.join(swapper[p] for p in zip(mask, c)))
		cont = {
			'width': w,
			'height': h,
			'mask': mask,
			'corrects': correct + inverses,
		}
		add_variant(cur, задача, desc, json.dumps(cont))

	задача = add_problem(cur, "Геома", 4, 'integer', "Точка на основании", "Постройте правильный треугольник со стороной BM.")
	for N, A in [(4, 13), (5, 16), (6, 19), (7, 22)]:
		desc = f"На основании AC равнобедренного треугольника АВС взяли точку М так, что угол AMB=120°. Оказалось, что AM={N}, BM={N+1}. Найдите AC."
		desc += read_file('geoma3.svg').decode('utf-8')
		cont = {
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))

	задача = add_problem(cur, "Геома", 2, 'perp-lines', "Прямые на клетчатой бумаге", "Пусть чтобы попасть из A в B требуется пройти n клеток вправо и m вверх, а чтобы попасть из C в D требуется пройти m клеток влево и n вверх. Тогда AB и CD перпендикулярны.")
	for points, D in [
		([[7, 1], [6, 6], [6, 3]], [1, 2]),
		([[3, 1], [6, 6], [7, 3]], [2, 6]), 
		([[7, 1], [4, 5], [2, 1]], [6, 4]),
		([[3, 1], [7, 6], [6, 3]], [1, 7])
		]:
		desс = "На клетчатом листе бумаги отметили три узла A, B и C. Отметьте ещё один узел D так, чтобы прямые AB и CD были перпендикулярны."
		cont = {
			'points' : points,
			'correct': D,
		}
		add_variant(cur, задача, desс, json.dumps(cont))


def make_chess_board(data):
	def format_cell(cell):
		if cell in {None, '', ' ', ' '}:
			return ''
		return f'<span class="label">{cell}</span>'
	return '<table class="grid chess">{0}</table>'.format(''.join(
			'<tr>{0}</tr>'.format(''.join(
			'<td>{0}</td>'.format(format_cell(cell))
			for cell in row)) for row in data))


def Головоломск(cur):
	задача = add_problem(cur, "Головоломск", 2, 'glass-bridge', "Стеклянный мост", "Отметьте все клетки из закалённого стекла, а потом уберите лишние.")
	for mask in [[
				[14, 54, 15, 82, 20, 36, 40, 98, 52, 22],
				[63, 68, 31, 96, 28, 10, 84, 45, 28, 15],
				[55, 39, 14, 59, 20, 37, 50, 59, 72, 37],
				[16, 80, 64, 88, 76, 77, 45, 24, 60, 87],
				[31, 39, 68, 73, 57, 51, 48, 14, 53, 93],
				[10, 49, 16, 71, 39, 55, 45, 52, 40, 81],
			], [
				[19, 88, 71, 47, 48, 27, 88, 83, 52, 73],
				[84, 84, 22, 96, 36, 39, 60, 48, 24, 91],
				[77, 87, 86, 46, 60, 46, 55, 65, 36, 14],
				[99, 72, 88, 60, 45, 83, 52, 99, 12, 53],
				[14, 53, 88, 87, 13, 77, 88, 79, 38, 97],
				[41, 35, 16, 61, 67, 43, 92, 44, 84, 92],
			], [
				[26, 48, 41, 31, 32, 68, 80, 71, 27, 37],
				[54, 36, 38, 18, 64, 83, 90, 44, 36, 14],
				[95, 21, 46, 85, 76, 34, 83, 19, 72, 34],
				[48, 80, 52, 88, 40, 10, 76, 52, 27, 51],
				[70, 71, 52, 66, 43, 37, 88, 62, 35, 91],
				[65, 62, 18, 82, 75, 17, 24, 20, 27, 76],
			], [
				[70, 16, 58, 97, 60, 52, 45, 51, 12, 30],
				[72, 96, 86, 24, 96, 50, 20, 27, 36, 73],
				[95, 53, 69, 15, 18, 21, 39, 93, 12, 23],
				[28, 18, 16, 76, 88, 14, 80, 52, 36, 95],
				[77, 49, 56, 42, 30, 55, 28, 25, 86, 13],
				[59, 33, 27, 59, 15, 78, 12, 68, 40, 60],
			]]:
		correct = ['----xxx---\n----x-xxx-\n----x---x-\nxxxxx-xxx-\n------x---\n------xxxx']
		desc = """
Стеклянный мост имеет размеры 6×10 и состоит из стеклянных ячеек 1×1, некоторые из
которых сделаны из закалённого стекла (только они выдерживают вес игрока), а
остальные из обычного. Если вы наступите на ячейку из обычного стекла, то провалитесь.
Вам сообщили, что ячейки, на которых написаны числа кратные 4 или 9, сделаны из
закалённого стекла. Как перейти мост, если перемещаться можно лишь по ячейками,
которые граничат по стороне? Можно выделять клетки в таблице в
процессе решения задачи, но в итоге нужно оставить только клетки вашего
пути."""
		cont = {
			'width': 10,
			'height': 6,
			'mask': mask,
			'corrects': correct,
		}
		add_variant(cur, задача, desc, json.dumps(cont))


	задача = add_problem(cur, "Головоломск", 4, 'integer', "Кони-невидимки", "Сначала рассмотрите угловую клетку, в которой стоит число 2.")
	_ = ' '
	x = '<i>x</i>'
	for T, A in [([[1, _, 2, _, 2], [_, 1, _, _, _], [2, _, x, _, 1], [_, _, _, 3, _], [_, _, 2, _, _]], 3),
				([[_, _, 2, _, _], [_, _, _, 2, _], [2, _, x, _, 1], [_, 1, _, _, _], [2, _, 1, _, _]], 2),
				([[_, _, 1, _, _], [_, _, _, _, _], [1, _, x, _, 2], [_, 2, _, _, _], [_, _, 3, _, 2]], 3),
				([[_, _, 1, _, 2], [_, _, _, _, _], [1, _, x, _, 1], [_, 2, _, _, _], [_, _, 1, _, _]], 0)]:
		table = make_chess_board(T)
		desc = f"На некоторых клетках доски 5×5 стоят невидимые шахматные кони. Числа на рисунке показывают сколько всего коней бьют данную клетку. Какое целое число должно стоять в центре доски? {table}"
		cont = {
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))


def РеспубликаКомби(cur):
	задача = add_problem(cur, "Республика Комби", 1, 'integer', "Непростой выбор", изображение="dif_choice.jpg")
	for subjects, A in [
		("физика, химия, история, информатика, биология, география, английский, литература", 28),
		("физика, химия, история, информатика, биология, география, литература", 21),
		("физика, история, информатика, биология, география, английский", 15),
		("физика, химия, история, обществознание, информатика, биология, география, английский, литература", 36)
	]:
		desc = f"""
				Пете нужно сдавать два обязательных экзамена (математика и русский) и два экзамена на
				выбор. Он хочет выбрать какие-то 2 предмета из следующих: {subjects}. Сколькими
				способами Петя может сделать свой выбор?
				"""
		cont = {
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))



	задача = add_problem(cur, "Республика Комби", 2, 'integer', "Дружба", изображение="friends.jpg", подсказка="Отметим несколько точек, которые обозначают мальчиков, и несколько точек, которые обозначают девочек. Если мальчик и девочка знакомы, то соединим две соответствующие точки отрезком. Теперь общее число отрезков можно посчитать двумя способами и составить уравнение.")
	for desc, A in [
			("В классе 24 ученика. Оказалось, что каждый мальчик дружит с тремя девочками,а каждая девочка с пятью мальчиками. Сколько всего девочек в этом классе?", 9),
			("В классе 28 учеников. Оказалось, что каждый мальчик дружит с тремя девочками, а каждая девочка с четырьмя мальчиками. Сколько всего мальчиков в этом классе?", 16),
			("В классе 27 учеников. Оказалось, что каждый мальчик дружит с пятью девочками, а каждая девочка с четырьмя мальчиками. Сколько всего девочек в этом классе?", 15),
			("В классе 30 учеников. Оказалось, что каждый мальчик дружит с шестью девочками, а каждая девочка с четырьмя мальчиками. Сколько всего мальчиков в этом классе?", 12),
			]:
		cont = {
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))

	задача = add_problem(cur, "Республика Комби", 4, 'integer', "В тире", "На картинке сделаны выстрелы в 8, 9 и 10 очков. Среди них только 8 и 10 не могут стоять рядом (9 отличается от 8 и 10 ровно на единицу). Поэтому любая последовательность выстрелов, удовлетворяющая условию задачи, задается взаимным расположением 8 и 10 (8 раньше 10 или 10 раньше 8), а также количеством девяток левее 8 и 10, между ними и правее них. И, наоборот, можно задать последовательность, поставив сначала все девятки. Далее нужно понять сколькими способами можно поставить 8 и 10 между девятками так, чтобы 8 и 10 не были соседними.")
	img_template = read_file('target.svg').decode('utf-8')
	img_hit = read_file('hit-white.png')
	for hits, A in [
			([(32, 4), (38, -80), (85, -27), (86, 56), (-2, 90), (-80, 64), (-95, -11), (-61, -39), (-98, 148)], 56),
			([(32, 4), (38, -80), (85, -27), (86, 56), (-2, 90), (-80, 64), (-95, -11), (-61, -39), (-45, -91), (-98, 148)], 72),
			([(32, 4), (38, -80), (85, -27), (86, 56), (42, 63), (-2, 90), (-80, 64), (-95, -11), (-61, -39), (-45, -91), (-98, 148)], 90),
			([(32, 4), (38, -80), (85, -27), (86, 56), (42, 63), (-2, 90), (-33, 59), (-80, 64), (-95, -11), (-61, -39), (-45, -91), (-98, 148)], 110),
			]:
		N = len(hits)
		hit_img = 'data:image/png;base64,' + base64.b64encode(img_hit).decode('ascii')
		img = img_template % {'hit-img': hit_img, 'hit-list': ''.join(f'<use href="#hit" x="{x}" y="{y}" />' for x, y in hits)}
		desc = f"""
			Вася сделал {N} выстрелов (на рисунке ниже мишень с результатом), записывая, сколько
			очков он выбивал в процессе. Оказалось, что количество очков для соседних выстрелов
			отличается не более, чем на 1. Например, если бы Вася сделал 8 выстрелов, то корректная
			последовательность очков могла бы быть такой: 9 9 8 9 9 9 10 9. Сколькими способами
			Вася мог добиться итогового результата, соответствующего картинке ниже? Две
			последовательности выстрелов считаются одинаковыми, если соответствующие им
			последовательности полученных очков совпадают.
			{img}
			"""
		cont = {
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))

	задача = add_problem(cur, "Республика Комби", 4, 'integer', "Король и пешки", make_chess_board([['<i>a</i>', '?'], ['<i>b</i>', '<i>c</i>']]) + "Если число способов попасть на три клетки равно <i>a</i>, <i>b</i> и <i>c</i> соответственно, то число способов попасть в правую верхнюю клетку равно <nobr><i>a</i> + <i>b</i> + <i>c</i></nobr>.")
	_ = ' '
	K = '♔'
	p = '♙'
	d = '★'
	for T, A in [([[_, _, _, _, d], [_, p, _, _, p], [_, _, p, _, _], [_, _, _, _, _], [K, _, _, _, _]], 46),
				([[_, _, _, _, d], [_, p, _, p, _], [_, _, _, _, _], [_, _, _, p, _], [K, _, _, _, _]], 76),
				([[_, _, _, _, d], [_, _, _, p, _], [_, p, _, _, _], [_, p, _, _, _], [K, _, _, _, _]], 40),
				([[_, _, _, p, d], [_, _, _, _, _], [_, p, _, _, _], [_, _, p, _, _], [K, _, _, _, _]], 42)]:
		table = make_chess_board(T)
		desc = f"В левом нижнем углу доски 5×5 стоит белый король. Также на доске стоят 3 белые пешки. Сколько различных способов есть у короля дойти до правой верхней клетки доски (помечена ★), если каждым ходом король смещается на одну клетку вправо, вверх или по диагонали вправо-вверх? При этом король не может вставать на одну клетку с пешками. {table}"
		cont = {
			'correct': A,
		}
		add_variant(cur, задача, desc, json.dumps(cont))


def update_positions_town(cur, town, problem_count):
	x0 = 1280 / 2
	y0 = 720 / 2
	R = 300
	base = 0
	if problem_count % 2:
		base = 0.25
		y0 += 0.5 * R * (1 - math.cos(math.pi / problem_count))
	cur.execute("select задача from Задача where город = %s", (town,))
	for k, (problem, ) in enumerate(cur.fetchall()):
		phi = 2 * math.pi * (k / problem_count + base)
		x, y = x0 + R * math.cos(phi), y0 - R * math.sin(phi)
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
			ОстровЛжецов(cur)
			Чиселбург(cur)
			Геома(cur)
			Головоломск(cur)
			РеспубликаКомби(cur)

			update_positions(cur)
