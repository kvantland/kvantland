def entry_form(data, kwargs):
	in_column = len(data['correct'])
	in_row = len(data['correct'][0])
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
			yield f'<rect class="grass" x="{x * side + line_width}" y ="{y * side + line_width}" width="{inner_side}" height="{inner_side}"/>'
			if (data['correct'][y][x] == -1):
				yield f'<image class="ground" choiced="-1" x="{x * side + line_width}" y ="{y * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/problem_assets/house.png" />'
			else:	
				yield f'<image class="ground field not_choiced" choiced="0" x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}" href="/static/problem_assets/dwarf.png"/>'
	yield '</svg>'
	yield '</div>'

def validate(data, answer):
	ans = list(map(int, answer[:-1].split(',')))
	print(ans)
	a = [ans[0:6], ans[6:12], ans[12:18], ans[18:24], ans[24:]]
	for x in range(len(a)):
		for y in range(len(a[0])):
			cnt = 0
			if (y > 0 and a[x][y] == a[x][y-1]):
				cnt += 1
			if (y + 1 < len(a[0]) and a[x][y] == a[x][y+1]):
				cnt += 1
			if (x > 0 and a[x][y] == a[x-1][y]):
				cnt += 1
			if (x + 1 < len(a) and a[x][y] == a[x+1][y]):
				cnt += 1
			if (a[x][y] == 1 and cnt != 2):
				return False
			if (a[x][y] == 0 and cnt ==2):
				return False
	return True