var position = document.documentElement.scrollTop
var nav = document.querySelector('.user_nav')
document.addEventListener('scroll', nav_scroll)

function nav_scroll () {
	if (nav.classList.contains('blocked')) {
		nav.classList.remove('blocked')
		return;
	}
	let cur = document.documentElement.scrollTop
	if (cur < position)
	{
		nav.classList.remove('down')
		nav.classList.add('up')
	}
	else if (cur > position)
	{
		nav.classList.add('down')
		nav.classList.remove('up')
	}
	position = cur
}

function show_out_dialog(e) {
	if (e.touches)
		e.preventDefault();
	let dialog = document.querySelector('.dialog.out')
	let zone = document.createElement('div')
	zone.classList.add('shadow')
	document.body.append(zone)
	if (!dialog.classList.contains('show'))
		dialog.classList.add('show')
	let cancel_button = dialog.querySelector('.button.cancel')
	cancel_button.addEventListener('click', hide_out_dialog)
	cancel_button.addEventListener('touchstart', hide_out_dialog)
}

function hide_out_dialog(e) {
	if (e.touches)
		e.preventDefault();
	let dialog = document.querySelector('.dialog.out')
	let zone = document.querySelector('.shadow')
	if (!zone)
		return;
	zone.remove()
	dialog.classList.remove('show')
	let cancel_button = dialog.querySelector('.button.cancel')
	cancel_button.removeEventListener('click', hide_out_dialog)
	cancel_button.removeEventListener('touchstart', hide_out_dialog)
}

var out_button = nav.querySelector('.logout_button')
if (out_button) {
	out_button.addEventListener('click', show_out_dialog)
	out_button.addEventListener('touchstart', show_out_dialog)
}