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
	let obj = $(e.currentTarget)
	$('svg').append(obj)
	let svg = $('svg')[0].getBoundingClientRect()
	$(obj).attr({
			'x': getSVGCoordinates(e).x - match_width / 2, 
			'y': getSVGCoordinates(e).y - match_length / 2,
			'transform': 'rotate(0)'})
	$(obj).addClass('targeted')
	update_best()
	$(document).on('mousemove touchmove', move)
}

function move(e) {
	let obj = $('.targeted')
	let svg = $('svg')[0].getBoundingClientRect()
	$(obj).attr({
			'x': getSVGCoordinates(e).x - match_width / 2,
			'y': getSVGCoordinates(e).y - match_length / 2})
	let [x, y] = [e.clientX, e.clientY]
	if (!in_access_zone(obj))
		drop()
	else 
		update_best()
	autoscroll(e.clientX, e.clientY)
}

function back_to_drag(obj=$('.match.targeted:eq(0)')) {
	console.log($(obj).attr('num'))
	let [pos, num] = [$(obj).attr('pos'), $(obj).attr('num')]
	let rect = $(`rect[pos=${pos}][num=${num}]`)
	$(obj).attr('x', $(rect).attr('x') - pad_)
	$(obj).attr('y', $(rect).attr('y'))
	if ($(rect).attr('direction') === 'hor') {
		$(obj).attr('y', $(obj).attr('y') - -rect_width)
		$(obj).attr('transform', `rotate(-90 ${$(rect).attr('x')} ${$(obj).attr('y')})`)
	}
	$(obj).appendTo(`g.num[num=${num}]`)
}

function drop() {
	let obj = $('.targeted')
	if ($('.best').length) {
		let response = true
		let rect = $('.best')
		let [prev_num, prev_pos] = [$(obj).attr('num'), $(obj).attr('pos')]
		let [num, pos] = [$(rect).attr('num'), $(rect).attr('pos')]
		let same = (num == $(obj).attr('num') && pos == $(obj).attr('pos'))
		$(obj).attr({
			'x': $(rect).attr('x') - pad_,
			'y': $(rect).attr('y') - -rect_width * ($(rect).attr('direction') === 'hor'),
			'pos': pos,
			'num': num,
			})
		if ($(rect).attr('direction') === 'hor')
			$(obj).attr('transform', `rotate(-90 ${$(rect).attr('x')} ${$(obj).attr('y')})`)
		rect.removeClass('best')
		$(obj).appendTo(`g.num[num=${num}]`)
		$(obj).removeClass('targeted')

		if (!same) {
			let url = new URL(window.location.href + 'xhr')
			let solution = $('#problem_form')[0].outerHTML
			$.post(url, JSON.stringify({'type': 'move', 'answer': get_answer()}), function(data){
				if (data != 'accepted') {
					show_xhr('Больше перекладывать нельзя!')
					$(obj).attr({
						'pos': prev_pos,
						'num': prev_num,
						})
					back_to_drag($(obj))
				}
				else
					$('.hide_').css('display', 'block')
			})
		}
	}
	else
		back_to_drag()
	$(obj).removeClass('targeted')
	$(document).off('mousemove touchmove')
}

function get_answer() {
	let ans = {}
	$('g.num').each(function(ind){ans[$(this).attr('num')] = []})
	$('.match.active').each(function(ind){
		ans[$(this).attr('num')].push($(this).attr('pos'))
	})
	return JSON.stringify(ans)
}

const match_width = Math.min($('.match').attr('width'), $('.match').attr('height'))
const match_length = Math.max($('.match').attr('width'), $('.match').attr('height'))
const rect_width = $('rect').attr('height')
const pad_ = (match_width - rect_width) / 2
const min_dist_ = 900 //квадрат расстояния между rect и match для подстветки

var scroll_p = $(document.createElement('div')).addClass('scroll_div')
$('body').append(scroll_p)

$('.match.active').on('mousedown touchstart', start_move)
$('.match.active').on('mouseup touchend', drop)

let url = new URL(window.location.href + 'xhr')
$('.reload').on('click touchstart', function(){
	$.post(url, JSON.stringify({'type': 'reload'}), function(data){window.location.reload("true")})})

$('button.submit_button').on('click touchstart', 
	function(){$('input[name="answer"]').val(get_answer())})