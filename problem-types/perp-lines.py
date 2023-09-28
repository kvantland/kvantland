def entry_form(data, kwargs):
	point_names = ['A', 'B', 'C']
	points = data['points']
	yield '<input name="answer" type="hidden" />'
	yield '<div class="plot_area">'
	yield'<svg class="full_window">'
	for i in range(9):
		x = i * 40 + 6
		yield f'<line class="grid_line" x1="{x}" y1="{7}" x2="{x}" y2="{8 * 40 + 6}" />'
	for j in range(9):
		y = j * 40 + 7
		yield f'<line class="grid_line" x1="{6}" y1="{y}" x2="{8 * 40 + 7}" y2="{y}" />'
	for i in range(9):
		for j in range(9):
			if [j, i] in points:
				yield f'<circle class="base_point" cx="{i * 40 + 6}px" cy="{j * 40 + 7}px" />'
			else:
				yield f'<circle class="point" cx="{i *40 + 6}px" cy="{j * 40 + 7}px" />'
	yield'</svg>'
	for i in range(9):
		for j in range(9):
			if [j, i] in points:
				yield f'<div class="point_name" style="top: {j * 40 - 20}px; left: {i * 40 - 20}px"> {point_names[points.index([j, i])]} </div>'
	yield '</div>'

def validate(data, answer):
	correct = ''.join(list(map(str, data['correct'])))
	return answer == correct