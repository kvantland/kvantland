def entry_form(data, kwargs):
	point_names = ['A', 'B', 'C']
	points = data['points']
	yield '<div class="plot_area">'
	yield '<div class="plot">'
	for i in range(8):
		yield '<div class="plot_row">'
		for j in range(8):
			yield '<div class="square"></div>'
		yield '</div>'
	yield '</div>'
	yield'<svg class="full_window">'
	for i in range(9):
		for j in range(9):
			if [j, i] in points:
				yield f'<circle class="base_point" cx="{i *40.8 + 6}px" cy="{j * 40.8 + 6}px" />'
			else:
				yield f'<circle class="point" cx="{i *40.8 + 6}px" cy="{j * 40.8 + 6}px" />'
	yield'</svg>'
	for i in range(9):
		for j in range(9):
			if [j, i] in points:
				yield f'<div class="point_name" style="top: {j *40.8 - 20}px; left: {i * 40.8 - 20}px"> {point_names[points.index([j, i])]} </div>'
	yield '</div>'

def validate(data, answer):
	correct = ''.join(list(map(str, data['correct'])))
	return answer == correct