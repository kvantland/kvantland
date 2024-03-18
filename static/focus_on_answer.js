function scroll_to_answer() {
	block_nav()
	let obj = document.querySelector('.problem_desc').getBoundingClientRect()
	let Y = obj.bottom
	let add = window.innerHeight
	window.scrollBy(0, Y - add)
}

document.addEventListener('DOMContentLoaded', scroll_to_answer)