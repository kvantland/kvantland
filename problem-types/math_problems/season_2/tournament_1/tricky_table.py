def validate(data, answer):
	try:
		number = data['numberValue'] # число, которое обязательно должно быть в таблице
		flag = False # флаг, показывающий, есть ли число в пользовательском ответе
		uniqueCheckSet = set() # множество, проверяющее уникальность каждого элемента
		row_multiplicity = [1, 1, 1]
		column_multiplicity = [1, 1, 1]

		print()
		print()
		print('======================')

		print(len(answer))
		if len(answer) != 3:
			return False
		print('here 1')
		for row in range(len(answer)):
			if len(answer[row]) != 3: return False
			for column in range(len(answer[row])):
				uniqueCheckSet.add(int(answer[row][column]))
				row_multiplicity[row] *= int(answer[row][column])
				column_multiplicity[column] *= int(answer[row][column])
				if int(answer[row][column]) == int(number):
					flag = True

		if not(flag):	return False
		if len(uniqueCheckSet) != 9: return False

		print('number exists!')
		print(row_multiplicity)
		print(column_multiplicity)
		
		if len(set(row_multiplicity) | set(column_multiplicity)) != 1:
			return False
		
		return True
	except:
		return False