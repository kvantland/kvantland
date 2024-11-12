def validate(data, answer):
	try:
		print('========================')
		print('here!')
		print(answer)
		print(data['correct'])
		return int(answer) == int(data['correct'])
	except:
		return False