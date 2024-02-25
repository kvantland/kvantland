function reload(e){
	if (e.touches)
		e.preventDefault();
	let mail = document.querySelector('.input').innerHTML
	let conf = {'email': mail}
	for (let inp of document.querySelectorAll('input'))
		conf[inp.getAttribute('name')] = inp.value
	let url = new URL(window.location.href + '/send_again')
	let xhr = new XMLHttpRequest()
	xhr.open('POST', url)
	xhr.send(JSON.stringify(conf))
	document.querySelector('.send_again').remove()
	let timer = document.querySelector('.timer')
	timer.classList.remove('hidden')
	let text = timer.innerHTML.split(': ')[0]
	timer.innerHTML = text + ': ' + start_time
	animation = setInterval(function(){go_time()}, 1000)
}

function go_time() {
	let timer = document.querySelector('.timer')
	let [text, time] = timer.innerHTML.split(': ')
	if (time == 1) {
		clearInterval(animation)
		timer.classList.add('hidden')
		let send_button = document.createElement('div')
		send_button.classList.add('send_again')
		send_button.innerHTML = 'Отправить еще раз'
		send_button.addEventListener('click', reload)
		send_button.addEventListener('touchstart', reload)
		timer.after(send_button)
	}
	else
		timer.innerHTML = text + ': ' + (time - 1)
}

var start_time = document.querySelector('.timer').innerHTML.split(': ')[1]
var animation = setInterval(function(){go_time()}, 1000)