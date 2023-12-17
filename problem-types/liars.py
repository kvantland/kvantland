def entry_form(data, kwargs):
	attrs = [
		'id="answer"',
		'name="answer"',
		'type="text"',
		'required'
	]

	r_chair = 32
	r_person = 36
	n_chairs = data['chairs']
	r_base = 0.5 * r_chair * n_chairs
	r_table = r_base - 1.5 * r_chair
	r_outer = r_base + 1.5 * r_chair
	D_persons = 3 * r_person
	x_persons = 2 * r_base + 4 * r_chair + 0.5 * D_persons
	y_persons = 0.5 * D_persons

	yield f"""
		<svg id="playground" height="{2 * r_outer}px">
			<g id="layer_table">
				<circle class="table" r="{r_table}" cx="{r_outer}" cy="{r_outer}">
			</g>
			<g id="layer_persons"></g>
			<g id="layer_ui"></g>
			<g id="layer_dnd"></g>
		</svg>

		<input id="i_answer" type="hidden" name="answer" minlength="{n_chairs}" >

		<script type="text/ecmascript">
			"use strict"
			const N = {n_chairs}
			const R = {r_base}
			const table_x = {r_outer}
			const table_y = {r_outer}
			const D_persons = {D_persons}
			const x_persons = {x_persons}
			const y_persons = {y_persons}
		</script>
		"""


def validate(data, answer):
	return answer in data['correct']
