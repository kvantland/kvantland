function dist(obj1, obj2) {
	let rect1 = obj1.getBoundingClientRect()
	let rect2 = obj2.getBoundingClientRect()
	let [x1, y1] = [(rect1.right + rect1.left) / 2, (rect1.bottom + rect1.top) / 2]
	let [x2, y2] = [(rect2.right + rect2.left) / 2, (rect2.bottom + rect2.top) / 2]
	return (x2 - x1) ** 2 + (y1 - y2) ** 2
}

function change_obj(obj1, obj2) {
	let [pos1, pos2] = [$(obj2).attr('pos'), $(obj1).attr('pos')]
	let [side1, side2] = [$(obj2).attr('side'), $(obj1).attr('side')]
	let rect1 = $(`rect[pos=${$(obj1).attr('pos')}][side=${$(obj1).attr('side')}]`)
	let rect2 = $(`rect[pos=${$(obj2).attr('pos')}][side=${$(obj2).attr('side')}]`)
	$(obj1).attr({'pos': pos1, 'side': side1, 'x': $(rect2).attr('x'), 'y': $(rect2).attr('y')})
	$(obj2).attr({'pos': pos2, 'side': side2, 'x': $(rect1).attr('x'), 'y': $(rect1).attr('y')})
	$(obj1).appendTo(`g.obj[side=${$(obj1).attr('side')}]`)
	$(obj2).appendTo(`g.obj[side=${$(obj2).attr('side')}]`)
}

function autoscroll(x, y) {
	block_nav()
	let [x_add, y_add] = [100, 100]
	let [y_tmp, x_tmp] = ['no', 'no']
	let dur = {'left': -1, 'right': 1, 'up': -1, 'down': 1, 'no': 0}
	$(scroll_p).css({'left': x, 'top': y - -y_add})
	if (!in_access_zone(scroll_p))
		y_tmp = 'down'

	$(scroll_p).css({'left': x, 'top': y - y_add})
	if (!in_access_zone(scroll_p))
		y_tmp = 'up'

	$(scroll_p).css({'top': y, 'left': x - -x_add})
	if (!in_access_zone(scroll_p))
		x_tmp = 'right'

	$(scroll_p).css({'top': y, 'left': x - x_add})
	if (!in_access_zone(scroll_p))
		x_tmp = 'left'

	scrollBy(dur[x_tmp] * x_add / 2, dur[y_tmp] * y_add / 2)
}

function in_window(obj) {
	let rect = $(obj)[0].getBoundingClientRect()
	let [hor_add, vert_add] = [rect.width / 2, rect.height / 2]
	if (rect.left + hor_add < 0 || rect.right - hor_add > $(window).width())
		return false
	if (rect.top + vert_add < 0 || rect.bottom - vert_add > $(window).height())
		return false
	return true
}

function is_intersect(obj1, obj2) {
	let [rect1, rect2] = [$(obj1)[0].getBoundingClientRect(), $(obj2)[0].getBoundingClientRect()]
	if (rect1.left > rect2.right || rect2.left > rect1.right) 
		return false
	if (rect1.bottom < rect2.top || rect2.bottom < rect1.top)
		return false
	return true
}

function in_access_zone(obj) {
	let nav = $('nav.user_nav')
	if (is_intersect(obj, nav))
		return false
	if (!in_window(obj))
		return false
	return true
}

function getSVGCoordinates(event) {
	if (event.touches) {
		let coordinatePoint = new DOMPoint(event.touches[0].clientX, event.touches[0].clientY)
		let svg = document.querySelector('svg')
		return coordinatePoint.matrixTransform(svg.getScreenCTM().inverse())
	}
	else {
		let coordinatePoint = new DOMPoint(event.clientX, event.clientY)
		let svg = document.querySelector('svg')
		return coordinatePoint.matrixTransform(svg.getScreenCTM().inverse())
	}
}

