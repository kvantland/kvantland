function reload(e){
	if (e.touches)
		e.preventDefault();
	window.location.reload('true')
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

var animation = setInterval(function(){go_time()}, 1000)