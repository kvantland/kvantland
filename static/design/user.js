var position = document.documentElement.scrollTop
var nav = document.querySelector('.user_nav')
document.addEventListener('scroll', nav_scroll)

function nav_scroll () {
	console.log('here')
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