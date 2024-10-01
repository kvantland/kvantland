def steps(step_num, params, data):
	try:
		print(step_num)
		if step_num > data['dron_amount']:
			return {'answer': {'status': "tries out"}}
		left_bottom_item = params['left_bottom_item']
		right_top_item = params['right_top_item']
		if left_bottom_item[0] < right_top_item[0] or left_bottom_item[1] > right_top_item[1]: 
			return {'answer': {'message': "Incorrect selected items"}}
		for row in range(right_top_item[0], left_bottom_item[0] + 1):
			for column in range(left_bottom_item[1], right_top_item[1] + 1):
				data['board'][row][column] = params['color']
		data['search_num'] += 1
		if left_bottom_item[0] >= data['correct'][0] and right_top_item[0] <= data['correct'][0]:
			if left_bottom_item[1] <= data['correct'][1] and right_top_item[1] >= data['correct'][1]:
				data['result'].append("accept")
				return {'answer': {'status': "success"}, 'data_update': data}
		data['result'].append("refuse")
		return {'answer': {'status': "unsuccess"}, 'data_update': data}
		
	except:
		return {'answer': {'message': "Unknown error"}}
	

def validate(data, answer):
	return data['correct'] == answer