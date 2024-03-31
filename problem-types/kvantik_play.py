def entry_form(data, kwargs):
	in_column = 2
	in_row = 7
	side = 64
	line_width = 2
	ind = line_width / 2
	inner_side = side - line_width 
	board_width = line_width + in_row * side 
	board_height = line_width + in_column * side
	point_r = 20

	yield '<input name="answer" type="hidden" />'
	yield '<div class="plot_area">'
	yield '<div class="flex_box">'
	yield '<div class="row">'
	for x in range(0, in_row):
		yield f'<div class="field color{x}">{data['word'][x]}</div>'
	yield '</div>'
	yield '<div class="row">'
	for x in range(0, in_row):
		yield f'<div class="field">'
		yield f'<input class="fieldinput" type="text" min="0" max="9" maxlength="1">'
		yield f'</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'

def validate(data, answer):
	return data['correct'] == int(answer)