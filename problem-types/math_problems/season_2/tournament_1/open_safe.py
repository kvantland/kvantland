def validate(data, answer):
	try:
		print(answer)
		return data['correct'] == answer
		return True
	except:
		return False