function scroll_to_answer() {
	block_nav()
	let obj = document.querySelector('.problem_desc').getBoundingClientRect()
	let Y = obj.bottom
	let add = window.innerHeight
	window.scrollBy(0, Y - add)
}

function block_nav() {
	let nav = document.querySelector('.user_nav')
	if (!nav.classList.contains('blocked'))
		nav.classList.add('blocked')
}

document.addEventListener('DOMContentLoaded', scroll_to_answer)