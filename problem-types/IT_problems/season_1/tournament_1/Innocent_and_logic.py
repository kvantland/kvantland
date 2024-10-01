def validate(data, answer):
	try:
		translation = data['translation']
		expression = ""
		if len(answer) > 10 ** 3:
			return False
		for block in answer:
			if not('text' in block.keys()):
				return False
			print(block['text'])
			if block['text'] not in translation.keys():
				return {'answer': "incorrect block text"}
			else:
				expression += translation[block['text']]
		print('translated user expression: ', expression)
		
		def get_nth_bit(num, n):
			return (num >> n) % 2
		
		vars_amount = len(data['blocks'])
		for i in range(0, 1 << vars_amount):
			A = get_nth_bit(i, 0)
			B = get_nth_bit(i, 1)
			C = get_nth_bit(i, 2)
			D = get_nth_bit(i, 3)
			can_go_out = False
			for variant in data['correct']:
				result = eval(variant)
				print(variant, ': ', A, B, C, D, ': ', result)
				if result:
					can_go_out = True
					break
			try:
				user_result = eval(expression)
			except:
				return False
			print(expression, ': ', A, B, C, D, ': ', user_result)
			if user_result != can_go_out:
				return False
		return True
	except:
		return 'Unknown error'