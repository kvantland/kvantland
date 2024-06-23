def validate(data, answer):
	converted = [str(num) for num in answer]
	result_string = ''.join(converted)
	return result_string in data['correct']