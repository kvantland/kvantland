def entry_form(data, kwargs):
	width = data['n'] # число клеточек в строке
	height = data['m'] # число строк в таблице
	line_width = 3 # ширина линий 
	ind = line_width // 2 # отступ
	side = 70 # длина стороны квадрата с границами
	inner_side = side - line_width # длина стороны квадрата без границ 
	board_width = line_width + side * width # ширина доски
	board_heigth = line_width + side * height # высота доски
	pad = 20 # расстояние между доской и зоной перетаскивания
	plot_width = pad + board_width + inner_side 
	plot_height = board_heigth
	yield '<input name="answer" type="hidden" />'
	yield f'<svg version="1.1" class="plot_area" width="{plot_width}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	for y in range(0, height + 1):
		yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + width * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
	for x in range(0, width + 1):
		yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
	for y in range(0, height):
		for x in range(0, width):
			yield f'<rect class="white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'

	yield f'<image class="tree passive" x="{pad + board_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" href="/static/tree.png" />'
	yield f'<image amount="1" class="tree active" x="{pad + board_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" href="/static/tree.png" />'
	yield f'<image class="reload" x = "{pad + board_width}" y="{plot_height - inner_side}" height="{inner_side}" width="{inner_side}" href="/static/reload.png" />'
	yield '</svg>'

def validate(data, answer):
	ans = list(map(int, answer[:-1].split(',')))
	check = data['correct']
	n = data['n']
	m = data['m']
	for variant in check:
		tmp = 1
		for i in range(m):
			for j in range(n):
				if variant[i][j] != ans[i * n + j]:
					tmp = 0
				if not tmp:
					break
			if not tmp:
				break
		if tmp:
			return True
	return False