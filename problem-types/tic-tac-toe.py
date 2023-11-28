def entry_form(data, kwargs):
	mask = data['mask']
	width = 3 # число клеточек в строке
	height = 3 # число строк в таблице
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
	yield f'<svg class="plot_area" width="{plot_width}" height="{plot_height}" overflow="visible">'
	for y in range(0, height + 1):
		yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + width * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
	for x in range(0, width + 1):
		yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + height * side}" stroke-width="{line_width}"/>'
	for y in range(0, height):
		for x in range(0, width):
			if mask[y][x] == 0:
				yield f'<rect class="occupied white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
				yield f'<text x="{x * side + line_width + side / 2}" y="{y * side + line_width + side / 2}"> 0 </text>'
			elif mask[y][x] == 1:
				yield f'<rect class="occupied white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
				yield f'<text x="{x * side + line_width + side / 2}" y="{y * side + line_width + side / 2}"> ❌ </text>'
			else:
				yield f'<rect class="free white" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
	yield '</svg>'

def validate(data, answer):
	for variant in data['correct']:
		y, x = variant
		if str(y * 3 + x) == answer:
			return True
	return False