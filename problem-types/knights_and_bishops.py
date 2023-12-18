def entry_form(data, kwargs):
	height = data['height'] # число клеточек в столбце
	width = data['width'] # число клеточек в строке
	line_width = 2 # ширина линий 
	ind = line_width // 2 # отступ
	side = 80 # длина стороны квадрата с границами
	inner_side = side - line_width # длина стороны квадрата без границ 
	board_width = line_width + side * width # длина доски
	board_height = line_width + side * height # ширина доски
	pad = 6 # расстояние между доской и зоной перетаскивания
	plot_width = pad + board_width + inner_side 
	plot_height = board_height
	yield '<input name="answer" type="hidden" />'
	yield f'<svg version="1.1" class="plot_area" width="{plot_width}" height="{plot_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
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
	yield f'<image class="horse passive" x="{pad + board_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" href="/static/chess/horse_b.png" />'
	yield f'<image class="horse active" x="{pad + board_width}" y="{line_width}" width="{inner_side}" height="{inner_side}" href="/static/chess/horse_b.png" />'
	yield f'<image class="bishop passive" x="{pad + board_width}" y="{inner_side + line_width * 2}" width="{inner_side}" height="{inner_side}" href="/static/chess/bishop_w.png" />'
	yield f'<image class="bishop active" x="{pad + board_width}" y="{inner_side + line_width * 2}" width="{inner_side}" height="{inner_side}" href="/static/chess/bishop_w.png" />'
	yield f'<image class="reload" x = "{pad + board_width}" y="{plot_height - inner_side}" height="{inner_side}" width="{inner_side}" href="/static/reload.png" />'
	yield '</svg>'

def to_str(a):
	ans = ''
	for i in a:
		ans += ''.join(map(str, i))
	return ans

def validate(data, answer):
	for correct in data['correct']:
		if to_str(correct) == answer:
			return True
	return False

