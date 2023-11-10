import problem

def entry_form(data, kwargs):
	size = len(data['table'][0]) # число клеточек в строке
	line_width = 3 # ширина линий 
	ind = line_width // 2 # отступ
	side = 70 # длина стороны квадрата с границами
	inner_side = side - line_width # длина стороны квадрата без границ 
	board_side = line_width + size * side # длина стороны доски
	pad = 20 # расстояние между доской и зоной перетаскивания
	plot_width = pad + board_side + inner_side 
	plot_height = board_side
	yield f'<svg class="plot_area" width="{plot_width}" height="{plot_height}" overflow="visible">'
	for y in range(0, size + 1):
		yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + size * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
	for x in range(0, size + 1):
		yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + size * side}" stroke-width="{line_width}"/>'
	for x in range(0, size):
		for y in range(0, size):
			if data['table'][y][x] != '_':
				if (x + y) % 2 == 1:
					yield f'<rect class="occupied orange" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
				else:
					yield f'<rect class="occupied white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
				if data['table'][y][x] != 'x':
					yield f'<text x="{x * side + line_width + inner_side // 2}" y ="{y * side + line_width + inner_side // 2}">{data["table"][y][x]}</text>'
				else:
					yield f'<image class="horse rejected passive" x="{x * side + line_width}" y ="{y * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/rejected_horse.png" />'
			else:
				if (x + y) % 2 == 1:
					yield f'<rect class="orange" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
				else:
					yield f'<rect class="white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
	yield f'<image class="horse allowed passive" x="{pad + board_side}" y="{line_width}" width="{inner_side}" height="{inner_side}" href="/static/horse.png" />'
	yield f'<image class="horse rejected passive" x="{pad + board_side}" y="{inner_side + line_width * 2}" width="{inner_side}" height="{inner_side}" href="/static/rejected_horse.png" />'
	yield f'<image class="horse allowed active" x="{pad + board_side}" y="{line_width}" width="{inner_side}" height="{inner_side}" href="/static/horse.png" />'
	yield f'<image class="horse rejected active" x="{pad + board_side}" y="{inner_side + line_width * 2}" width="{inner_side}" height="{inner_side}" href="/static/rejected_horse.png" />'
	yield f'<image class="reload" x = "{pad + board_side}" y="{plot_height - inner_side}" height="{inner_side}" width="{inner_side}" href="/static/reload.png" />'
	yield '</svg>'
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