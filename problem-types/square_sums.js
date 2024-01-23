function get_cur_coord(obj){
	let [first_part, pre_second_part] = obj.getAttribute('transform').split('translate(')
	let [second_part, third_part] = pre_second_part.split(')')
	let coord = second_part.split(' ')
	return coord
}

function exchange(obj_1, obj_2, pos_1, pos_2){
	let cur_pos_1 = get_cur_coord(obj_1)[0]
	let cur_pos_2 = get_cur_coord(obj_2)[0]
	let sgn = (pos_2 - pos_1) / Math.abs(pos_2 - pos_1)
	let step = sgn * 36

	if (cur_pos_1 != pos_2 || cur_pos_2 != pos_1)
	{
		if (Math.abs(cur_pos_1 - pos_2) >= Math.abs(step))
			move(obj_1, step, 0)
		else
			move(obj_1, pos_2 - cur_pos_1, 0)
		if (Math.abs(cur_pos_1 - pos_2) >= Math.abs(step))
			move(obj_2, -step, 0)
		else
			move(obj_2, pos_1 - cur_pos_2, 0)
	}
	else
	{
		clearInterval(movement)
		movement_tmp = 0
		hide_interface()
	}
}

function move(obj, x, y){
	let [first_part, pre_second_part] = obj.getAttribute('transform').split('translate(')
	let [second_part, third_part] = pre_second_part.split(')')
	let [cur_x, cur_y] = second_part.split(' ')
	let [new_x, new_y] = [cur_x - -x, cur_y - -y]
	obj.setAttribute('transform', first_part + 'translate(' + new_x + ' ' + new_y + ')' + third_part)
}

function show_interface(e){
	if ('ontouchstart' in window)
		e.preventDefault()
	let sel_list = document.querySelectorAll('.selected')
	let bar_width = document.querySelector('.exchange_bar').getAttribute('bar_width')
	if (sel_list.length == 2)
	{
		let new_x = (get_cur_coord(sel_list[0])[0] - -get_cur_coord(sel_list[1])[0] - -sel_list[0].getAttribute('card_width')) / 2
		document.querySelector('.exchange_bar').setAttribute('transform', `translate(${new_x - bar_width / 2}, 0)`)
		document.querySelector('.exchange_bar').classList.remove('hidden')
		document.querySelector('.exchange_bar').classList.add('active')
	}
}

function hide_interface(){
	for (card of document.querySelectorAll('.selected'))
		{
			card.classList.remove('selected')
			move(card, 0, 10)
		}
	document.querySelector('.exchange_bar').classList.remove('active')
	document.querySelector('.exchange_bar').classList.add('hidden')
}

function choose(e, obj) {
	if (e.targetTouches)
		e.preventDefault()
	if (movement_tmp)
		return;
	if (!document.querySelector('.exchange_bar.active'))
	{
		if (obj.classList.contains('selected'))
		{
			obj.classList.remove('selected')
			move(obj, 0, 10)
		}
		else
		{
			obj.classList.add('selected')
			move(obj, 0, -10)
			obj.parentNode.appendChild(obj)
		}
	}
}

for (let card of document.querySelectorAll('.card'))
{
	card.addEventListener("click", (e) => choose(e, card))
	card.addEventListener("touchstart", (e) => choose(e, card))
}

var [pos_1, pos_2] = [0, 0]
var [movement, movement_tmp] = ['', 0]

function start_exchange(e) {
	if (e.targetTouches)
		e.preventDefault()
	if (movement_tmp)
		return;
	let [card_1, card_2] = document.querySelectorAll('.selected')
	let url = new URL(window.location.href + 'xhr')
	let selected = card_1.getAttribute('num') + ' ' + card_2.getAttribute('num')

	let xhr = new XMLHttpRequest()
	xhr.open('POST', url)
	xhr.responseType = 'text'
	xhr.send(JSON.stringify({'selected': selected}));

	xhr.onload = function() {
		if (xhr.status != 200)
			alert(`Ошибка ${xhr.status}: ${xhr.statusText}`)
		else
		{
			if (xhr.response == 'rejected'){
				alert('Сумма номеров не явялется полным квадратом!')
				hide_interface()
			}
			else
			{
				[pos_1, pos_2] = [get_cur_coord(card_1)[0], get_cur_coord(card_2)[0]]
				movement = setInterval(function(){exchange(card_1, card_2, pos_1, pos_2)}, 20)
				movement_tmp = 1
			}
		}
	}
}

document.querySelector('.icon.exchange').addEventListener("click", (e) => start_exchange(e))
document.querySelector('.icon.exchange').addEventListener("touchstart", (e) => start_exchange(e))

function hide(e) {
	if (e.targetTouches)
		e.preventDefault()
	if (movement_tmp)
		return;
	hide_interface()
}

document.querySelector('.icon.cross').addEventListener("click", (e) => hide(e))
document.querySelector('.icon.cross').addEventListener("touchstart", (e) => hide(e))

document.addEventListener('click', (e) => show_interface(e))
document.addEventListener('touchstart', (e) => show_interface(e))

function reload(e) {
	if (e.targetTouches)
		e.preventDefault()
	if (movement_tmp)
		return;
	let url = new URL(window.location.href + 'xhr')
	url.searchParams.set('reload', 'true')

	let xhr = new XMLHttpRequest()
	xhr.open('POST', url)
	xhr.responseType = 'text'
	xhr.send(JSON.stringify({'reload': 'true'}))

	xhr.onload = function(){
		if (xhr.status != 200)
			alert(`Ошибка ${xhr.status}: ${xhr.statusText}`)
		else
			window.location.reload('true')
	}
}

document.querySelector('.reload').addEventListener("click", (e) => reload(e))
document.querySelector('.reload').addEventListener("touchstart", (e) => reload(e))
