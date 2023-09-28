def entry_form(data, kwargs):
	point_names = ['A', 'B', 'C']
	points = data['points']
	yield '<input name="answer" type="hidden" />'
	yield '<div class="plot_area">'
	yield '<table class="plot">'
	yield '<tbody class="plot_body">'
	for i in range(8):
		yield '<tr class="plot_row">'
		for j in range(8):
			yield '<td class="square"></td>'
		yield '</tr>'
	yield '</tbody>'
	yield '</table>'
	yield'<svg class="full_window">'
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