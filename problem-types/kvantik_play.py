def entry_form(data, kwargs):
	in_column = 2
	in_row = 7
	side = 105
	line_width = 2
	ind = line_width / 2
	inner_side = side - line_width 
	board_width = line_width + in_row * side 
	board_height = line_width + in_column * side
	point_r = 20

	yield '<input name="answer" type="hidden" />'
	yield '<div class="plot_area">'
	yield f'<svg version="1.1" width="{board_width}" height="{board_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	for y in range(1, in_column + 1):
		yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + in_row * side}" y2="{ind + y * side}" stroke-width="{line_width}"/>'
	for x in range(0, in_row + 1):
		yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind + side}" x2="{ind + x * side}" y2="{ind + in_column * side}" stroke-width="{line_width}"/>'
	for y in range(0, 1):
		for x in range(0, in_row):	
			yield f'<text class="field color{x}" x="{x * side + side / 2}" y="{(y + 1) * side - side / 2}" width="{inner_side}" height="{inner_side}">{data['word'][x]}</text>'
	for y in range(1, 2):
		for x in range(0, in_row):	
			yield f'<foreignObject x="{x * side + line_width}" y="{y * side + line_width}" width="{inner_side}" height="{inner_side}">'
			yield f'<div xmlns="http://www.w3.org/1999/xhtml">'
			yield f'<input class="fieldinput" type="number" maxlength="1">'
			yield f'</div>'
			yield f'</foreignObject>'
	yield '</svg>'
	yield '</div>'

def validate(data, answer):
	return data['correct'] == int(answer)