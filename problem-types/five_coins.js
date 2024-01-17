var coin_width = document.querySelector('.coin circle').getAttribute('r') * 2
var coin_height = document.querySelector('.coin circle').getAttribute('r') * 2

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
	var [el_a, scale_coin, scale_inside, val_a, down_pad] = [obj.getAttribute('ry') / obj.getAttribute('rx'), 0.9, 0.55, Math.random() * 60 -30, 13]

	var tmp = 0

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

	var obj_rx = obj.getAttribute('rx')
	var obj_ry = obj.getAttribute('ry')
	var coin_amount = document.querySelectorAll('.coin').length
	var pos = [];
	for (let k = 0; k < coin_amount; k++)
	{
		var phi = 2 * Math.PI * k / coin_amount - -phi_add
		var [pos_x, pos_y] = [obj_rx * Math.cos(phi) * scale_inside, obj_ry * Math.sin(phi) * scale_inside]
		var tmp = 1;
		for (let coin of document.querySelectorAll('.coin.onscale'))
		{
			if (coin.getAttribute('cup') == obj.classList[1] && k == coin.getAttribute('scale_num'))
				tmp = 0;
		}
		if (tmp)
			pos.push([pos_x, pos_y, k])
	}

	var ind = Math.floor(Math.random() * (pos.length - 1))

	var [x, y, num] = pos[ind]

	document.querySelector(`.inside.${obj.classList[1]}`).after(coin)

	x = x - -obj_rx
	y = y - -obj_ry

	coin.setAttribute('transform', `translate(${x} ${y + down_pad}) scale(${scale_coin} ${el_a * scale_coin}) rotate(${val_a})`)
	if (coin.classList.contains('targeted'))
		coin.classList.remove('targeted')
	coin.classList.add('onscale')
	coin.setAttribute('cup', obj.classList[1])
	coin.setAttribute('scale_num', num)
	document.removeEventListener('mousemove', move)
}

function container_drop(obj){
	var coin = document.querySelector('.targeted')
	if (!coin)
		return;
	if (obj.hasAttribute('occupied'))
		back_to_drag(document.querySelector(`.coin.num_${obj.getAttribute('occupied')}`))
	var x = (obj.getBoundingClientRect().right - -obj.getBoundingClientRect().left) / 2
	var y = (obj.getBoundingClientRect().top - -obj.getBoundingClientRect().bottom) / 2
	moveAt(x, y)
	coin.classList.remove('targeted')
	coin.classList.add('choiced')
	coin.setAttribute('occupied', obj.classList[1].split('_')[1])
	obj.setAttribute('occupied', coin.classList[1].split('_')[1])
	document.removeEventListener('mousemove', move)
}

function dist(obj){
	var coin = document.querySelector('.targeted')
	if (!coin)
		return;
	var coin_x = (coin.getBoundingClientRect().right - -coin.getBoundingClientRect().left) / 2
	var coin_y = (coin.getBoundingClientRect().top - -coin.getBoundingClientRect().bottom) / 2
	var obj_x = (obj.getBoundingClientRect().right - -obj.getBoundingClientRect().left) / 2
	var obj_y = (obj.getBoundingClientRect().top - -obj.getBoundingClientRect().bottom) / 2
	return ((obj_x - coin_x) ** 2) -  -((obj_y - coin_y) ** 2)
}

function check_if_close(obj){
	var coin = document.querySelector('.targeted')
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
	if (coin.classList.contains('.targeted'))
		document.removeEventListener('mousemove', move)
	if (coin.hasAttribute('occupied'))
		coin.removeAttribute('occupied')
	var num = coin.classList[1].split('_')[1]
	var pad = document.querySelectorAll('.coin_container')[1].getAttribute('transform').split(' ')[0].split('(')[1]
	coin.setAttribute('transform', `translate(${(num - 1) * pad - -coin_width / 2} ${coin_height * 1.3})`)
	if (coin.classList.contains('targeted'))
		coin.classList.remove('targeted')
	if (coin.classList.contains('choiced'))
		coin.classList.remove('choiced')
	document.querySelector('.drag_zone').appendChild(coin)
}

function move(event){
	var [cur_X, cur_Y] = [event.clientX, event.clientY]
	var [left, top, right, bottom] = [0, 0, document.documentElement.clientWidth, document.documentElement.clientHeight]
	if (cur_X < right && cur_X > left && cur_Y > top && cur_Y < bottom)
		moveAt(cur_X, cur_Y);
	else
		back_to_drag(document.querySelector('.targeted'));
}

function moveAt(x, y){
	const pt = new DOMPoint(x, y)
	const svgP = pt.matrixTransform(document.querySelector('svg').getScreenCTM().inverse());
	var coin = document.querySelector('.targeted')
	if (!coin)
		return;
	coin.setAttribute('transform', `translate(${svgP.x} ${svgP.y})`)
}

for (coin of document.querySelectorAll('.coin')){
	coin.onmousedown = function(){
		this.classList.add('targeted')
		this.classList.remove('choiced')
		if (this.classList.contains('onscale'))
		{
			this.classList.remove('onscale')
			this.removeAttribute('cup')
			this.removeAttribute('scale_num')
		}
		if (this.hasAttribute('occupied'))
		{
			document.querySelector(`.coin_container_drag.num_${this.getAttribute('occupied')}`).removeAttribute('occupied')
			this.removeAttribute('occupied')
		}
		document.querySelector('svg').appendChild(this)
		moveAt(event.clientX, event.clientY)
		document.addEventListener('mousemove', move)
	}
	coin.onmouseup = function(){
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
				cup_drop(best_obj, this)

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
		up_cup = document.querySelector('.movement.right')
		down_cup = document.querySelector('.movement.left')
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

document.querySelector('.weight').onclick = function(){
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
				let [text, amount] = document.querySelector('.remaining_weightings p').innerHTML.split(':')
				document.querySelector('.remaining_weightings p').innerHTML = text + ': ' + (amount - 1)
				let side = xhr.response
				movement = setInterval(function(){move_scales(side)}, 20)
				movement_tmp = 1
			}
		}
	}
}

document.querySelector('.clean').onclick = function(){
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

document.querySelector('#send').onclick = function(){
	let ans = new Array(document.querySelectorAll('.coin').length).fill(0)
	for (let coin of document.querySelectorAll('.coin.choiced'))
		ans[coin.getAttribute('occupied') - 1] = coin.classList[1].split('_')[1]
	document.querySelector('input').value = ans.join(' ')
}