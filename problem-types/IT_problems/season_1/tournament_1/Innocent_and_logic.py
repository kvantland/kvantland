class condition(int):
	def __init__(self, value):
		self.value = value
	def __invert__(self):
		if self.value == 1:
			return 0
		return 1


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
			A = condition(get_nth_bit(i, 0)) # жарко
			B = condition(get_nth_bit(i, 1)) # светит солнце
			C = condition(get_nth_bit(i, 2)) # дует ветер 
			D = condition(get_nth_bit(i, 3)) # идёт дождь
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
			print()
			if user_result != can_go_out:
				return False
		return True
	except:
		return 'Unknown error'