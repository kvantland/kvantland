var coin_width = document.querySelector('.coin circle').getAttribute('r') * 2
var coin_height = document.querySelector('.coin circle').getAttribute('r') * 2
var x, y

function def_pos()
{
	if (document.querySelector('.remaining_weightings p').innerHTML.split(':')[1] == 2)
	{
		let left = document.querySelector('.cup.left').querySelector('.inside')
		let right = document.querySelector('.cup.right').querySelector('.inside')
		for (let coin of document.querySelectorAll('.coin'))
		{
			if(coin.classList[1].split('_')[1] <= 3)
				cup_drop(left, coin)
			else
				cup_drop(right, coin)
		}
	}
}

document.addEventListener("DOMContentLoaded", def_pos)

function cup_drop(obj, coin){
	let [el_a, scale_coin, scale_inside, val_a, down_pad] = [obj.getAttribute('ry') / obj.getAttribute('rx'), 0.9, 0.55, Math.random() * 60 -30, 13]

	let tmp = 0

	for (let coin_ of document.querySelectorAll('.coin.onscale'))
		if (coin_.getAttribute('cup') == obj.classList[1])
			tmp = 1

	if (!tmp && obj.hasAttribute('phi_add'))
		obj.removeAttribute('phi_add')

	if (obj.hasAttribute('phi_add'))
		phi_add = obj.getAttribute('phi_add')
	else
	{
		phi_add = Math.random() * Math.PI * 2
		obj.setAttribute('phi_add', phi_add)
	}

	let obj_rx = obj.getAttribute('rx')
	let obj_ry = obj.getAttribute('ry')
	let coin_amount = document.querySelectorAll('.coin').length
	let pos = [];
	for (let k = 0; k < coin_amount; k++)
	{
		let phi = 2 * Math.PI * k / coin_amount - -phi_add
		let [pos_x, pos_y] = [obj_rx * Math.cos(phi) * scale_inside, obj_ry * Math.sin(phi) * scale_inside]
		let tmp = 1;
		for (let coin of document.querySelectorAll('.coin.onscale'))
		{
			if (coin.getAttribute('cup') == obj.classList[1] && k == coin.getAttribute('scale_num'))
				tmp = 0;
		}
		if (tmp)
			pos.push([pos_x, pos_y, k])
	}

	let ind = Math.floor(Math.random() * (pos.length - 1))

	let [x, y, num] = pos[ind]

	document.querySelector(`.inside.${obj.classList[1]}`).after(coin)

	x = x - -obj_rx
	y = y - -obj_ry

	coin.setAttribute('transform', `translate(${x} ${y + down_pad}) scale(${scale_coin} ${el_a * scale_coin}) rotate(${val_a})`)
	if (coin.classList.contains('targeted'))
		coin.classList.remove('targeted')
	coin.classList.add('onscale')
	coin.setAttribute('cup', obj.classList[1])
	coin.setAttribute('scale_num', num)
	document.removeEventListener("mousemove", move)
	document.removeEventListener("touchmove", move)
}

function container_drop(obj){
	let coin = document.querySelector('.targeted')
	if (!coin)
		return;
	if (obj.hasAttribute('occupied'))
		back_to_drag(document.querySelector(`.coin.num_${obj.getAttribute('occupied')}`))
	let x = (obj.getBoundingClientRect().right - -obj.getBoundingClientRect().left) / 2
	let  y = (obj.getBoundingClientRect().top - -obj.getBoundingClientRect().bottom) / 2
	moveAt(x, y)
	coin.classList.remove('targeted')
	coin.classList.add('choiced')
	coin.setAttribute('occupied', obj.classList[1].split('_')[1])
	obj.setAttribute('occupied', coin.classList[1].split('_')[1])
	document.removeEventListener("mousemove", move)
	document.removeEventListener("touchmove", move)
}

