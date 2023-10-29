import sys

def entry_form(data, kwargs):
	size = 4 # число клеточек в строке
	line_width = 2 # ширина линий 
	ind = line_width // 2 # отступ
	side = 80 # длина стороны квадрата с границами
	inner_side = side - line_width # длина стороны квадрата без границ 
	board_side = line_width + size * side # длина стороны доски
	pad = 6 # расстояние между доской и зоной перетаскивания
	plot_width = pad + board_side + inner_side 
	plot_height = board_side
	yield '<input name="answer" type="hidden" />'
	yield f'<svg class="plot_area" width="{plot_width}" height="{plot_height}" overflow="visible">'
	for y in range(0, size + 1):
		yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + size * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
	for x in range(0, size + 1):
		yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + size * side}" stroke-width="{line_width}"/>'
	for x in range(0, size):
		for y in range(0, size):
			if (x + y) % 2 == 1:
				yield f'<rect class="brown" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
			else:
				yield f'<rect class="white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
			if [y, x] in data['cur']:
					yield f'<image class="rook passive choiced" x="{x * side + line_width}" y ="{y * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/rook.png" />'
	for i in range(2):
		yield f'<image class="rook active" x="{pad + board_side}" y="0" width="{inner_side}" height="{inner_side}" href="/static/rook.png" />'
	yield f'<text style="font-size: {inner_side * 0.2}" textLength="{inner_side * 0.8}" x="{pad + board_side}" y="{inner_side * 1.2}">Осталось</text>'
	yield f'<text class="amount" style="font-size: {inner_side * 0.2}" textLength="{inner_side * 0.1}" x="{pad + board_side + inner_side * 0.9}" y="{inner_side * 1.2}"> 2</text>'
	yield f'<image class="reload" x = "{pad + board_side}" y="{plot_height - inner_side}" height="{inner_side}" width="{inner_side}" href="/static/reload.png" />'
	yield '</svg>'

def validate(data, answer):
	correct = data['correct']
	ans = list(answer.split(' '))
	print(sorted(ans), file=sys.stderr)
	for i in correct:
		print(sorted(i), file=sys.stderr)
	for i in correct:
		if sorted(i) == sorted(ans):
			return True
	return False