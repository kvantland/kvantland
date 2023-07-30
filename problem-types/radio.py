def entry_form(data):
	yield '<ul>'
	for k, answer in enumerate(data['answers']):
		yield f'<li><label><input name="answer" type="radio" required value="{k}" />{answer}</label></li>'
	yield '</ul>'

def validate(data, answer):
	answer = int(answer)
	return answer == data['correct']
