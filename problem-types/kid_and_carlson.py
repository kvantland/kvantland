def entry_form(data, kwargs):
	in_column = len(data['field'])
	in_row = len(data['field'][0])
	side = 70
	line_width = 3
	ind = line_width / 2
	inner_side = side - line_width 
	board_width = line_width + in_row * side 
	board_height = line_width + in_column * side
	point_r = 20

	yield '<input name="answer" type="hidden" />'
	yield '<div class="plot_area">'
	yield f'<svg version="1.1" width="{board_width}" height="{board_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	for y in range(0, in_column + 1):
		yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + in_row * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
	for x in range(0, in_row + 1):
		yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + in_column * side}" stroke-width="{line_width}"/>'
	for y in range(0, in_column):
		for x in range(0, in_row):
			yield f'<rect class="cake not_choiced" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" />'
			if data['field'][y][x] == 1:
				yield f'<image class="point"  x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/problem_assets/cherry.svg" />'
	yield '</svg>'
	yield '</div>'

def validate(data, answer):
	ans = list(map(int, answer[:-1].split(',')))
	for var in data['correct']:
		cnt, tmp = (0, 1)
		for i in range(len(var)):
			for j in range(len(var[0])):
				if ans[cnt] != var[i][j]:
					tmp = 0
				cnt += 1
		if tmp:
			return True
	return False