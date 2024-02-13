var buttons = document.querySelectorAll('.active');
var unknowns = document.querySelectorAll('.unknown');
var R = document.querySelector('.slot').getAttribute('height') / 2 / Math.sin(Math.PI / 10)
var height = document.querySelector('.slot').getAttribute('height') / 2

function transform(obj) {
	let angle = obj.getAttribute('angle')
	let y = Math.abs(R * Math.sin(angle))
	let scale = Math.cos(angle)
	obj.setAttribute('y', height - y * obj.getAttribute('sgn'))
	obj.setAttribute('transform', `scale(1 ${scale})`)
}

function back_to_default(tmp, column) {
	let up = document.querySelectorAll('.up_number')[column]
	let down = document.querySelectorAll('.bottom_number')[column]
	let cur = document.querySelectorAll('.unknown')[column]
	up.setAttribute('y', -height)
	up.removeAttribute('transform')
	down.setAttribute('y', 3 * height)
	down.removeAttribute('transform')
	cur.setAttribute('y', height)
	cur.removeAttribute('transform')

	if (cur.getAttribute('unset') - 1 == 0)
	{
		cur.innerHTML = 0
		if (tmp == 1)
			cur.innerHTML = 9
		cur.setAttribute('unset', 0)
	}
	else
		cur.innerHTML = (cur.innerHTML - -tmp + 10) % 10

	up.innerHTML = (cur.innerHTML - -9) % 10
	down.innerHTML = (cur.innerHTML - -11) % 10

	cur.setAttribute('angle', 0)
	up.setAttribute('angle', Math.PI / 5)
	down.setAttribute('angle', Math.PI / 5)
}

function move(tmp, column) {
	let add = (Math.PI / 5) / 20
	let up = document.querySelectorAll('.up_number')[column]
	let down = document.querySelectorAll('.bottom_number')[column]
	let cur = document.querySelectorAll('.unknown')[column]
	if (tmp == 1)
		down.setAttribute('angle', down.getAttribute('angle') - add)
	else
		up.setAttribute('angle', up.getAttribute('angle') - add)
	cur.setAttribute('sgn', tmp)
	cur.setAttribute('angle', cur.getAttribute('angle') - -add)
	transform(up)
	transform(down)
	transform(cur)
	if ((down.getAttribute('angle') - 0) < 10 ** (-4) || (up.getAttribute('angle') -0) < 10 ** (-4))
	{
		clearInterval(animation_arr[column])
		animation_arr[column] = ''
		movement_tmp[column] = 0
		back_to_default(tmp, column)
	}
}

var animation_arr = []
var movement_tmp = []

for (let i of document.querySelectorAll('.slot')){
	animation_arr.push('')
	movement_tmp.push(0)
}

function change(e, obj) {
	if (e.targetTouches)
		e.preventDefault()
	let column = obj.getAttribute('num')
	if (movement_tmp[column])
		return;
	let tmp = -1	
	if (obj.classList.contains('top'))
		tmp = 1
	animation_arr[column] = setInterval(function(){move(tmp, column)}, 20)
	movement_tmp[column] = 1
}


for (const button of buttons){
	button.addEventListener("click", (e) => change(e, button))
	button.addEventListener("touchstart", (e) => change(e, button))
}

function reload(e) {
	if (e.targetTouches)
		e.preventDefault()
	for (let column = 0; column < unknowns.length; column++){
	let up = document.querySelectorAll('.up_number')[column]
	let down = document.querySelectorAll('.bottom_number')[column]
	let cur = document.querySelectorAll('.unknown')[column]
	cur.innerHTML = '*';
	cur.setAttribute('unset', 1)
	up.innerHTML = '0'
	down.innerHTML = '9'
	}
}

document.querySelector('.reload').addEventListener("click", (e) => reload(e))
document.querySelector('.reload').addEventListener("touchstart", (e) => reload(e))

function xhr_request(xhr) {
	if (xhr.status != 200)
			show_xhr(`Ошибка ${xhr.status}: ${xhr.statusText}`)
		else
		{
			if (xhr.response == 'no_tries')
				show_xhr('Больше нельзя делать проверок!')
			else
				{
					if (xhr.response == 'false')
						show_xhr('Неверная комбинация!')
					else
						show_xhr('Верная комбинация!')
					let [text, cur_amount] = document.querySelector('.remaining_checks p').innerHTML.split(': ')
					if (xhr.response == 'true' || cur_amount == '0')
						window.location.reload('true')
				}
		}
}

function check(e) {
	if (e.targetTouches)
		e.preventDefault()
	for (let i = 0; i < animation_arr.length; i++)
	{
		clearInterval(animation_arr[i])
		animation_arr[i] = ''
		movement_tmp[i] = 0
	}

	let [text, cur_amount] = document.querySelector('.remaining_checks p').innerHTML.split(': ')
	document.querySelector('.remaining_checks p').innerHTML = text + ': ' + (cur_amount - 1)

	let url = new URL(window.location.href + 'xhr')
	let ans = ''
	for (const u of unknowns) {
		ans += u.innerHTML;
	}
	let solution = document.querySelector('#interactive_problem_form').outerHTML
	let xhr = new XMLHttpRequest()
	xhr.open('POST', url)
	xhr.responseType = 'text'
	xhr.send(JSON.stringify({'answer': ans, 'solution': solution}));
	xhr.onload = function() {xhr_request(xhr)}
}

document.querySelector('.check ').addEventListener("click", (e) => check(e))
document.querySelector('.check ').addEventListener("touchstart", (e) => check(e))
