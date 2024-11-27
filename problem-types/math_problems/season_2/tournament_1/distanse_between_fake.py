def steps(step_num, params, data): 
	print('==========================')
	print()
	print()
	try:
		if data['weightings_amount'] <= 0:
			return {'answer': {'message': "Ваши попытки закончились!"}}
		true_weight = 1000
		fake_weight = 1
		weights = params['weights']
		alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

		right_mass = 0
		left_mass = 0
		history_item = {'left': [], 'right': []}

		print('correct start params')

		for weight in weights['left']:
			weight_index = weight['rowNum'] * 5 + weight['itemNum']
			print(weight_index)
			history_item['left'].append(alph[weight_index])
			is_fake = int(weight_index) in data['correct']
			if is_fake:
				left_mass += fake_weight
			else:
				left_mass += true_weight

		print(left_mass)
		
		for weight in weights['right']:
			weight_index = weight['rowNum'] * 5 + weight['itemNum']
			print(weight_index)
			history_item['right'].append(alph[weight_index])
			is_fake = int(weight_index) in data['correct']
			if is_fake:
				right_mass += fake_weight
			else:
				right_mass += true_weight

		print(right_mass)

		data['weightings_amount'] -= 1
		if not ('history' in data.keys()):
			data['history'] = []
		
		if right_mass > left_mass:
			data['history'].append(f"({', '.join(history_item['left'])}) < ({', '.join(history_item['right'])})")
			return {'answer': {'move_side': "right"}, 'data_update': data}
		elif right_mass < left_mass:
			data['history'].append(f"({', '.join(history_item['left'])}) > ({', '.join(history_item['right'])})")
			return {'answer': {'move_side': "left"}, 'data_update': data}
		else:
			data['history'].append(f"({', '.join(history_item['left'])}) = ({', '.join(history_item['right'])})")
			return {'answer': {'move_side': "equal"}, 'data_update': data}
	except:
		return {'answer': {'message': "Unknown error"}}
	
def validate(data, answer):
	print('correct check function!')
	try:
		position_1 = data['correct']['position_1']
		position_2 = data['correct']['position_2']
		return abs(position_2 - position_1) - 1 == int(answer)
	except:
		return False