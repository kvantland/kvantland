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
	if (e.touches)
		e.preventDefault()
	let obj = $('.targeted')
	let svg = $('svg')[0].getBoundingClientRect()
	$(obj).attr('x', e.clientX - svg.left - side / 2).attr('y', e.clientY - svg.top - side / 2)
	let [x, y] = [e.clientX, e.clientY]
	if (x <= 0 || y <= 0 || y >= $(window).height() || x >= $(window).width()) {
		back_to_drag()
	}
	autoscroll(e.clientX, e.clientY)
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
	if (remain == 0) create_new_horse()
	remain += 1
}

function start_move(e) {
	if (e.touches)
		e.preventDefault()
	let obj = $(e.currentTarget) 
	if (!$(obj).hasClass('choiced')) {
		remain -= 1
		if (remain > 0)
			create_new_horse()
	}
	$('svg').append(obj)
	let svg = $('svg')[0].getBoundingClientRect()
	$(obj).attr('x', e.clientX - svg.left - side / 2).attr('y', e.clientY - svg.top - side / 2)
	$(obj).addClass('targeted')
	$(document).on('mousemove touchmove', move)
	update_status()
}

function end_move() {
	let obj = $('.targeted')
	let [best_ind, min_dist] = [0, Math.sqrt(2) * side]
	$('rect').each(function(index){
		let dist = Math.hypot(($(obj).attr('x') - $(this).attr('x')), ($(obj).attr('y') - $(this).attr('y')))
		if (min_dist >= dist)
			[best_ind, min_dist] = [index, dist]
	})
	if (best_ind == '' || occupied(best_ind)) {
		back_to_drag()
	}
	else {
		$(document).off('mousemove touchmove')
		$(obj).attr('x', $(`rect:eq(${best_ind})`).attr('x')).attr('y', $(`rect:eq(${best_ind})`).attr('y'))
		$(obj).addClass('choiced')
		$(obj).removeClass('targeted')
	}
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