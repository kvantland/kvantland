import random


def steps(step_num, params, data):
	try:
		if params['moveObject'] == "farmer":
			print('farmer')
			move_position = params['moveTo']
			if move_position['x'] < 0 or move_position['x'] >= data['board_width']:
				return {'answer': {'status': "not allowed"}}
			if move_position['y'] < 0 or move_position['y'] >= data['board_height']:
				return {'answer': {'status': "not allowed"}}
			if abs(move_position['y'] - data['farmer_coordinates'][0]) + abs(move_position['x'] - data['farmer_coordinates'][1]) != 1:
				return {'answer': {'status': "not allowed"}}
			data['farmer_coordinates'][0] = move_position['y']
			data['farmer_coordinates'][1] = move_position['x']
			data['remaining_moves'] -= 1
			print('move to: ', data['farmer_coordinates'])
			print(data['farmer_coordinates'], data['cockerel_coordinates'])
			return {'answer': {'status': "allowed"}, 'data_update': data}
		
		elif params['moveObject'] == "cockerel":
			print('cockerel')
			if data['farmer_coordinates'] == data['cockerel_coordinates']:
				return {
					'answer': {'status': "you win!"}, 
					'user_answer': 'catch!', 
					'solution': params['solution'],
					'answer_correct': True,
					'data_update': data
					}
			if data['remaining_moves'] == 0:
				return {
					'answer': {'status': "you lose"},
					'user_answer': "no catch",
					'solution': params['solution'],
					'answer_correct': False,
					'data_update': data
				}
			cockerel_coordinates = data['cockerel_coordinates']
			farmer_coordinates = data['farmer_coordinates']
			good_possible_coordinates = []
			bad_possible_coordinates = []
			movements = [[0, 1], [1, 0], [-1, 0], [0, -1]]

			for movement in movements:
				new_cockerel_coordinates = [cockerel_coordinates[0] + movement[0], cockerel_coordinates[1] + movement[1]]
				if new_cockerel_coordinates[0] >= 0 and new_cockerel_coordinates[0] < data['board_height']:
					if new_cockerel_coordinates[1] >= 0 and new_cockerel_coordinates[1] < data['board_width']:
						new_distanse = get_distanse(new_cockerel_coordinates, farmer_coordinates)
						if new_distanse > 1:
							good_possible_coordinates.append(new_cockerel_coordinates)
						else:
							bad_possible_coordinates.append(new_cockerel_coordinates)

			print(good_possible_coordinates, bad_possible_coordinates)
			if len(good_possible_coordinates) > 0:
				new_cockerel_coordinates = random.choice(good_possible_coordinates)
			else:
				new_cockerel_coordinates = random.choice(bad_possible_coordinates)
			
			print('move to: ', new_cockerel_coordinates)
			data['cockerel_coordinates'] = new_cockerel_coordinates
			return {'answer': {'status': "allowed"}, 'data_update': data}
	except:
		return {'answer': {'status': "Unknown error"}}
	

def get_distanse(first_coordinates, second_coordinates):
	x_distanse = abs(first_coordinates[1] - second_coordinates[1])
	y_distanse = abs(first_coordinates[0] - second_coordinates[0])
	return x_distanse + y_distanse