function dist(obj){
	let coin = document.querySelector('.targeted')
	if (!coin)
		return;
	let coin_x = (coin.getBoundingClientRect().right - -coin.getBoundingClientRect().left) / 2
	let coin_y = (coin.getBoundingClientRect().top - -coin.getBoundingClientRect().bottom) / 2
	let obj_x = (obj.getBoundingClientRect().right - -obj.getBoundingClientRect().left) / 2
	let obj_y = (obj.getBoundingClientRect().top - -obj.getBoundingClientRect().bottom) / 2
	return ((obj_x - coin_x) ** 2) -  -((obj_y - coin_y) ** 2)
}

function check_if_close(obj){
	let coin = document.querySelector('.targeted')
	if (!coin)
		return false;
	if (obj.getBoundingClientRect().left > coin.getBoundingClientRect().right)
		return false;
	if (obj.getBoundingClientRect().right < coin.getBoundingClientRect().left)
		return false;
	if (obj.getBoundingClientRect().top > coin.getBoundingClientRect().bottom)
		return false;
	if (obj.getBoundingClientRect().bottom < coin.getBoundingClientRect().top)
		return false;
	return true;
}

function back_to_drag(coin){
	if (!coin)
		return;
	if (coin.classList.contains('targeted'))
	{
		document.removeEventListener("mousemove", move)
		document.removeEventListener("touchmove", move)
	}
	if (coin.hasAttribute('occupied'))
		coin.removeAttribute('occupied')
	let num = coin.classList[1].split('_')[1]
	let pad = document.querySelectorAll('.coin_container')[1].getAttribute('transform').split(' ')[0].split('(')[1]
	coin.setAttribute('transform', `translate(${(num - 1) * pad - -coin_width / 2} ${coin_height * 1.3})`)
	if (coin.classList.contains('targeted'))
		coin.classList.remove('targeted')
	if (coin.classList.contains('choiced'))
		coin.classList.remove('choiced')
	document.querySelector('.drag_zone').appendChild(coin)
}

