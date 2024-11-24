def validate(data, answer):
	print(answer)
	print(data['correct'])
	try: 
		return set(map(str, data['correct'])) == set(answer)
	except:
		return False