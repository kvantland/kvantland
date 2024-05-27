import json

MARGIN = 0.2

def render_lamp_array(w: int, h: int, extra_attrs):
	off = MARGIN

	yield f'<svg class="grid" width="{2 * off + w}em" height="{2 * off + h}em">'
	for y in range(h):
		for x in range(w):
			attrs = ' '.join(f'{key}="{value}"' for key, value in extra_attrs(x, y).items())
			yield f'<rect {attrs} x="{off + x}em" y="{off + y}em" width="1em" height="1em" />'
	yield '</svg>'

def entry_form(data, kwargs):
	w, h = data['width'], data['height']
	switches = data['switches']
	yield '<div class="real_lamps">'
	yield from render_lamp_array(w, h, lambda x, y: {'id': f"lamp_{x}_{y}", 'class': "lamp lamp_on"})
	yield '</div>'
	yield '<div class="lamp_bar">'
	for k, switch in enumerate(switches):
		yield '<div>'
		yield from render_lamp_array(w, h, lambda x, y: {'class': "lamp lamp_on" if switch[y][x] else "lamp"})
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