function update_best() {
	$('rect').removeClass('best')
	let obj = $('.targeted')[0]
	let [best_ind, min_dist] = [0, 10 ** 18]
	$('rect').each(function(ind){
		let new_dist = dist(this, obj)
		if (new_dist < min_dist) {
			[best_ind, min_dist] = [ind, new_dist]
		}
	})
	if (min_dist <= min_dist_) {
		$(`rect:eq(${best_ind})`).addClass('best')
	}
}

function start_move(e) {
	let obj = $(e.currentTarget)
	$('svg:eq(0)').append(obj)
	let svg = $('svg')[0].getBoundingClientRect()
	$(obj).attr({
			'x': getSVGCoordinates(e).x - $(obj).attr('width') / 2, 
			'y': getSVGCoordinates(e).y - $(obj).attr('height') / 2,
			})
	$(obj).addClass('targeted')
	update_best()
	$(document).on('mousemove touchmove', move)
}

function move(e) {
	let obj = $('.targeted')
	let svg = $('svg')[0].getBoundingClientRect()
	$(obj).attr({
			'x': getSVGCoordinates(e).x - $(obj).attr('width') / 2,
			'y': getSVGCoordinates(e).y - $(obj).attr('height') / 2})
	if (!in_access_zone(obj)) 
		drop()
	else 
		update_best()
	autoscroll(e.clientX, e.clientY)
}

function drop() {
	let obj = $('.targeted')
	if ($('.best').length) {
		if ($('.best').hasClass('boat') && $('.best').attr('side') == $(obj).attr('side')) {
			let pref_className = $('.best').attr('dwarf') + '_' + $('.best').attr('bag')
			if ($(obj).hasClass('dwarf') && remain_weight >= 20) {
				$('.best').attr('dwarf', $('.best').attr('dwarf') - -1)
				remain_weight -= 20
				$(obj).addClass('in_boat')
			}
			else if (remain_weight >= 50) {
				$('.best').attr('bag', $('.best').attr('bag') - -1)
				remain_weight -= 50
				$(obj).addClass('in_boat')
			}
			else 
				show_xhr('Слишком большая масса лодки!')
			let className = $('.best').attr('dwarf') + '_' + $('.best').attr('bag')
			if (pref_className != className) {
				$(`image.boat.${className}`).addClass('cur')
			}
			back_to_drag()
		}
		else if ($('.best').attr('side') == $(obj).attr('side')) {
			let obj2 = $(`image.active[pos=${$('.best').attr('pos')}][side=${$('.best').attr('side')}]`)
			if (obj2.length)
				change_obj(obj, obj2)
			else {
				$(obj).attr({'pos': $('.best').attr('pos'),
							'side': $('.best').attr('side'),
							'x': $('.best').attr('x'), 
							'y': $('.best').attr('y')})
				$(obj).appendTo(`g.obj[side=${$(obj).attr('side')}]`)
			}
		}
		else
			back_to_drag()
	}
	else
		back_to_drag()
	if ($(obj))
		$(obj).removeClass('targeted')
	$(document).off('mousemove touchmove')
}

function back_to_drag() {
	let obj = $('.targeted')
	let [pos, side] = [$(obj).attr('pos'), $(obj).attr('side')]
	let rect = $(`rect[pos=${pos}][side=${side}]`)
	$(obj).attr('x', $(rect).attr('x'))
	$(obj).attr('y', $(rect).attr('y'))
	$(obj).appendTo(`g.obj[side=${side}]`)
}

