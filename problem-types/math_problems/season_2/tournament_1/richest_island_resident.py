def validate(data, answer):
	try:
		print(answer)
		return data['correct'] == answer
	except:
		return False