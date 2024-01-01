def entry_form(data, kwargs):
	card_height = 60 # высота карт без учета уголков
	card_width = 40 # ширина карт без учета уголков
	pad = 10 # отступы между картами
	r = 5 # радиус скругления краёв карт

	svg_width = len(data['end']) * (card_width + 2 * r) + (len(data['end']) - 1) * pad
	svg_height = card_height + 2 * r
	yield '<input type="hidden" name="answer" />'
	yield f'<svg version="1.1" class="plot_area" width="{svg_width}" height="{svg_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	for card in range(len(data['start'])):
		yield f'<g class="card" transform="translate({card * (card_width + 2 * r + pad)} 0)">'
		yield f"""<path d="
					M 0 {r}
					v {card_height}
					a {r} {r} 0 0 0 {r} {r}
					h {card_width}
					a {r} {r} 0 0 0 {r} {-r}
					v {-card_height}
					a {r} {r} 0 0 0 {-r} {-r}
					h {-card_width}
					a {r} {r} 0 0 0 {-r} {r}"
					/>"""
		yield f'<text x="{card_width / 2 + r}" y="{card_height / 2 + r}"> {data["start"][card]} </text>'
		yield '</g>'
	yield '</svg>'

def validate(data, answer):
	return True