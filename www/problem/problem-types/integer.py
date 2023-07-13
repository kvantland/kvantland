def entry_form(data):
	print('<input type="number" name="answer" />')

def validate(data, answer):
	answer = int(answer)
	return answer == data['correct']
