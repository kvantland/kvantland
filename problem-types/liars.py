def entry_form(data, kwargs):
	attrs = [
		'id="answer"',
		'name="answer"',
		'type="text"',
		'required'
	]

	yield '<svg id="playground">'
	yield '<g id="layer_table"></g>'
	yield '<g id="layer_persons"></g>'
	yield '<g id="layer_ui"></g>'
	yield '<g id="layer_dnd"></g>'
	yield '</svg>'

	yield f'<input id="i_answer" type="text" name="answer" />'
	yield '<script type="text/ecmascript">'
	yield '"use strict";'
	yield f"const N = {data['chairs']};"
	yield 'const R = 0.5 * r * N;'
	yield 'const R_table = R - 1.5 * r;'
	yield 'const R_outer = R + 1.5 * r;'
	yield 'const table_x = R_outer;'
	yield 'const table_y = R_outer;'
	yield 'var sidebar_x = 2 * R_outer + 0.5 * r;'
	yield 'var sidebar_y = 0;'
	yield '</script>'


def validate(data, answer):
	return answer in data['correct']