function screen_border_check(x, y) {
	let [right, f_right] = [window.innerWidth, document.documentElement.scrollWidth]
	let [bott, f_bott] = [window.innerHeight, document.documentElement.scrollHeight]
	if (x >= right && window.scrollX >= f_right - right)
		return false
	if (x <= 0 && window.scrollX <= 0)
		return false
	if (y <= 0 && window.scrollY <= 0)
		return false
	if (y >= bott && window.scrollY >= f_bott - bott)
		return false
	return true
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

function move(event) {
	let cur_X, cur_Y
	if (event.touches) {
		cur_X = event.touches[0].clientX
		cur_Y = event.touches[0].clientY
		event.preventDefault()
	}
	else {
		cur_X = event.clientX
		cur_Y = event.clientY
	}
	autoscroll(cur_X, cur_Y)
	if (screen_border_check(cur_X, cur_Y))
		moveAt(cur_X, cur_Y)
	else
		back_to_drag(document.querySelector('.targeted'))
}

function moveAt(x, y){
	const pt = new DOMPoint(x, y)
	const svgP = pt.matrixTransform(document.querySelector('svg').getScreenCTM().inverse());
	var coin = document.querySelector('.targeted')
	if (!coin)
		return;
	coin.setAttribute('transform', `translate(${svgP.x} ${svgP.y})`)
}

function start(event, obj) {
	obj.classList.add('targeted')
	obj.classList.remove('choiced')
	if (obj.classList.contains('onscale'))
	{
		obj.classList.remove('onscale')
		obj.removeAttribute('cup')
		obj.removeAttribute('scale_num')
	}
	if (obj.hasAttribute('occupied'))
	{
		document.querySelector(`.coin_container_drag.num_${obj.getAttribute('occupied')}`).removeAttribute('occupied')
		obj.removeAttribute('occupied')
	}
	document.querySelector('svg').appendChild(obj)
	let cur_X, cur_Y
	if (event.touches) {
		cur_X = event.touches[0].clientX
		cur_Y = event.touches[0].clientY
		event.preventDefault()
	}
	else {
		cur_X = event.clientX
		cur_Y = event.clientY
	}
	moveAt(cur_X, cur_Y)
	document.addEventListener("mousemove", move)
	document.addEventListener("touchmove", move)
}

function end(event, obj) {
	if (!document.querySelector('.targeted'))
		return;
	else{
		var best_dist = 10 ** 8
		var best_obj = null
		for (cup of document.querySelectorAll('.cup'))
			if (check_if_close(cup.querySelector('.inside')))
				if (dist(cup.querySelector('.inside')) < best_dist)
					[best_dist, best_obj] = [dist(cup.querySelector('.inside')), cup.querySelector('.inside')]

		if (best_obj)
			cup_drop(best_obj, obj)

		if (best_dist == 10 ** 8)
		{
			for (cont of document.querySelectorAll('.coin_container_drag'))
				if (check_if_close(cont))
					if (dist(cont)  < best_dist)
						[best_dist, best_obj] = [dist(cont), cont]
		
			if (best_obj)
				container_drop(best_obj)
		}

		if (document.querySelector('.targeted'))
			back_to_drag(document.querySelector('.targeted'))
	}
}

for (let coin of document.querySelectorAll('.coin')){
	coin.addEventListener("mousedown", (e) => start(e, coin))
	coin.addEventListener("touchstart", (e) => start(e, coin))
	coin.addEventListener("mouseup",(e) => end(e, coin))
	coin.addEventListener("touchend", (e) => end(e, coin))
}

var [movement, movement_tmp] = ['', 0]

function move_scales(side)
{
	let up_cup, down_cup, angle
	if (side == 'left')
	{
		up_cup = document.querySelector('.movement.right')
		down_cup = document.querySelector('.movement.left')
	}
	if (side == 'right')
	{
		up_cup = document.querySelector('.movement.left')
		down_cup = document.querySelector('.movement.right')
	}
	if (side == 'equal')
	{
		if (document.querySelector('.plank').hasAttribute('transform'))
		{
			let cur_ang = document.querySelector('.plank').getAttribute('transform').split('(')[1].split(')')[0].split(' ')[0]
			if (cur_ang < 0)
			{
				up_cup = document.querySelector('.movement.left')
				down_cup = document.querySelector('.movement.right')
			}
			else
			{
				up_cup = document.querySelector('.movement.right')
				down_cup = document.querySelector('.movement.left')
			}
		}
		else
		{
			up_cup = document.querySelector('.movement.right')
			down_cup = document.querySelector('.movement.left')
		}
	}

	let plank = document.querySelector('.plank')
	let plank_len = plank.getAttribute('width') / 2
	let plank_height = plank.getAttribute('height') / 2

	if (plank.hasAttribute('transform'))
		angle = plank.getAttribute('transform').split('(')[1].split(')')[0].split(' ')[0]
	else
		angle = 0

	if (side == 'left' && angle <= -10 || side == 'right' && angle >= 10 || side == 'equal' && angle == 0)
	{
		clearInterval(movement)
		movement_tmp = 0
	}
	else
	{
		let rad_ = Math.PI / 180 * angle
		if (down_cup == document.querySelector('.movement.left'))
		{
			up_cup.setAttribute('transform', `translate(${-(1 - Math.cos(rad_)) * plank_len - -plank_height * Math.sin(rad_)} ${Math.sin(rad_) * plank_len - plank_height * Math.cos(rad_)})`)
			down_cup.setAttribute('transform', `translate(${(1 - Math.cos(rad_)) * plank_len -plank_height * Math.sin(rad_)} ${-Math.sin(rad_) * plank_len + plank_height * Math.cos(rad_)})`)
			plank.setAttribute('transform', `rotate(${angle - 1} ${plank_len} ${plank_height})`)
		}
		else
		{
			up_cup.setAttribute('transform', `translate(${(1 - Math.cos(rad_)) * plank_len - -plank_height * Math.sin(rad_)} ${-Math.sin(rad_) * plank_len - plank_height * Math.cos(rad_)})`)
			down_cup.setAttribute('transform', `translate(${-(1 - Math.cos(rad_)) * plank_len - plank_height * Math.sin(rad_)} ${Math.sin(rad_) * plank_len + plank_height * Math.cos(rad_)})`)
			plank.setAttribute('transform', `rotate(${angle - -1} ${plank_len} ${plank_height})`)
		}
	}
}

document.querySelector('.weight').addEventListener("click", (e) => weight(e))
document.querySelector('.weight').addEventListener("touchstart", (e) => weight(e))

function weight(e){
	if (e.targetTouches)
		e.preventDefault()
	let url = new URL(window.location.href + 'xhr')
	var conf = ''
	for (let num = 1; num <= document.querySelectorAll('.coin').length; num++)
	{
		if (document.querySelector(`.coin.num_${num}`).hasAttribute('cup'))
		{
			if (document.querySelector(`.coin.num_${num}`).getAttribute('cup') == 'left')
				conf += '1'
			else
				conf += '2'
		}
		else
			conf += '0'
	}
	let xhr = new XMLHttpRequest()
	xhr.open('POST', url)
	xhr.responseType = 'text'
	xhr.send(JSON.stringify({'conf': conf}));
	xhr.onload = function() {
		if (xhr.status != 200)
			alert(`Ошибка ${xhr.status}: ${xhr.statusText}`)
		else
		{
			if (xhr.response == 'no_tries')
				alert('Больше нельзя делать взвешивания!')
			else
			{
				let sign = {'equal': '=', 'right': '<', 'left': '>'}
				let [h_left, h_right] = [[], []]
				let cnt = 0
				let coin_name = ['A', 'B', 'C', 'D', 'E']
				for (let i of conf) {
					if (i == '1')
						h_left.push(coin_name[cnt])
					if (i == '2')
						h_right.push(coin_name[cnt])
					cnt += 1
				}
				let [text, amount] = document.querySelector('.remaining_weightings p').innerHTML.split(':')
				let hist = document.querySelector('.history')
				let h_item = document.createElement('div')
				hist.append(h_item)
				document.querySelector('.remaining_weightings p').innerHTML = text + ': ' + (amount - 1)
				let side = xhr.response
				let h_text = '(' + h_left.join(', ') + `) ${sign[side]} (` + h_right.join(', ') + ')'
				h_item.classList.add('item')
				h_item.innerHTML = `<div class="header"> Взвешивание ${3 - amount} </div> <p> ${h_text} </p>`
				movement = setInterval(function(){move_scales(side)}, 20)
				movement_tmp = 1
			}
		}
	}
}

function clean(e) {
	if (e.targetTouches)
		e.preventDefault()
	if (!movement_tmp)
	{
		for (let coin of document.querySelectorAll('.coin'))
			if (coin.classList.contains('onscale'))
			{
				coin.classList.remove('onscale')
				coin.removeAttribute('cup')
				coin.removeAttribute('scale_num')
				back_to_drag(coin)
			}
		document.querySelector('.plank').removeAttribute('transform')
		for (let cup of document.querySelectorAll('.movement'))
			cup.removeAttribute('transform')
	}
}

document.querySelector('.clean').addEventListener("click", (e) => clean(e))
document.querySelector('.clean').addEventListener("touchstart", (e) => clean(e))

function send(e) {
	let ans = new Array(document.querySelectorAll('.coin').length).fill(0)
	for (let coin of document.querySelectorAll('.coin.choiced'))
		ans[coin.getAttribute('occupied') - 1] = coin.classList[1].split('_')[1]
	document.querySelector('input').value = ans.join(' ')
}

document.querySelector('#send').addEventListener("click", (e) => send(e))
document.querySelector('#send').addEventListener("touchstart", (e) => send(e))