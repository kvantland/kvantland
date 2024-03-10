def entry_form(data, kwargs):
	match_length = 60  #длина спички
	match_width = 7  #ширина спички
	match_width_ = 11 #ширина картинки спички
	pad_ = (match_width_ - match_width) / 2  # сдвиг между картинкой и тенью
	match_length_ = 60 # длина картинки спички
	full_match = match_length + match_width  # длина с отступом для удобства
	full_match_ = match_length_ + match_width_  # длина картинки с отступом для удобства
	num_height = match_length * 2 + match_width * 3  #высота цифр
	num_width = match_length + match_width * 2  #ширина цифр
	symb_pad = 25  #отступ между символами в выражении
	margin = {'left': 20, 'top': 30, 'right': 20, 'bottom': 30}  #общие отступы
	num_amount = len(data['nums'])
	sgn_amount = len(data['sgn'])
	symb_amount = sgn_amount + num_amount
	view_box = {
		'height': num_height + margin['top'] + margin['bottom'],
		'width': num_width * num_amount + 
				sgn_amount * match_length + 
				symb_pad * (symb_amount - 1) + 
				margin['left'] + margin['right']
	}
	grid = [
		['hor', match_width, 0, match_length, match_width],
		['vert', 0, match_width, match_width, match_length],
		['vert', full_match, match_width, match_width, match_length],
		['hor', match_width, full_match, match_length, match_width],
		['vert', 0, full_match + match_width, match_width, match_length],
		['vert', full_match, full_match + match_width, match_width, match_length],
		['hor', match_width, full_match * 2, match_length, match_width]
	]  # общая разметка rect под цифры

	num_grid = [
		{'x':  match_width - pad_, 'y': match_width, 'width': match_width_, 'height': match_length_, 'transform': f'rotate(-90 {match_width} {match_width})'},
		{'x': -pad_, 'y': match_width, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(0)'},
		{'x': full_match - pad_, 'y': match_width, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(0)'},
		{'x':  match_width - pad_, 'y': full_match + match_width, 'width': match_width_, 'height': match_length_, 'transform': f'rotate(-90 {match_width} {match_width + full_match})'},
		{'x': -pad_, 'y': full_match + match_width, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(0)'},
		{'x': full_match - pad_, 'y': full_match + match_width, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(0)'},
		{'x':  match_width - pad_, 'y': full_match * 2 + match_width, 'width': match_width_, 'height': match_length_, 'transform': f'rotate(-90 {match_width} {full_match * 2 + match_width})'},
	]


	sgn_grid = {
		'-': [{'x': -match_width_ / 2, 'y': -match_length_ / 2, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(90)'}],
		'+': [
				{'x': -match_width_ / 2, 'y': -match_length_ / 2, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(90)'},
				{'x': -match_width_ / 2, 'y': -match_length_ / 2, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(0)'}
			],
		'*': [
				{'x': -match_width_ / 2, 'y': -match_length_ / 2, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(135)'},
				{'x': -match_width_ / 2, 'y': -match_length / 2, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(45)'}
			],
		'=': [
				{'x': -match_width_ / 2, 'y': -match_length_ / 2, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(90) translate(-15 0)'},
				{'x': -match_width_ / 2, 'y': -match_length_ / 2, 'width': match_width_, 'height': match_length_, 'transform': 'rotate(90) translate(15 0)'}
			]
	}  # разметка знаков

	translate = {
		0: [0, 1, 2, 4, 5, 6],
		1: [2, 5],
		2: [0, 2, 3, 4, 6],
		3: [0, 2, 3, 5, 6],
		4: [1, 2, 3, 5],
		5: [0, 1, 3, 5, 6],
		6: [0, 1, 3, 4, 5, 6],
		7: [0, 2, 5],
		8: [0, 1, 2, 3, 4, 5, 6],
		9: [0, 1, 2, 3, 5, 6]
	}  # индексы rect для отрисовки всех цифр

	yield f'<svg version="1.1" width="{view_box["width"]}" height="{view_box["height"]}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	
	cur_dist = 0
	yield f'<g class="field" transform="translate({margin["left"]} {margin["top"]})">'
	for num_ind in range(num_amount):
		yield f'<g class="num" transform="translate({cur_dist + symb_pad * (num_ind > 0)} {0})">'
		cur_dist += symb_pad * (num_ind > 0) + num_width
		for ind in range(len(grid)):
			yield f'<rect direction="{grid[ind][0]}" ind="{ind}" x="{grid[ind][1]}" y="{grid[ind][2]}" width="{grid[ind][3]}" height="{grid[ind][4]}" />'
		for ind in translate[data['nums'][num_ind]]:
			rect = num_grid[ind]
			yield f"""<image href="/static/assets/match.svg" 
							x="{rect["x"]}" y="{rect["y"]}" 
							width="{rect["width"]}" 
							height="{rect["height"]}" 
							preserveAspectRatio="none" 
							transform="{rect["transform"]}"/>"""
		yield '</g>'
		if (num_ind < sgn_amount):
			yield f'<g class="sgn" type="{data["sgn"][num_ind]}" transform="translate({cur_dist + match_length / 2 + symb_pad} {num_height / 2})">'
			for rect in sgn_grid[data['sgn'][num_ind]]:
				yield f"""<image href="/static/assets/match.svg" 
							x="{rect["x"]}" y="{rect["y"]}" 
							width="{rect["width"]}" 
							height="{rect["height"]}" 
							preserveAspectRatio="none" 
							transform="{rect["transform"]}"/>"""
			yield '</g>'
			cur_dist += symb_pad + match_length
	yield '</g>'
	yield '</svg>'