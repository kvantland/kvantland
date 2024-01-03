def entry_form(data, kwargs):
	icon_side = 40 # сторона иконок интерфейса
	card_height = 60 # высота карт без учета уголков
	card_width = 40 # ширина карт без учета уголков
	pad = 10 # отступы между картами
	r = 5 # радиус скругления углов карт
	reload_side = 60 # размер кнопки сброса
	reload_pad = 20 # отступ до кнопки сброса

	svg_width = len(data['end']) * (card_width + 2 * r) + (len(data['end']) - 1) * pad + reload_pad + reload_side
	svg_height = card_height + 2 * r + 1.5 * icon_side
	yield '<input type="hidden" name="answer" />'
	yield f'<svg version="1.1" class="plot_area" width="{svg_width}" height="{svg_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield f'<g class="exchange_bar hidden" bar_width="{icon_side * 2.5}">'
	yield f'<image class="icon exchange" width="{icon_side}" height="{icon_side}" href="/static/exchange_icon.png"/>'
	yield f'<image class="icon cross" x="{icon_side * 1.5}" width="{icon_side}" height="{icon_side}" href="/static/cross_icon.png">'
	yield '</g>'
	for card in range(len(data['cur'])):
		yield f'<g class="card" num="{card}" card_width="{card_width + 2 * r}" transform="translate({card * (card_width + 2 * r + pad)} {icon_side * 1.5})">'
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
		yield f'<text x="{card_width / 2 + r}" y="{card_height / 2 + r}"> {data["cur"][card]} </text>'
		yield '</g>'
	yield f'<image class="reload" width="{reload_side}" height="{reload_side}" transform="translate({svg_width - reload_side} {icon_side * 1.5})" href="/static/reload.png">'
	yield '</svg>'

def steps(step_num, params, data):
	resp = {}
	squares = [1, 4, 9, 16]
	try:
		selected = list(map(int, params['selected'].split()))
		if sum(selected) in squares:
			ind_1 = data['cur'].index(selected[0])
			ind_2 = data['cur'].index(selected[1])
			data['cur'][ind_1] = selected[1]
			data['cur'][ind_2] = selected[0]
			resp['answer'] = 'accepted'
			resp['data_update'] = data
		else:
			resp['answer'] = 'rejected'
	except KeyError:
		resp['answer'] = "OK"
		data['cur'] = data['start']
		resp['data_update'] = data
	return resp


def validate(data, answer):
	return data['cur'] == data['end']