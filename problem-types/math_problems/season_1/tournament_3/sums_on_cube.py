import sys

def entry_form(data, kwargs):
	arr = [data['a'], data['b'], data['c']]
	arr.sort()
	name = '_'.join(map(str, arr))
	yield '<div class="cont">'
	yield f'<img class="cube" src="/static/problem_assets/sums_on_cube/sums_on_cube_{name}.svg" />'
	yield '</div>'

def validate(data, answer):
	print(data['correct'], answer, file=sys.stderr)
	return int(answer) == int(data['correct'])

CUSTOM_BUTTONS = True
HYBRID = True