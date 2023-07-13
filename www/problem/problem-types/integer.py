def entry_form(data):
	print('<input name="answer" type="number" required />')

def validate(data, answer):
	answer = int(answer)
	return answer == data['correct']
