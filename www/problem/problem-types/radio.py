def entry_form(data):
	print('<ul>')
	for k, answer in enumerate(data['answers']):
		print(f'<li><label><input name="answer" type="radio" required value="{k}" />{answer}</label></li>')
	print('</ul>')

def validate(data, answer):
	answer = int(answer)
	return answer == data['correct']
