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
	let add = 40
	let [x_diff, y_diff] = [0, 0]
	let [bott, right] = [window.innerHeight, window.innerWidth]
	if (x < add)
		x_diff = x - add
	if (y < add)
		y_diff = y - add
	if (y > bott - add)
		y_diff = y - bott + add
	if (x > right - add)
		x_diff = x - right + add
	scrollBy(x_diff, y_diff)
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
	console.log('here')
	if (e.touches)
		e.preventDefault();
	let obj = $(e.currentTarget)
	$('svg:eq(0)').append(obj)
	let svg = $('svg')[0].getBoundingClientRect()
	$(obj).attr({
			'x': e.clientX - svg.left - $(obj).attr('width') / 2, 
			'y': e.clientY - svg.top - $(obj).attr('height') / 2,
			})
	$(obj).addClass('targeted')
	update_best()
	$(document).on('mousemove touchmove', move)
}

function move(e) {
	if (e.touches)
		e.preventDefault();
	let obj = $('.targeted')
	let svg = $('svg')[0].getBoundingClientRect()
	$(obj).attr({
			'x': e.clientX - svg.left - $(obj).attr('width') / 2,
			'y': e.clientY - svg.top - $(obj).attr('height') / 2})
	let [x, y] = [e.clientX, e.clientY]
	if (x <= 0 || y <= 0 || y >= $(window).height() || x >= $(window).width()) {
		drop()
	}
	else 
		update_best()
	autoscroll(e.clientX, e.clientY)
}

function drop() {
	let obj = $('.targeted')
	if ($('.best').length) {
		if ($('.best').hasClass('boat')) {
			if ($(obj).hasClass('dwarf'))
				$('image.boat').attr('dwarf', $('image.boat').attr('dwarf') - -1)
			else
				$('image.boat').attr('bag', $('image.boat').attr('bag') - -1)
			$('image.boat').attr('href', `/static/problem_assets/boat_${$('image.boat').attr('dwarf')}_${$('image.boat').attr('boat')}`)
			$(obj).remove()
		}
		else if ($('.best').attr('side') == $(obj).attr('side')) {
			let obj2 = $(`image.active[pos=${$('.best').attr('pos')}][side=${$('.best').attr('side')}]`)
			change_obj(obj, obj2)
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
	$(obj).appendTo(`g.obj[side=${$(obj).attr('side')}]`)
}

var min_dist_ = 9000 //квадрат расстояния между центрами для перемещения объекта

$('image.active').on('mousedown touchstart', start_move)
$('image.active').on('mouseup touchend', drop)

