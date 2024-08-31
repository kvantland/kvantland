def description(params):
	return '''
		Мальчик Иннокентий очень любит школьные уроки информатики, потому научился мыслить только в терминах логических выражений. 
		Иннокентий также очень любит гулять на улице, однако Мама Иннокентия, Мария Ивановна, сформулировала правило, 
		когда ему разрешается выходить на улицу (не удивляйтесь, мама Иннокентия тоже учила логику, но в гуманитарном университете): 
		Иннокентий может выйти погулять в следующих случаях:
		<ul style="padding-left: 40px; margin-top: 1em; margin-bottom: 1em;">
			<li>если за окном жарко, то на улицу можно выйти если светит солнце и нет дождя и ветра одновременно</li>
			<li>если же за окном не жарко, то на улицу можно выйти если светит солнце или нет ветра, но если светит<
			солнце и нет ветра одновременно, то Иннокентию лучше остаться дома.</li>
		</ul>
		Помогите Иннокентию составить логическое выражение, которое должно быть истинным тогда и только тогда, когда ему можно выходить на прогулку. 
		Вам доступны операции “и”, “или”, “не”, “”
		'''

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