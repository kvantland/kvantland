function show_xhr(desc) {
	let dialog = document.querySelector('.xhr_notification')
	block_nav()
	let cross = dialog.querySelector('.cross')
	cross.addEventListener('click', close_xhr)
	cross.addEventListener('touchstart', close_xhr)
	let zone = document.createElement('div')
	zone.classList.add('shadow')
	document.body.append(zone)
	let txt = dialog.querySelector('.text_area').querySelector('.text')
	txt.innerHTML = desc
	if (!dialog.classList.contains('show'))
		dialog.classList.add('show')
}

function close_xhr() {
	let zones = document.querySelectorAll('.shadow')
	if (!zones)
		return;
	for (let zone of zones)
		zone.remove()
	let dialog = document.querySelector('.xhr_notification')
	dialog.classList.remove('show')
}

function block_nav() {
	let nav = document.querySelector('.user_nav')
	if (!nav.classList.contains('blocked'))
		nav.classList.add('blocked')
}