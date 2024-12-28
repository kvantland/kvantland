from problem_xhr import ProblemResponse

def steps(data, params):
	try:
		print('start transfusions check')
		config = data['current_config']
		vessel_from = params['objects']['from']
		vessel_to = params['objects']['to']
		liquid = params['liquid']
		max_height = data['max_height']

		if check_is_number(liquid):
			liquid = int(liquid)
		else:
			return {'answer': "unsuccess"}
		
		if liquid > (max_height - config[vessel_to]) or liquid > config[vessel_from]:
			return {'answer': "unsuccess"}
		
		data['steps_amount'] += 1
		data['current_config'][vessel_to] += liquid
		data['current_config'][vessel_from] -= liquid
		print('success!')
		return ProblemResponse({'answer': 'success', 'data_update': data})
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