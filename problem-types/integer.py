import problem

def entry_form(data, kwargs):
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
	yield '<div class="answer_bar">'
	yield 'Введите ответ:'
	yield f'<form method="post" id="problem_form" class="problem answer_area">'
	yield f'<input {attrs} />'
	yield '</form>'
	yield from problem.show_buttons(**kwargs)
	yield '</div>'

def validate(data, answer):
	answer = int(answer)
	return answer == data['correct']

CUSTOM_BUTTONS = True
SAVE_PROGRESS = False
