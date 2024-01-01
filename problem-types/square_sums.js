function exchange(obj_1, obj_2){
	let pos_1 = obj_1.getAttribute('transform')
	let pos_2 = obj_2.getAttribute('transform')
	obj_1.setAttribute('transform', pos_2)
	obj_2.setAttribute('transform', pos_1)
}

function get_cur_coord(obj){
	let [first_part, pre_second_part] = obj.getAttribute('transform').split('translate(')
	let [second_part, third_part] = pre_second_part.split(')')
	let coord = second_part.split(' ')
	return coord
}

function move(obj, x, y){
	let [first_part, pre_second_part] = obj.getAttribute('transform').split('translate(')
	let [second_part, third_part] = pre_second_part.split(')')
	let [cur_x, cur_y] = second_part.split(' ')
	let [new_x, new_y] = [cur_x - -x, cur_y - -y]
	obj.setAttribute('transform', first_part + 'translate(' + new_x + ' ' + new_y + ')' + third_part)
}

function show_interface(){
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

for (card of document.querySelectorAll('.card'))
{

	card.onclick = function(){
		if (!document.querySelector('.exchange_bar.active'))
		{
			if (this.classList.contains('selected'))
			{
				this.classList.remove('selected')
				move(this, 0, 10)
			}
			else
			{
				this.classList.add('selected')
				move(this, 0, -10)
			}
		}
	}
}


document.querySelector('.icon.exchange').onclick = function(){
	let [card_1, card_2] = document.querySelectorAll('.selected')
	let url = new URL(window.location.href + 'xhr')
	let selected = card_1.getAttribute('num') + ' ' + card_2.getAttribute('num')

	url.searchParams.set('selected', selected)

	let xhr = new XMLHttpRequest()
	xhr.open('GET', url)
	xhr.responseType = 'text'
	xhr.send();

	xhr.onload = function() {
		if (xhr.status != 200)
			alert(`Ошибка ${xhr.status}: ${xhr.statusText}`)
		else
		{
			if (xhr.response == 'rejected')
				alert('Сумма номеров не явялется полным квадратом!')
			else
				exchange(card_1, card_2)
		}
	}
	for (card of document.querySelectorAll('.selected'))
	{
		card.classList.remove('selected')
		move(card, 0, 10)
	}
	document.querySelector('.exchange_bar').classList.remove('active')
	document.querySelector('.exchange_bar').classList.add('hidden')
}

document.querySelector('.icon.cross').onclick = function(){
	for (card of document.querySelectorAll('.selected'))
	{
		card.classList.remove('selected')
		move(card, 0, 10)
	}
	document.querySelector('.exchange_bar').classList.remove('active')
	document.querySelector('.exchange_bar').classList.add('hidden')
}

document.addEventListener('click', show_interface)

document.querySelector('.reload').onclick = function(){
	let url = new URL(window.location.href + 'xhr')
	url.searchParams.set('reload', 'true')

	let xhr = new XMLHttpRequest()
	xhr.open('GET', url)
	xhr.responseType = 'text'
	xhr.send()

	xhr.onload = function(){
		if (xhr.status != 200)
			alert(`Ошибка ${xhr.status}: ${xhr.statusText}`)
		else
			location.reload()
	}
}