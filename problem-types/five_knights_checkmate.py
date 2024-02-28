import sys

def entry_form(data, kwargs):
	height = 8 # число клеточек в столбце
	width = 8 # число клеточек в строке
	line_width = 2 # ширина линий 
	ind = line_width // 2 # отступ
	side = 70 # длина стороны квадрата с границами
	inner_side = side - line_width # длина стороны квадрата без границ 
	board_width = line_width + side * width # длина доски
	board_height = line_width + side * height # ширина доски
	pad = 6 # расстояние между доской и зоной перетаскивания
	plot_width = pad + board_width + inner_side 
	plot_height = board_height
	yield '<input name="answer" type="hidden" />'
	yield '<div class="plot_area">'
	yield f'<svg version="1.1" width="{plot_width}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	for y in range(0, height + 1):
		yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + width * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
	for x in range(0, width + 1):
		yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
	for y in range(0, height):
		for x in range(0, width):
			if (x + y) % 2 == 1:
				yield f'<rect class="orange" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
			else:
				yield f'<rect class="white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
	yield f'<image class="king passive" x="{(data["king_pos"][1] - 1) * side + line_width}" y="{(data["king_pos"][0] - 1) * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/chess/king_b.png" />'
	yield f'<image class="horse passive" x="{(data["horse_pos"][1] - 1) * side + line_width}" y="{(data["horse_pos"][0] - 1) * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/chess/horse_w.png" />'
	
	yield f'<image class="horse passive drag" x="{pad + board_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" href="/static/chess/horse_w.png" />'
	yield f'<image class="horse active" x="{pad + board_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" href="/static/chess/horse_w.png" />'
	yield f'<text style="font-size: {inner_side * 0.2}px" textLength="{inner_side * 0.8}" x="{pad + board_width}" y="{inner_side * 1.2}">Осталось</text>'
	yield f'<text class="amount" style="font-size: {inner_side * 0.2}px" textLength="{inner_side * 0.1}" x="{pad + board_width + inner_side * 0.9}" y="{inner_side * 1.2}"> 4</text>'
	yield f'<image class="reload" x = "{pad + board_width}" y="{plot_height - inner_side}" height="{inner_side}" width="{inner_side}" href="/static/reload.png" />'
	yield '</svg>'
	yield '</div>'

def validate(data, answer):
	ans = list(answer[:-1].split(','))
	ans = ['' if i == "''" else i for i in ans]
	for var in data['correct']:
		tmp = 1
		for i in range(8):
			for j in range(8):
				if str(ans[i * 8 + j]) != str(var[i][j]):
					tmp = 0
		if tmp == 1:
			return True
	return False