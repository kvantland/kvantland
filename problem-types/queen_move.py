from collections import deque
from random import choice


def steps(step_num, params, data):
	try:

		def possible_coordinates(y, x, board_side):
			return y >= 0 and y < board_side and x >= 0 and x < board_side
		
		def can_reach_plus(start_x, start_y, canceled_positions, stop_positions, markup):
			diractions = [ [-1, 1], [-1, 0], [0, 1] ]
			for diraction in diractions:
				current_y, current_x = [start_y + diraction[0], start_x + diraction[1]]
				while possible_coordinates(current_y, current_x, board_side):
					if [current_y, current_x] in stop_positions:
						break
					if [current_y, current_x] not in canceled_positions and markup[current_y][current_x] == '+':
						return {'status': True, 'position': [current_y, current_x]}
					current_y += diraction[0]
					current_x += diraction[1]
			return {'status': False}
		
		def printt(arr):
			for row in arr:
				print(row, end='\n')

		board_config = data['horse_config']
		board_side = len(board_config)
		possible_positions = []
		stop_positions = []
		canceled_positions = []
		queen_y, queen_x = data['queen_position']

		horse_moves = [ [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1] ]
		for y in range(board_side):
			for x in range(board_side):
				if board_config[y][x] == 'H':
					stop_positions.append([y, x])
					for move in horse_moves:
						canceled_positions.append([y + move[0], x + move[1]])

		diractions = [ [-1, 1], [-1, 0], [0, 1] ]
		for diraction in diractions:
			current_y, current_x = [queen_y + diraction[0], queen_x + diraction[1]]
			while possible_coordinates(current_y, current_x, board_side):
				if [current_y, current_x] in stop_positions:
					break
				if [current_y, current_x] not in canceled_positions:
					possible_positions.append([current_y, current_x])
				current_y += diraction[0]
				current_x += diraction[1]

		if 'check' in params.keys():
			print('check!')
			print(possible_positions)
			if len(possible_positions) == 0:
				return {'answer': {'message': "you lose!"}, 'answer_correct': False, 'user_answer': [queen_y, queen_x], 'solution': params['solution']}
				
		if params['turn'] == 'player':
			if data['turn'] != 'player':
				return {'answer': {'status': "not accepted", 'message': "incorrect turn"}}
			else:
				data['turn'] = 'computer'
			if [params['row'], params['column']] in possible_positions:
				data['queen_position'] = [params['row'], params['column']]
				print('accepted movement')
				return {'answer': {'status': "accepted", 'turn': "player"}, 'data_update': data}
			else:
				print('not accepted movement')
				return {'answer': {'status': "Impossible movement"}}
			
		elif params['turn'] == 'computer':
			if data['turn'] != 'computer':
				return {'answer': {'status': "not accepted", 'message': "incorrect turn"}}
			else:
				data['turn'] = 'player'
			if len(possible_positions) == 0:
				return {'answer': {'message': "you won!"}, 'answer_correct': True,  'user_answer': [queen_y, queen_x], 'solution': params['solution']}
			print('here_0')
			markup = [[' ' for i in range(board_side)] for j in range(board_side)]
			markup[0][9] = '+'
			print('!')
			for y in range(board_side):
				for x in range(board_side - 1, -1, -1):
					if y == 0 and x == board_side - 1:
						continue
					if [y, x] in canceled_positions:
						continue
					if [y, x] in stop_positions:
						markup[y][x] = 'H'
						continue
					if can_reach_plus(x, y, canceled_positions, stop_positions, markup)['status']:
						markup[y][x] = '-'
					else:
						markup[y][x] = '+'

			printt(markup)
			print(queen_x, queen_y)
			if markup[queen_y][queen_x] == '+':
				new_position = choice(possible_positions)
				prev_position = data['queen_position']
				data['queen_position'] = new_position
				return {'answer': {'status': "accepted", 'row': new_position[0], 'column': new_position[1], 'prev_position': prev_position, 'turn': "computer"}, 'data_update': data}
			elif markup[queen_y][queen_x] == '-':
				new_position = can_reach_plus(queen_x, queen_y, canceled_positions, stop_positions, markup)['position']
				print(new_position, queen_x, queen_y)
				prev_position = data['queen_position']
				data['queen_position'] = new_position
				return {'answer': {'status': "accepted", 'row': new_position[0], 'column': new_position[1], 'prev_position': prev_position, 'turn': "computer"}, 'data_update': data}
			else:
				return {'answer': {'status': "Impossible start position"}}
		else:
			return {'answer': {'status': "Incorrect request"}}
	except:
		return {'answer': {'status':"Unknown error"}}