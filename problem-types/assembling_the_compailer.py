def validate(data, answer):
	try:
		if len(answer) > data['max_lines_amount']:
			return False
		print('user_answer: ', answer)

		def vasya_function(a, b, c):
			return a - b // 4 + 63 * c
		
		tests = [
			[1, 0, 0],
			[0, 4, 0],
			[0, 0, 1],
			[5, 0, 0],
			[1, 4, 0],
			[1, 0, 4],
			[4, 1, 0],
			[0, 5, 0],
			[0, 1, 4],
			[4, 0, 1],
			[0, 4, 1],
			[0, 0, 5],
			[64, 76, 86],
			]
		nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

		for test in tests:
			print('test: ', test)
			operands = {
					'A': test[0],
					'B': test[1],
					'C': test[2],
					'D': None,
					'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '0': 0
				}
			
			default_function_result = vasya_function(test[0], test[1], test[2])
			for block in answer:
				if 'type' not in block.keys():
					return False
				if 'firstInputValue' not in block.keys():
					return False
				if 'secondInputValue' not in block.keys():
					return False
				block_type = block['type']
				first_field = block['firstInputValue']
				second_field = block['secondInputValue']
				if block_type not in data['blockTypes']:
					return False
				if first_field not in ['A', 'B', 'C', 'D', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
					return False
				if second_field not in ['A', 'B', 'C', 'D']:
					return False
				
				if block_type == 'Add':
					if operands[second_field] != None and operands[first_field] != None:
						operands[second_field] += operands[first_field]
				if block_type == 'Sub':
					if operands[second_field] != None and operands[first_field] != None:
						operands[second_field] -= operands[first_field]
				if block_type == 'ShiftLeft':
					if operands[second_field] != None and operands[first_field] != None:
						operands[second_field] *= 2 ** operands[first_field]
				if block_type == 'ShiftRight':
					if operands[second_field] != None and operands[first_field] != None:
						operands[second_field] = operands[second_field] // (2 ** operands[second_field])
				if block_type == 'Move':
					operands[second_field] = operands[first_field]

				print(block_type, first_field, second_field, 'result: ', operands[first_field], operands[second_field])

			print('final: ', operands['A'], default_function_result)
			if operands['A'] != default_function_result:
				return False
		return True
	except:
		return False