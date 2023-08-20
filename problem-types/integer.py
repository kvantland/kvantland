def entry_form(data):
	attrs = [
		'name="answer"',
		'type="number"',
		'required'
	]
	if lim := data.get('range'):
		if (a := lim.get('min')) != None:
			attrs.append(f'min="{a}"')
		if (b := lim.get('max')) != None:
			attrs.append(f'max="{b}"')
	attrs = ' '.join(attrs)
	yield f'<input {attrs} />'

def validate(data, answer):
	answer = int(answer)
	return answer == data['correct']
