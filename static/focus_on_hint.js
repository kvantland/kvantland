function scroll_to_hint() {
	block_nav()
	let obj = document.querySelector('.hint_wrapper').getBoundingClientRect()
	let Y = obj.bottom
	let add = window.innerHeight
	window.scrollBy(0, Y - add)
}

document.addEventListener('DOMContentLoaded', scroll_to_hint)