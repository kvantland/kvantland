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

function occupied(rect) {
	let [pos, num] = [$(rect).attr('pos'), $(rect).attr('num')]
	let match = $(`.match.active[pos=${pos}][num=${num}]`)
	return (match.length > 0 && !match.hasClass('targeted'))
}

function dist(obj1, obj2) {
	let rect1 = obj1.getBoundingClientRect()
	let rect2 = obj2.getBoundingClientRect()
	let [x1, y1] = [(rect1.right + rect1.left) / 2, (rect1.bottom + rect1.top) / 2]
	let [x2, y2] = [(rect2.right + rect2.left) / 2, (rect2.bottom + rect2.top) / 2]
	console.log(x1, x2, y1, y2)
	return (x2 - x1) ** 2 + (y1 - y2) ** 2
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
	if (min_dist <= min_dist_ && !occupied($(`rect:eq(${best_ind})`))) {
		$(`rect:eq(${best_ind})`).addClass('best')
	}
}

function start_move(e) {
	if (e.touches)
		e.preventDefault();
	let obj = $(e.currentTarget)
	$('svg').append(obj)
	let svg = $('svg')[0].getBoundingClientRect()
	$(obj).attr({
			'x': e.clientX - svg.left - match_width / 2, 
			'y': e.clientY - svg.top - match_length / 2,
			'transform': 'rotate(0)'})
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
			'x': e.clientX - svg.left - match_width / 2,
			'y': e.clientY - svg.top - match_length / 2})
	let [x, y] = [e.clientX, e.clientY]
	if (x <= 0 || y <= 0 || y >= $(window).height() || x >= $(window).width()) {
		drop()
	}
	else 
		update_best()
	console.log($(obj).attr('pos'), $(obj).attr('num'))
	autoscroll(e.clientX, e.clientY)
}

function back_to_drag() {
	let obj = $('.match.targeted:eq(0)')
	let [pos, num] = [$(obj).attr('pos'), $(obj).attr('num')]
	console.log(pos, num, $(obj).attr('x'), $(obj).attr('y'))
	let rect = $(`rect[pos=${pos}][num=${num}]`)
	$(obj).attr('x', $(rect).attr('x') - pad_)
	$(obj).attr('y', $(rect).attr('y'))
	if ($(rect).attr('direction') === 'hor') {
		$(obj).attr('y', $(obj).attr('y') - -rect_width)
	}
	$(obj).appendTo(`g.num[num=${num}]`)
}

function drop() {
	let obj = $('.targeted')
	if ($('.best').length) {
		let rect = $('.best')
		let num = $(rect).attr('num')
		$(obj).attr({
			'x': $(rect).attr('x') - pad_,
			'y': $(rect).attr('y') - -rect_width * ($(rect).attr('direction') === 'hor'),
			'pos': $(rect).attr('pos'),
			'num': $(rect).attr('num'),
		})
		if ($(rect).attr('direction') === 'hor')
			$(obj).attr('transform', `rotate(-90 ${$(rect).attr('x')} ${$(obj).attr('y')})`)
		rect.removeClass('best')
		$(obj).appendTo(`g.num[num=${num}]`)
	}
	else {
		back_to_drag()
	}
	$(obj).removeClass('targeted')
	$(document).off('mousemove touchmove')
}

const match_width = Math.min($('.match').attr('width'), $('.match').attr('height'))
const match_length = Math.max($('.match').attr('width'), $('.match').attr('height'))
const rect_width = $('rect').attr('height')
const pad_ = (match_width - rect_width) / 2
const min_dist_ = 900 //квадрат расстояния между rect и match для подстветки
const side = {
	'hor': [match_length, match_width],
	'vert': [match_width, match_length]
}

$('.match.active').on('mousedown touchstart', start_move)
$('.match.active').on('mouseup touchend', drop)