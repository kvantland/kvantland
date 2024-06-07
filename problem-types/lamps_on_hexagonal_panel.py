import sys

def validate(data, answer):
	#print('check!', file=sys.stderr)
	try:
		lamps_in_row = data['lamps_in_line']
		side = data['side']
		if len(answer) != side * 2 - 1:
			return False
		#print('here 1', file=sys.stderr)
		for row in range(len(answer)):
			if 2 * side - 1 - abs(side - 1 - row) != len(answer[row]):
				return False
		#print('here 2', file=sys.stderr)
		for row in range(len(answer)):
			lamps_amount = 0
			for lamp in answer[row]:
				#print(lamp, file=sys.stderr)
				if int(lamp) != 1 and int(lamp) != 0:
					return False
				if int(lamp) == 1:
					lamps_amount += 1
			#print(lamps_amount, lamps_in_row, file=sys.stderr)
			if lamps_amount != lamps_in_row:
				#print('not approved', file=sys.stderr)
				return False
		#print('here 3', file=sys.stderr)
		num = 0
		while num < 2 * side - 1:
			y = (num - side + 1) * (num >= side)
			lamps_amount = 0
			while y < min(2 * side - 1, side + num):
				x = num - (y - side + 1) * (y >= side)
				#print(y, x, file=sys.stderr)
				if int(answer[y][x]) == 1:
					lamps_amount += 1
				y += 1
			#print(lamps_amount, file=sys.stderr)
			if lamps_amount != lamps_in_row:
				return False
			num += 1
		#print('here 4', file=sys.stderr)
		num = 0
		while num < 2 * side - 1:
			y = (num - side + 1) * (num >= side)
			lamps_amount = 0
			while y < min(2 * side - 1, side + num):
				curr_side = 2 * side - 1 - abs(y - (side - 1))
				x = curr_side - (num - (y - side + 1) * (y >= side)) - 1
				#print(y, x, file=sys.stderr)
				if int(answer[y][x]) == 1:
					lamps_amount += 1
				y += 1
			#print(lamps_amount, file=sys.stderr)
			if lamps_amount != lamps_in_row:
				return False
			num += 1
		#print('here 5', file=sys.stderr)
		return True
	except:
		return False