import sys

def entry_form(data, kwargs):
	full_width, full_height = (1000, 600) # размеры поля без учета кнопки reload
	shore_width, shore_height = (200, 600)
	sea_width, sea_height = (1000, 600)
	dwarf_width, dwarf_height = (80, 95)
	bag_width, bag_height = (80, 95)
	rel_width, rel_height = (50, 50) # размеры кнопки reload
	shore_pad = {'left':(shore_width - dwarf_width * 2) // 4, 'top': 5}
	add = 10 # прибавка к left_pad
	obj_amount = 6 # количесто юнитов на берегу
	boat_width, boat_height = (200, 200)
	boat_name = ['0_0', '0_1', '1_0', '1_1', '2_0', '3_0']

	yield '<div class="full_problem">'
	yield '<input type="hidden" name="answer" />'
	yield f"""<svg 
				version="1.1" 
				preserveAspectRatio="xMidYMid meet" 
				viewBox="0 0 {full_width + rel_width} {full_height}" 
				width="{full_width + rel_width}"
				overflow="visible" 
				xmlns="http://www.w3.org/2000/svg" 
				xmlns:xlink="http://www.w3.org/1999/xlink">"""

	yield f'<svg width="{full_width}" height="{full_height}" >'
	yield f'<image class="sea" height="{sea_height}" dx="{-sea_width}" dy="0" transform="translate({-sea_width} 0)" href="/static/problem_assets/sea.svg" />'
	yield '</svg>'
	boat_translate = {'left': shore_width - full_width + shore_width + boat_width, 'right': 0}
	yield f'<g class="boat" dx="{boat_translate[data["side"]]}" dy="0" side="{data["side"]}" transform="translate({boat_translate[data["side"]]} 0)">'
	yield f"""<rect class="boat grid" width={boat_width} height="{boat_height}"
				side="{data["side"]}"
				dwarf="0" bag="0"
				x="{full_width - shore_width - boat_width}"
				y="{(full_height - boat_height) / 2}" />"""
	for name in boat_name:
		if name == '0_0':
			yield f"""<image class="boat {name} cur" width={boat_width} height="{boat_height}"
						x="{full_width - shore_width - boat_width}"
						y="{(full_height - boat_height) / 2}"
						href="/static/problem_assets/boat_with_dwarf/boat_{name}.png" />"""
		else:
			yield f"""<image class="boat {name}" width={boat_width} height="{boat_height}"
						x="{full_width - shore_width - boat_width}"
						y="{(full_height - boat_height) / 2}"
						href="/static/problem_assets/boat_with_dwarf/boat_{name}.png" />"""
	yield '</g>'
	yield '<g class="shore" side="left">'
	yield f'<image height="{shore_height}" width="{shore_width}" href="/static/problem_assets/left_shore.svg" />'
	yield f'<g class="obj" side="left" transform="translate({shore_pad["left"] - add} {shore_pad["top"]})">'
	pos, cur_height = (0, 0)
	for rect in range(obj_amount):
		yield f"""<rect class="grid" width="{dwarf_width}" height="{dwarf_height}"
					pos="{pos}" side="left"
					x="{(pos % 2 == 1) * dwarf_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}"/>"""
		pos += 1
		cur_height += dwarf_height

	pos, cur_height = (0, 0)
	for dwarf in range(data['conf']['left']['dwarf']):
		yield f"""<image class="active dwarf" width="{dwarf_width}" height="{dwarf_height}"
					pos="{pos}" side="left" 
					href="/static/problem_assets/dwarf.png"
					x="{(pos % 2 == 1) * dwarf_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}"" />"""
		pos += 1
		cur_height += dwarf_height
	for bag in range(data['conf']['left']['bag']):
		yield f"""<image class="active bag" width="{bag_width}" height="{bag_height}" 
					pos="{pos}" side="left" 
					href="/static/problem_assets/money_bag.png"
					x="{(pos % 2 == 1) * bag_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}" />"""
		pos += 1
		cur_height += bag_height

	yield '</g>'
	yield '</g>'
	yield f'<g class="shore" side="right" transform="translate({full_width - shore_width} {0})">'
	yield f'<image height="{shore_height}" width="{shore_width}" href="/static/problem_assets/right_shore.svg" />'
	yield f'<g class="obj" side="right" transform="translate({shore_pad["left"] + add} {shore_pad["top"]})">'
	pos, cur_height = (0, 0)
	for rect in range(obj_amount):
		yield f"""<rect class="grid" width="{dwarf_width}" height="{dwarf_height}"
					pos="{pos}" side="right"
					x="{(pos % 2 == 1) * dwarf_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}"/>"""
		pos += 1
		cur_height += dwarf_height

	pos, cur_height = (0, 0)
	for dwarf in range(data['conf']['right']['dwarf']):
		yield f"""<image class="active dwarf" width="{dwarf_width}" height="{dwarf_height}" 
					pos="{pos}" side="right"
					href="/static/problem_assets/dwarf.png"
					x="{(pos % 2 == 1) * dwarf_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}" />"""
		pos += 1
		cur_height += dwarf_height
	for bag in range(data['conf']['right']['bag']):
		yield f"""<image class="active bag" width="{bag_width}" height="{bag_height}"
					pos="{pos}" side="right"
					href="/static/problem_assets/money_bag.png"
					x="{(pos % 2 == 1) * dwarf_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}" />"""
		pos += 1
		cur_height += bag_height
	yield '</g>'
	yield '</g>'

	yield f"""<image class="reload" href="/static/problem_assets/reload.png" 
					width="{rel_width}" height="{rel_height}" 
					x="{full_width}" y="{full_height - rel_height}" />"""
	yield '</svg>'
	yield '<div class="UI for_dwarfs">'
	yield '<div id="go" class="active"> Отправить лодку </div>'
	yield f'<div id="time" class="passive"> Осталось времени: {data["remain_time"]}:00 </div>'
	yield '<div id="clear" class="active"> Очистить лодку </div>'
	yield '</div>'
	yield '</div>'

def steps(step_num, params, data):
	if 'type' in params.keys():
		if params['type'] == 'go':
			print('here1', file=sys.stderr)
			if params['side'] == 'left':
				side_from, side_to = ('right', 'left')
			else:
				side_from, side_to = ('left', 'right')

			if data['remain_time'] <= 0:
				return {'answer': 'no_time'}
			elif data['dwarf_weight'] * params['dwarf'] + data['bag_weight'] * params['bag'] > data['remain_weight']:
				return {'answer': 'too_heavy'}
			elif params['dwarf'] == 0:
				return {'answer': 'no_dwarf'}
			elif data['conf'][side_from]['dwarf'] < params['dwarf'] or data['conf'][side_from]['bag'] < params['bag']:
				return {'answer': 'cheating'}
			elif data['conf'][side_from]['dwarf'] == params['dwarf'] and data['conf'][side_from]['bag']:
				return {'answer': 'bag_without_dwarfs'}
			else:
				resp = {}
				data['conf'][side_from]['dwarf'] -= params['dwarf']
				data['conf'][side_from]['bag'] -= params['bag']
				data['conf'][side_to]['dwarf'] += params['dwarf']
				data['conf'][side_to]['bag'] += params['bag']
				data['remain_time'] -= data['trip_time']
				data['side'] = side_to
				return {'answer': 'accept', 'data_update': data}
		elif params['type'] == 'reload':
			data['remain_time'] = data['start_time']
			data['conf'] = data['start_conf']
			data['side'] = data['start_side']
			data['remain_weight'] = data['start_weight']
			return {'answer': '', 'type': 'reload', 'data_update': data}
	else:
		return {'answer': ''}


def validate(data, answer):
	return data['conf']['right']['dwarf'] == 0 and data['conf']['right']['bag'] == 0 
