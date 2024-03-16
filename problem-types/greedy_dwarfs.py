def entry_form(data, kwargs):
	full_width, full_height = (1000, 600)
	shore_width, shore_height = (200, 600)
	sea_width, sea_height = (1000, 600)
	dwarf_width, dwarf_height = (80, 95)
	bag_width, bag_height = (80, 95)
	shore_pad = {'left':(shore_width - dwarf_width * 2) // 4, 'top': 5}
	add = 10 # прибавка к left_pad
	boat_width, boat_height = (200, 200)

	yield '<div class="full_problem">'
	yield '<input type="hidden" name="answer" />'
	yield f"""<svg 
				version="1.1" 
				width="{full_width}" 
				height="{full_height}" 
				overflow="visible" 
				xmlns="http://www.w3.org/2000/svg" 
				xmlns:xlink="http://www.w3.org/1999/xlink">"""

	yield f'<svg width="{sea_width}" height="{sea_height}" >'
	yield f'<image class="sea" width={sea_width} height="{sea_height}" href="/static/problem_assets/sea.svg" />'
	yield '</svg>'
	yield '<g class="boat">'
	yield f"""<rect class="boat grid" width={boat_width} height="{boat_height}"
				x="{full_width - shore_width - boat_width}"
				y="{(full_height - boat_height) / 2}" />"""
	yield f"""<image class="boat" width={boat_width} height="{boat_height}"
				dwarf="0" bag="0"
				x="{full_width - shore_width - boat_width}"
				y="{(full_height - boat_height) / 2}"
				href="/static/problem_assets/boat_0_0.png" />"""
	yield '</g>'
	yield '<g class="shore" side="left">'
	yield f'<image height="{shore_height}" width="{shore_width}" href="/static/problem_assets/left_shore.svg" />'
	yield f'<g class="obj" side="left" transform="translate({shore_pad["left"] - add} {shore_pad["top"]})">'
	pos, cur_height = (0, 0)
	for dwarf in range(data['conf']['left']['dwarf']):
		yield f"""<rect class="grid" width="{dwarf_width}" height="{dwarf_height}"
					pos="{pos}" side="left"
					x="{(pos % 2 == 1) * dwarf_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}"/>"""
		yield f"""<image class="active dwarf" width="{dwarf_width}" height="{dwarf_height}"
					pos="{pos}" side="right" 
					href="/static/problem_assets/dwarf.png"
					x="{(pos % 2 == 1) * dwarf_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}"" />"""
		pos += 1
		cur_height += dwarf_height
	for bag in range(data['conf']['left']['bag']):
		yield f"""<rect class="grid" width="{bag_width}" height="{bag_height}"
					pos="{pos}" side="left"
					x="{(pos % 2 == 1) * bag_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}"/>"""
		yield f"""<image class="active bag" width="{bag_width}" height="{bag_height}" 
					pos="{pos}" side="right" 
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
	for dwarf in range(data['conf']['right']['dwarf']):
		yield f"""<rect class="grid" width="{dwarf_width}" height="{dwarf_height}"
					pos="{pos}" side="right"
					x="{(pos % 2 == 1) * dwarf_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}"/>"""
		yield f"""<image class="active dwarf" width="{dwarf_width}" height="{dwarf_height}" 
					pos="{pos}" side="right"
					href="/static/problem_assets/dwarf.png"
					x="{(pos % 2 == 1) * dwarf_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}" />"""
		pos += 1
		cur_height += dwarf_height
	for bag in range(data['conf']['right']['bag']):
		yield f"""<rect class="grid" width="{bag_width}" height="{bag_height}"
					pos="{pos}" side="right"
					x="{(pos % 2 == 1) * bag_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}"/>"""
		yield f"""<image class="active bag" width="{bag_width}" height="{bag_height}"
					pos="{pos}" side="right"
					href="/static/problem_assets/money_bag.png"
					x="{(pos % 2 == 1) * dwarf_width + shore_pad['left']}"
					y="{cur_height + shore_pad['top']}" />"""
		pos += 1
		cur_height += bag_height
	yield '</g>'
	yield '</g>'
	yield '</svg>'
	yield '<div class="UI for_dwarfs">'
	yield '<div id="go" class="active"> Отправить лодку </div>'
	yield f'<div id="time" class="passive"> Осталось времени: {data["remain_time"]}:00 </div>'
	yield '<div id="restart" class="active"> Рестарт </div>'
	yield '</div>'
	yield '</div>'

def validate(data, answer):
	return True

WITHOUT_BUTTONS = True