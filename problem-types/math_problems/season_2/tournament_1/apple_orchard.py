def validate(data, answer):
	try:
		print('===================')
		print()
		print('start checkout')
		if len(answer) != 9:
			print('incorrect items amount')
			return False
		
		left_up_corner = {'x': 1000, 'y': 1000}
		right_bottom_corner = {'x': 0, 'y': 0}
		for item in answer:
			left_up_corner['x'] = min(left_up_corner['x'], item[1])
			left_up_corner['y'] = min(left_up_corner['y'], item[0])
			right_bottom_corner['x'] = max(right_bottom_corner['x'], item[1])
			right_bottom_corner['y'] = max(right_bottom_corner['y'], item[0])
		print('left up: ', left_up_corner)
		print('right bottom: ', right_bottom_corner)

		tree_amount = 0
		for x in range(left_up_corner['x'], right_bottom_corner['x'] + 1):
			for y in range(left_up_corner['y'], right_bottom_corner['y'] + 1):
				if not([y, x] in answer):
					print('not in square: ', x, y)
					return False
				if data['orchard_config'][y][x]:
					tree_amount += 1
		
		print('tree amount: ', tree_amount)
		return tree_amount == data['apple_amount']
	except:
		return False