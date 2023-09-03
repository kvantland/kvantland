def entry_form(data, kwargs):
	mask = data['mask'].split('\n')
	assert len(mask) == data['height']

	yield '<table class="grid field">'
	for y, row in enumerate(mask):
		assert len(row) == data['width']
		yield '<tr>'
		for x, cell in enumerate(row):
			yield '<td class="tile">' if cell == 'x' else '<td>'
	yield '</table>'

def validate(data, answer):
	answer = '\n'.join(answer.split())
	return answer in data['corrects']
