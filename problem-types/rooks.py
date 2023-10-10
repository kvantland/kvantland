import sys

def entry_form(data, kwargs):
	ind = 0.5
	side = 80
	yield '<input name="answer" type="hidden" />'
	yield '<div class="plot_area">'
	yield '<div class="board_zone">'
	yield '<svg class="full_window">'
	for y in range(0, 5):
		yield f'<line class="grid_line" x1="{ind}" y1 = "{ind + y * side}" x2="{ind + 4 * side}" y2="{ind + y * side}" />'
	for x in range(0, 5):
		yield f'<line class="grid_line" x1="{ind + x * side}" y1 = "{ind}" x2="{ind + x * side}" y2="{ind + 4 * side}" />'
	for x in range(0, 4):
		for y in range(0, 4):
			if (x + y) % 2 == 1:
				yield f'<rect class="brown" x="{x * side + 2 * ind}" y="{y * side + 2 * ind}" width="{side - 2 * ind}" height="{side - 2 * ind}" />'
			else:
				yield f'<rect class="white" x="{x * side + 2 * ind}" y="{y * side + 2 * ind}" width="{side - 2 * ind}" height="{side - 2 * ind}" />'
			if [y, x] in data['cur']:
					yield f'<image x="{x * side + 2 * ind}" y ="{y * side + 2 * ind}" width="{side - 2 * ind}" height="{side - 2 * ind}" href="/static/rook.png" />"'
	yield '</svg>'
	yield '</div>'
	yield '<div class="drag_zone">'
	for i in range(2):
		yield '<div class="rook">'
		yield '</div>'
	yield '<div class="rook_amount">'
	yield '<p> Осталось&nbsp&nbsp </p>'
	yield '<p id="amount"> 2 </p>'
	yield '</div>'
	yield '<div class="reload">'
	yield '</div>'
	yield '</div>'
	yield '</div>'

def validate(data, answer):
	correct = data['correct']
	ans = list(answer.split(' '))
	print(ans, file=sys.stderr)
	for i in correct:
		print(ans, file=sys.stderr)
		if sorted(i) == sorted(ans):
			return True
	return False