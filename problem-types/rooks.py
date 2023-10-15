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
	yield f'<div class="plot_area" style="width: {plot_width}px; height: {plot_height}px">'
	yield f'<div class="board_zone" style="width: {board_side}px; padding-right: {pad}px">'
	yield f'<svg class="full_window" style="width: {board_side}; height: {board_side}">'
	for y in range(0, size + 1):
		yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + size * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
	for x in range(0, size + 1):
		yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + size * side}" stroke-width="{line_width}"/>'
	for x in range(0, size):
		for y in range(0, size):
			if (x + y) % 2 == 1:
				yield f'<rect class="brown" x="{x * side + 2 * ind}" y="{y * side + 2 * ind}" width="{inner_side}" height="{inner_side}" />'
			else:
				yield f'<rect class="white" x="{x * side + 2 * ind}" y="{y * side + 2 * ind}" width="{inner_side}" height="{inner_side}" />'
			if [y, x] in data['cur']:
					yield f'<image x="{x * side + 2 * ind}" y ="{y * side + 2 * ind}" width="{side - 2 * ind}" height="{side - 2 * ind}" href="/static/rook.png" />"'
	yield '</svg>'
	yield '</div>'
	yield f'<div class="drag_zone" style="width: {inner_side}px">'
	for i in range(2):
		yield f'<div class="rook" style="width: {inner_side}px; height: {inner_side}px">'
		yield '</div>'
	yield f'<div class="rook_amount" style="width: {inner_side}px; margin-top: {inner_side}px; font-size: {inner_side * 0.19}px">'
	yield '<p> Осталось </p>'
	yield '<p id="amount"> 2 </p>'
	yield '</div>'
	yield f'<div class="reload" style="width: {inner_side}px; height: {inner_side}px">'
	yield '</div>'
	yield '</div>'
	yield '</div>'

def validate(data, answer):
	correct = data['correct']
	ans = list(answer.split(' '))
	for i in correct:
		if sorted(i) == sorted(ans):
			return True
	return False