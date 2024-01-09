import problem

def show_answer_area(data, clas, kwargs, value='',):
	if clas == 'with_input':
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
		attrs.append(f'value="{value}"')
		attrs = ' '.join(attrs)

		yield '<div class="answer_bar with_input">'
		yield 'Введите ответ:'
		yield f'<form method="post" id="problem_form" class="problem answer_area">'
		yield f'<input {attrs} />'
		yield '</form>'
		yield from problem.show_buttons(**kwargs)
		yield '</div>'
	if clas == 'hint_only':
		yield '<div class="answer_bar hint_only">'
		yield from problem.show_hint_button(**kwargs)
		yield '</div>'
	if clas == 'without_input':
		yield '<div class="answer_bar without_input">'
		yield from problem.show_buttons(**kwargs)
		yield '</div>'
