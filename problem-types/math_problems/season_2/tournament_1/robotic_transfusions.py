from email.policy import default


def steps(step_num, params, data):
	try:
		print('start transfusions check')
		config = data['current_config']
		vessel_from = params['objects']['from']
		vessel_to = params['objects']['to']
		liquid = params['liquid']
		max_height = data['max_height']
		print('from: ', vessel_from, 'to: ', vessel_to, 'liquid: ', liquid)

		if check_is_number(liquid):
			liquid = int(liquid)
			print('correct input!')
		else:
			return {'answer': "unsuccess"}
		
		if liquid > (max_height - config[vessel_to]) or liquid > config[vessel_from]:
			return {'answer': "unsuccess"}
		
		print('correct liquid amount!')
		
		data['steps_amount'] += 1
		data['current_config'][vessel_to] += liquid
		data['current_config'][vessel_from] -= liquid
		print('success!')
		return {'answer': 'success', 'data_update': data}
	except:
		return {'answer': "unsuccess"}


def check_is_number(string):
	try:
		if '.' in string:
			return False
		try:
			int(string)
			return True
		except:
			return False
	except:
		return False


def validate(data, answer):
	try:
		default_liquid = data['current_config'][0]
		for liquid in data['current_config']:
			if liquid != default_liquid:
				return False
		if data['correct'] != data['steps_amount']:
			return False
		return True
	except:
		return False