def validate(data, answer):
	print(answer)
	print(data['correct'])
	try: 
		return list(map(str, data['correct'])) == answer
	except:
		return False