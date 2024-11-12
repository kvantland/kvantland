
def validate(data, answer): 
	print('=====================')
	print()
	print()
	print('here!')
	try:
		if not check_configuration_possibility(answer, data):
			return False
		print('configuration check passed!')

		for row in range(len(answer)):
			for column in range(len(answer[row])):
				figure_type = answer[row][column]['type']
				print(row, column, figure_type)
				if not check_figure(figure_type, row, column, answer):
					return False

		return True
	except:
		return False


def check_figure(figure_type, row, column, board):
	if figure_type == '':
		return True
	
	if figure_type == 'rook_b':
		for check_row in range(len(board)):
			if check_row == row: continue
			if board[check_row][column]['type'] != '':
				return False
		for check_column in range(len(board)):
			if check_column == column: continue
			if board[row][check_column]['type'] != '':
				return False
		return True
	
	if figure_type == 'bishop_w':
		for add in range(-min(row, column), min(7 - row, 7 - column) + 1):
			if add == 0: continue
			check_row = row + add
			check_column = column + add
			if board[check_row][check_column]['type'] != '':
				return False
		for add in range(-min(7 - column, row), min(7 - row, column)):
			if add == 0: continue
			check_row = row + add
			check_column = column - add
			if board[check_row][check_column]['type'] != '':
				return False
		return True


def check_configuration_possibility(answer, data):
	active_rooks_amount = 0
	active_bishops_amount = 0
	pasive_rooks_amount = 0
	print('start config check')

	for row in range(len(answer)):
		for column in range(len(answer[row])):
			figure_type = answer[row][column]['type']
			figure_move_status = answer[row][column]['moveStatus']
			print(row, column, figure_type, figure_move_status)

			if figure_type == '':
				continue

			elif figure_type == 'bishop_w' and figure_move_status == 'active':
				active_bishops_amount += 1

			elif figure_type == 'rook_b' and figure_move_status == 'active':
				active_rooks_amount += 1

			elif figure_type == 'rook_b' and figure_move_status == 'passive':
				if [row, column] in data['positions']:
					pasive_rooks_amount += 1
				else:
					return False
				
			else:
				return False
			
	print('bishops amount: ', active_bishops_amount)
	print('active rooks amount: ', active_rooks_amount)
	print('passive rooks amount: ', pasive_rooks_amount)
	
	if active_bishops_amount != 4 or active_rooks_amount != 4:
		return False
	if pasive_rooks_amount != 2:
		return False
	return True