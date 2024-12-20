def validate(data, answer):
	try:
		start_white = data['startConfig']['white']
		start_black = data['startConfig']['black']
		count = {'white': 0, 'black': 0}

		if answer[start_white[0]][start_white[1]] != {'type': 'horse_w', 'moveStatus': 'passive'}:
			return False
		if answer[start_black[0]][start_black[1]] != {'type': 'horse_b', 'moveStatus': 'passive'}:
			return False
		
		print('start config check approved!')

		for row in range(8):
			for column in range(8):
				beaten_type = None
				if answer[row][column]['type'] == 'horse_b': 
					beaten_type = 'horse_w'
					count['black'] += 1
				elif answer[row][column]['type'] == 'horse_w':
					beaten_type = 'horse_b'
					count['white'] += 1
				
				if beaten_amount(row, column, answer, beaten_type) != 4 and beaten_type != None:
					return False
		
		print('beaten amount check approved!')
		
		if count['white'] != count['black']:
			return False
		
		print('equal amount check approved!')
 
		return True
	except:
		return False
	

def beaten_amount(row, column, board, beaten_type):
	print('check beaten amount: ', row, column, beaten_type)
	moves = [
		[1, 2], [-1, 2], [-1, -2], [1, -2], 
		[2, 1], [2, -1], [-2, 1], [-2, -1]
		]
	amount = 0

	for move in moves:
		target = [row  + move[0], column + move[1]]
		if target[0] > 0 and target[0] < 8 and target[1] > 0 and target[1] < 8:
			if board[target[0]][target[1]]['type'] == beaten_type:
				amount += 1
	
	print('beaten amount: ', amount)
	return amount