function move_boat(e) {
	if (boat_move_tmp)
		return;
	else {
		let url = new URL(window.location.href + 'xhr')
		$.post(url, JSON.stringify({
			'side': side, 
			'dwarf': $('.dwarf.in_boat').length, 
			'bag': $('.bag.in_boat').length, 
			'type': 'go'
			}), function(data){
			
			if (data == 'accept') {
				remain_time -= 6
				$('#time')[0].innerHTML = $('#time')[0].innerHTML.split(': ')[0] + ': ' + remain_time + ':00'
				boat_move_tmp = 1
				$('g.boat rect').attr('side', side)

				boat_move = setInterval(function(){
					let [dx, dy] =  [$('g.boat').attr('dx'), $('g.boat').attr('dy')] 
					if (stop_pos['left'] > dx - add || stop_pos['right'] < dx - add) {
						go_out()
						boat_move_tmp = 0
						clearInterval(boat_move)
					}
					else {
						$('g.boat').attr({
							'side': side,
							'dx': dx - add, 
							'dy': dy, 
							'transform': `translate(${dx - add} 0)`})
						let sea_dx = $('.sea').attr('dx')
						$('.sea').attr({
							'dx': sea_dx - -add,
							'transform':  `translate(${sea_dx - -add} 0)`})
					}
				}, 10)
			}
			else if (data == 'no_time')
				show_xhr('Время вышло!')
			else if (data == 'too_heavy') {
				show_xhr('Слишком большая масса лодки!')
				go_out('here')
			}
			else if (data == 'no_dwarf')
				show_xhr('Лодкой некому управлять!')
			else if (data == 'cheating')
				show_xhr('Решайте задачу честно!')
			else if (data == 'bag_without_dwarfs') {
				show_xhr('Мешок не может остаться без присмотра!')
				go_out(here=true)
			}
			else {
				show_xhr('Невозможно совершить перевозку!')
				go_out(here=true)
			}
		})
	}
}

function go_out(here=false) {
	if (here) {
		if (side == 'left')
			[side, add] = ['right', -2]
		else
			[side, add] = ['left', 2]
	}
	$('.in_boat').each(function(index){
		let free_ind
		$(`g.obj[side=${side}] rect`).each(function(index){
			if (!$(`image.active[side=${$(this).attr('side')}][pos=${$(this).attr('pos')}]`).length) {
				free_ind = index
				return false;
			}
		})
		let free_space = $(`g.obj[side=${side}] rect:eq(${free_ind})`)
		$(this).attr({
			'side': free_space.attr('side'),
			'pos': free_space.attr('pos'),
			'x': free_space.attr('x'),
			'y': free_space.attr('y')
		})
		$(this).removeClass('in_boat')
		$(this).appendTo(`g.obj[side=${side}]`)
	})
	$('image.boat:not(.0_0)').removeClass('cur')
	$('g.boat rect').attr({'dwarf': 0, 'bag': 0})
	remain_weight = 70
	if (side == 'left')
		[side, add] = ['right', -2]
	else
		[side, add] = ['left', 2]
}

const min_dist_ = 9000 //квадрат расстояния между центрами для перемещения объекта
var remain_time = $('#time')[0].innerHTML.split(': ')[1].split(':')[0]
var remain_weight = 70
var [boat_move, boat_move_tmp] = [0, 0]
var [side_from, add] = [$('g.boat').attr('side'), 0] //откуда и как быстро плывет лодка
var side // куда плывет лодка
if (side_from == 'left')
	[side, add] = ['right', -2]
else
	[side, add] = ['left', 2]
const stop_pos = {'left': $('g.shore[side="left"] image').attr('width') - $('rect.boat').attr('x'), 'right': 0}

var scroll_p = $(document.createElement('div')).addClass('scroll_div')
$('body').append(scroll_p)

$('image.boat').not('.0_0').each(function(ind){
	if (!$(this).hasClass('cur')) {
	$(this).addClass('cur');
	setTimeout(() => $(this).removeClass('cur'));
	}
})

$('image.active').on('mousedown touchstart', start_move)
$('image.active').on('mouseup touchend', drop)

$('#go').on('click touchstart', move_boat)
$('#clear').on('click touchstart', (e) => go_out(here=true))

let url = new URL(window.location.href + 'xhr')
$('.reload').on('click touchstart', function(){
	$.post(url, JSON.stringify({'type': 'reload'}), 
		function(data){window.location.reload('true')} )})
