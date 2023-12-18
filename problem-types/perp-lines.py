def entry_form(data, kwargs):
	point_names = ['A', 'B', 'C']
	points = data['points']
	yield '<input name="answer" type="hidden" />'
	yield '<div class="plot_area" style="margin-top: 30px">'
	yield'<svg version="1.1" class="full_window" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	for i in range(9):
		x = i * 40 + 6
		yield f'<line class="grid_line" x1="{x}" y1="{7}" x2="{x}" y2="{8 * 40 + 6}" />'
	for j in range(9):
		y = j * 40 + 7
		yield f'<line class="grid_line" x1="{6}" y1="{y}" x2="{8 * 40 + 6}" y2="{y}" />'
	for i in range(9):
		for j in range(9):
			if [j, i] in points:
				yield f'<circle class="base_point" cx="{i * 40 + 6}px" cy="{j * 40 + 7}px" />'
			else:
				yield f'<circle class="point" cx="{i *40 + 6}px" cy="{j * 40 + 7}px" />'
	for i in range(9):
		for j in range(9):
			if [j, i] in points:
				yield f'<text y="{j * 40}" x="{i * 40 - 20}"> {point_names[points.index([j, i])]} </text>'
			if [j, i] not in points:
				yield f'<text class="invisible" y="{j * 40}" x="{i * 40 - 20}"> D </text>'
	yield'</svg>'
	yield '</div>'

def validate(data, answer):
	correct = ''.join(list(map(str, data['correct'])))
	return answer == correct