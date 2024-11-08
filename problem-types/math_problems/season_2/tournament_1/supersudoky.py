import json


def validate(data, answer):
	try:
		print()
		print()
		print('====================')
		print(json.dumps(answer))
		figure_numbers = dict()
		row_numbers = dict()
		column_numbers = dict()

		n = len(data['plot']) # plot side
		check_set = set([str(i) for i in range(1, n + 1)])

		for row_num in range(len(data['plot'])):
			for column_num in range(len(data['plot'][row_num])):
				color = data['plot'][row_num][column_num]
				answer_number = str(answer[row_num][column_num])
				# print(color, answer_number, row_num, column_num)

				if color in figure_numbers.keys():
					figure_numbers[color].append(answer_number)
				else:
					figure_numbers[color] = [answer_number]

				if row_num in row_numbers.keys():
					row_numbers[row_num].append(answer_number)
				else:
					row_numbers[row_num] = [answer_number]

				if column_num in column_numbers.keys():
					column_numbers[column_num].append(answer_number)
				else:
					column_numbers[column_num] = [answer_number]
				
		for numbers in figure_numbers.values():
			if set(numbers) != check_set:
				return False
		print('figures correct!')
		for numbers in row_numbers.values():
			if set(numbers) != check_set:
				return False
		print('rows correct!')
		for numbers in column_numbers.values():
			if set(numbers) != check_set:
				return False
			
		return True
	except:
		return False
	

	