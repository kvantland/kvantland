def _shore(content=None):
	yield '<td class="pad land">'
	if content:
		yield '<span class="label">'
		yield str(content)
		yield '</span>'

def _river_row(w, text=''):
	yield '<tr class="pad">'
	yield from _shore()
	yield f'<td class="water" colspan="{w}">{text}'
	yield from _shore()

def entry_form(data):
	mask = data['mask']
	assert len(mask) == data['height']

	yield '<table class="grid glass-bridge">'
	yield from _river_row(data['width'])
	for y, row in enumerate(mask):
		assert len(row) == data['width']
		yield '<tr>'
		yield from _shore('→')
		for x, cell in enumerate(row):
			if cell != None:
				yield '<td class="tile">'
				yield '<span class="label">'
				yield str(cell)
				yield '</span>'
			else:
				yield '<td>'
		yield from _shore('→')
	yield from _river_row(data['width'], "Река")
	yield '</table>'

def validate(data, answer):
	answer = '\n'.join(answer.split())
	return answer in data['corrects']
