import json

def entry_form(data, kwargs):
	w, h = data['width'], data['height']
	switches = data['switches']
	yield '<table class="grid">'
	for y in range(h):
		yield '<tr>'
		for x in range(w):
			yield f'<td id="lamp_{x}_{y}" class="lamp lamp_on">'
	yield '</table>'
	yield '<div class="lamp_bar">'
	for k, switch in enumerate(switches):
		yield '<div>'
		yield '<table class="grid">'
		assert len(switch) == h
		for y, row in enumerate(switch):
			assert len(row) == w
			yield '<tr>'
			for x, val in enumerate(row):
				classes = 'lamp'
				if val:
					classes += ' lamp_on'
				yield f'<td id="lamp_{x}_{y}" class="{classes}">'
		yield '</table>'
		yield f'<button type="button" class="lamp_switch" data-id="{k}">{k + 1}</button>'
		yield '</div>'
	yield '</div>'
	yield f"""
		<script type="text/ecmascript">
			"use strict"
			const w = {w}
			const h = {h}
			const switches = {json.dumps(switches)}
		</script>
		"""
	yield f'<form method="post" id="problem_form" class="button_bar">'
	yield '<input id="i_answer" type="hidden" name="answer" >'

def validate(data, answer):
	answer = json.loads(answer)
	return answer in data['correct']
