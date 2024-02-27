import sys

def entry_form(data, kwargs):
	names = {
	'here': 'Приз лежит здесь',
	'no': 'Здесь приза нет',
	'near': 'Приз в соседней шкатулке'
	}
	yield '<div class="row">'
	num = 1
	for name in data['tmp']:
		yield '<div class="column">'
		yield f'<img class="casket" tmp="1" num="{num}" src="/static/casket/empty_1.png" />'
		yield f'<div class="name"> {names[name]} </div>'
		yield '</div>'
		num += 1
	yield '</div>'

def steps(step_num, params, data):
	if step_num > 1:
		return {'answer': 'no'}
	print(data['correct'], params['answer'], file=sys.stderr)
	if int(data['correct']) == int(params['answer']):
		return {'answer': 'true', 'user_answer': params['answer'], 'answer_correct': True, 'solution': params['solution_full']}
	else:
		return {'answer': 'false', 'user_answer': params['answer'], 'answer_correct': False, 'solution': params['solution_empty']}

def validate(data, answer):
	return int(data['correct']) == int(answer)

HINT_ONLY = True