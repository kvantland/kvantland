def validate(data, answer):
	try:
		translatesX = [0, 0, -1, 0, -1, -1]
		startConfig = data['honeycombsConfig']
		amount = 0

		if len(answer) != len(startConfig):	return False
		for row in range(len(answer)):
			if len(answer[row]) != len(startConfig[row]): return False
			for column in range(len(answer[row])):
				if answer[row][column]:	amount += 1
				if startConfig[row][column] == '':
					continue
				print('number!')
				filled_combs_near = 0

				if row > 0:
					prev_row = answer[row - 1]
					translate = -translatesX[row]
					if column + translate - 1 >= 0 and column + translate - 1 < len(prev_row):
						if prev_row[column + translate - 1]:
							filled_combs_near += 1
							print('up left')
					if column + translate >= 0 and column + translate < len(prev_row):
						if prev_row[column + translate]:
							filled_combs_near += 1
							print('up right')

				if row < len(answer) - 1:
					next_row = answer[row + 1]
					translate = translatesX[row + 1]
					if column + translate >= 0 and column + translate < len(next_row):
						if next_row[column + translate]:
							filled_combs_near += 1
							print('bottom left')
					if column + translate + 1 >= 0 and column + translate + 1 < len(next_row):
						if next_row[column + translate + 1]:
							filled_combs_near += 1
							print('bottom right')
					
				if column > 0:
					if answer[row][column - 1]:
						filled_combs_near += 1
						print('left')

				if column + 1 < len(answer[row]):
					if answer[row][column + 1]:
						filled_combs_near += 1
						print('right')
				
				print(filled_combs_near, row, column, startConfig[row][column])
				if startConfig[row][column] != filled_combs_near:
					return False
		if amount == data['amount']:
			return True
		else:
			return False
	except:
		return False