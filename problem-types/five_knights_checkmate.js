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

function occupied(ind, only_horse = false) {
	let [x, y] = [$(`rect:eq(${ind})`).attr('x'), $(`rect:eq(${ind})`).attr('y')]
	let tmp = 0
	if (only_horse)
		$('image.horse.active').each(function(index){if ($(this).attr('x') == x && $(this).attr('y') == y) tmp = 1})
	else
		$('image').each(function(index){if ($(this).attr('x') == x && $(this).attr('y') == y) tmp = 1})
	return tmp == 1
}
function move(e) {
	let obj = $('.targeted')
	let svg = $('svg')[0].getBoundingClientRect()
	if (!in_access_zone(obj)) {
		end_move(in_access=false)
	}
	else {
		autoscroll(e.clientX, e.clientY)
		$(obj).attr({'x': getSVGCoordinates(e).x - side / 2,
					'y': getSVGCoordinates(e).y - side / 2})
	}
}

function create_new_horse() {
	let obj = $('.horse')
	let new_horse = $(document.createElementNS("http://www.w3.org/2000/svg", 'image'))
	    .addClass('horse active')
	    .attr({
	        x: def_x,
	        y: def_y,
	        width: $(obj).attr('width'),
	        height: $(obj).attr('height'),
	        href: $(obj).attr('href')
	    });
	    $('svg').append(new_horse)
}

function back_to_drag() {
	$(document).off('mousemove touchmove')
	$('.targeted').remove()
	remain += 1
}

function start_move(e) {
	let obj = $(e.currentTarget) 
	if (!$(obj).hasClass('choiced')) {
		remain -= 1
	}
	$('svg').append(obj)
	let svg = $('svg')[0].getBoundingClientRect()
	$(obj).attr({'x': getSVGCoordinates(e).x - side / 2,
				'y': getSVGCoordinates(e).y - side / 2})
	$(obj).addClass('targeted')
	$(document).on('mousemove touchmove', move)
	update_status()
}

function end_move(in_access=true) {
	let obj = $('.targeted')
	let [best_ind, min_dist] = [0, Math.sqrt(2) * side]
	$('rect').each(function(index){
		let dist = Math.hypot(($(obj).attr('x') - $(this).attr('x')), ($(obj).attr('y') - $(this).attr('y')))
		if (min_dist >= dist)
			[best_ind, min_dist] = [index, dist]
	})
	if (best_ind == '' || occupied(best_ind) || !in_access) {
		back_to_drag()
	}
	else {
		$(document).off('mousemove touchmove')
		$(obj).attr('x', $(`rect:eq(${best_ind})`).attr('x')).attr('y', $(`rect:eq(${best_ind})`).attr('y'))
		$(obj).addClass('choiced')
		$(obj).removeClass('targeted')
	}
	if (remain > 0 && $('.active').not('.choiced').length == 0) create_new_horse()
	update_status()
}

function update_status() {
	$('.horse.active').off('mousedown touchstart')
	$('.horse.active').off('mouseup touchend')
	$('.horse.active').on('mousedown touchstart', start_move)
	$('.horse.active').on('mouseup touchend', end_move)
	$('text.amount')[0].innerHTML = remain
}

var side = $('.horse.active').attr('width')
var [def_x, def_y] = [$('.horse.passive.drag').attr('x'), $('.horse.passive.drag').attr('y')]
var remain = $('text.amount').html()

$('.horse.active').on('mousedown touchstart', start_move)
$('.horse.active').on('mouseup touchend', end_move)
$('.reload').on('click touchstart', function(){
	$('.horse.active').remove()
	create_new_horse()
	remain = 4
	update_status()
})
$('.submit_button').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	let ans = ''
	$('rect').each(function(index){
		if (occupied(index, only_horse=true)) ans += "1,"
		else ans += "'',"
	})
	$('input[name="answer"]').val(ans)
})

var scroll_p = $(document.createElement('div')).addClass('scroll_div')
$('body').append(scroll_p)
