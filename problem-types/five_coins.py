def entry_form(data, kwargs):
	scale_1 = 0.7
	ellipse_a = 0.45
	cup_xr = 300 * 0.4
	cup_yr = cup_xr * ellipse_a
	cup_under_xr = cup_xr
	cup_under_yr = cup_yr * 1.5
	rope_length = 400 * 0.4
	plank_width = 10
	plank_length = 500
	hinge_r = 20 * 0.4
	base_plank_width = 15
	base_plank_height = 400
	base_plank_up = 30
	basement_width = 250
	basement_hight = 80
	base_inside_yr = cup_yr * 0.7
	base_inside_xr = cup_xr * 0.7
	coin_size = 70
	drag_pad = 30
	weight = [10, 20, 20, 30, 60]
	answer_zone_height = 120
	container_height = answer_zone_height
	container_width = 100
	container_pad = 20
	coin_pad = container_width - coin_size + container_pad
	cont_a = 0.25
	answer_zone_pad = 20
	svg_width = (plank_length + cup_xr * 2) * scale_1
	svg_height = (base_plank_width / 2 * ellipse_a + base_plank_height + basement_hight + basement_width / 2 * ellipse_a) * scale_1 + drag_pad + coin_size + answer_zone_height + answer_zone_pad
	yield '<input name="answer" type="hidden" />'
	yield '<div class="plot_area">'
	yield f'<svg version="1.1" width="{svg_width}" height="{svg_height}" overflow="visible" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield '<defs>'

	yield '<linearGradient id="cupShadowInside">'
	yield '<stop offset="0%" stop-color="#373200" />'
	yield '<stop offset="100%" stop-color="#7B6F01" />'
	yield '</linearGradient>'

	yield '<linearGradient id="cupShadowOutside">'
	yield '<stop offset="0%" stop-color="#B0A000" />'
	yield '<stop offset="36%" stop-color="#EDE8B4" />'
	yield '<stop offset="100%" stop-color="#B0A000" />'
	yield '</linearGradient>'

	yield '<linearGradient id="baseBlankShadow">'
	yield '<stop offset="0%" stop-color="#C9B700" />'
	yield '<stop offset="38%" stop-color="#EDE8B4" />'
	yield '<stop offset="100%" stop-color="#C9B700" />'
	yield '</linearGradient>'

	yield '<linearGradient id="blankShadow" x1="0" x2="0" y1="0" y2="1">'
	yield '<stop offset="0%" stop-color="#C9B700" />'
	yield '<stop offset="62%" stop-color="#EDE8B4" />'
	yield '<stop offset="100%" stop-color="#C9B700" />'
	yield '</linearGradient>'

	yield '<linearGradient id="coinShadow" x1="0" x2="1" y1="0" y2="1">'
	yield '<stop offset="0%" stop-color="gold" />'
	yield '<stop offset="50%" stop-color="#fff2af" />'
	yield '<stop offset="100%" stop-color="gold" />'
	yield '</linearGradient>'

	yield '</defs>'
	yield f'<g class="scales" transform="scale({scale_1}) translate({cup_xr} {base_plank_up + base_plank_width / 4})">'
	yield f"""<rect class="plank" 
				x="0"
				y="0"
				width="{plank_length}"
				height="{plank_width}" />"""
	yield f'<g class="base" transform="translate({plank_length / 2} 0)">'
	yield f"""<path class="base_outside" transform="translate({-basement_width / 2} {base_plank_height - base_plank_up})"
				d="M 0 0 
				V {basement_hight}
				A {basement_width / 2} {basement_width / 2 * ellipse_a} 0 0 0 {basement_width} {basement_hight}
				V 0
				H 0
				Z" />"""
	yield f"""<ellipse class="base_outside"
	 			cx="0"
	 			cy="{base_plank_height - base_plank_up}"
	 			rx="{basement_width / 2}"
	 			ry="{basement_width / 2 * ellipse_a}" />"""
	yield f"""<ellipse class="base_inside"
				cx="0"
				cy="{base_plank_height - base_plank_up}"
				rx="{base_inside_xr}"
				ry="{base_inside_yr}"" />"""
	yield f"""<path class="base_plank"
				transform="translate({-base_plank_width / 2} {-base_plank_up})"
				d="M 0 0
	 			V {base_plank_height}
	 			A {base_plank_width / 2} {base_plank_width / 2 * ellipse_a} 0 0 0 {base_plank_width} {base_plank_height}
	 			V 0
	 			A {base_plank_width / 2} {base_plank_width / 2 * ellipse_a} 0 0 0 0 0"
	 			/>"""
	yield f"""<circle class="hinge center" transform="translate(0 {plank_width / 2})"
			cx="0"
			cy="0"
			r="{hinge_r * 2}" />"""
	yield '</g>'
	yield f'<g class="cup_with_rope left" transform="translate({-cup_xr} {plank_width / 2})">'
	yield f'<g class="cup left" transform="translate(0 {rope_length})">'
	yield f'<path transform="translate(0 {cup_yr})" class="outside" d="M  0 0 A {cup_under_xr} {cup_under_yr} 0 0 0 {cup_under_xr * 2} 0 Z" />'
	yield f"""<ellipse class="inside left" 
				cx="{cup_xr}"
				cy="{cup_yr}"
				rx="{cup_xr}"
				ry="{cup_yr}" />"""
	yield '</g>'
	yield f"""<line 
				x1="{cup_xr}"
				y1="0"
				x2="{cup_xr}"
				y2="{rope_length}" />"""
	yield f"""<line 
				x1="{cup_xr}"
				y1="0"
				x2="{cup_xr - 1.5 * cup_xr / (3 ** 0.5)}"
				y2="{rope_length + cup_yr * 1.5}" />"""
	yield f"""<line 
				x1="{cup_xr}"
				y1="0"
				x2="{cup_xr + 1.5 * cup_xr / (3 ** 0.5)}"
				y2="{rope_length + cup_yr * 1.5}" />"""
	yield f"""<circle class="hinge left"
				cx="{cup_xr}"
				cy="0"
				r="{hinge_r}"/>"""
	yield '</g>'
	yield f'<g class="cup_with_rope right" transform="translate({plank_length - cup_xr} {plank_width / 2})">'
	yield f'<g class="cup right" transform="translate(0 {rope_length})">'
	yield f'<path transform="translate(0 {cup_yr})" class="outside" d="M  0 0 A {cup_under_xr} {cup_under_yr} 0 0 0 {cup_under_xr * 2} 0" />'
	yield f"""<ellipse class="inside right" 
				cx="{cup_xr}"
				cy="{cup_yr}"
				rx="{cup_xr}"
				ry="{cup_yr}" />"""
	yield '</g>'
	yield f"""<line 
				x1="{cup_xr}"
				y1="0"
				x2="{cup_xr}"
				y2="{rope_length}" />"""
	yield f"""<line 
				x1="{cup_xr}"
				y1="0"
				x2="{cup_xr - 1.5 * cup_xr / (3 ** 0.5)}"
				y2="{rope_length + cup_yr * 1.5}" />"""
	yield f"""<line 
				x1="{cup_xr}"
				y1="0"
				x2="{cup_xr + 1.5 * cup_xr / (3 ** 0.5)}"
				y2="{rope_length + cup_yr * 1.5}" />"""
	yield f"""<circle class="hinge right"
				cx="{cup_xr}"
				cy="0"
				r="{hinge_r}"/>"""
	yield '</g>'
	yield '</g>'
	yield f'<g class="drag_zone" transform="translate({(container_width - coin_size) / 2} {svg_height - coin_size - answer_zone_height - answer_zone_pad})">'
	for i in range(1, 6):
		yield f'<g class="coin num_{i}" transform="translate({(coin_size + coin_pad) * (i - 1) + coin_size / 2} {coin_size / 2})">'
		yield f'<title> {i} </title>'
		yield f'<circle cx="0" cy="0" r="{coin_size / 2}" />'
		yield f'<text class="coin_text" x="0" y="0"> {i} </text>'
		yield '</g>'
	yield '</g>'
	yield f'<g class="answer_zone" transform="translate(0 {svg_height - answer_zone_height})">'
	yield f'<rect class="answer_zone" x="0" y="0" width="{(container_width + container_pad) * 5 - container_pad}" height="{container_height}" />'
	for i in range(1, 6):
		yield f'<g class="coin_container" transform="translate({(container_width + container_pad) * (i - 1)} 0)">'
		yield f'<rect class="coin_container_name" x="0" y="0" width="{container_width}" height="{container_height * cont_a}"/>'
		yield f'<text class="coin_container_name" x="{container_width / 2}" y="{container_height * cont_a / 2}"> {weight[i - 1]} граммов </text>'
		yield f'<rect class="coin_container_drag num_{i}" x=0 y="{container_height * cont_a}" width="{container_width}" height="{container_height * (1 - cont_a)}">'
		yield '</g>'
	yield '</g>'
	yield '</svg>'
	yield '<div class="interface_zone">'
	yield '<button type="submit"> Взвесить! </button>'
	yield '<button> Очистить весы </button>'
	yield '<div class="remaining_weightings">'
	yield '<p> Осталось </br> взвешиваний: 2<p>'
	yield '</div>'
	yield '</div>'
	yield '</div>'

def validate(data, answer):
	return True