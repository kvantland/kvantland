function block_nav() {
	let nav = document.querySelector('.user_nav')
	if (!nav.classList.contains('blocked'))
		nav.classList.add('blocked')
}

function go_left(e) {
	if (e.touches)
		e.preventDefault()
	let n = document.querySelectorAll('.problem').length
	let cur_page = document.querySelector('.page.selected')
	let cur_problem = document.querySelector('.problem.active')
	let cur_num = cur_problem.getAttribute('num')
	let next_problem = document.querySelector(`.problem[num="${(cur_num - -2) % n}"]`)
	let next_page = document.querySelector(`.page[num="${(cur_num - -(n - 1)) % n}"]`)
	cur_problem.classList.remove('active')
	next_problem.classList.add('active')
	cur_page.classList.remove('selected')
	next_page.classList.add('selected')
	block_nav()
}

function go_right(e) {
	if (e.touches)
		e.preventDefault()
	let n = document.querySelectorAll('.problem').length
	let cur_problem = document.querySelector('.problem.active')
	let cur_page = document.querySelector('.page.selected')
	let cur_num = cur_problem.getAttribute('num')
	let next_problem = document.querySelector(`.problem[num="${(cur_num - -1) % n}"]`)
	let next_page = document.querySelector(`.page[num="${(cur_num - -1) % n}"]`)
	cur_problem.classList.remove('active')
	next_problem.classList.add('active')
	cur_page.classList.remove('selected')
	next_page.classList.add('selected')
	block_nav()
}

function scroll(e) {
	let add = document.querySelector('nav').getBoundingClientRect().height
	if (e.touches)
		e.preventDefault()
	let id = e.target.id
	let X, Y, box, key_obj
	switch(id) {
		case 'info': {
			key_obj = document.querySelector('.info_container').getBoundingClientRect();
			[X, Y] = [key_obj.left, key_obj.top];
			break;
		}
		case 'team': {
			[X, Y] = [-window.pageXOffset, -window.pageYOffset];
			break;
			// key_obj = document.querySelector('.team_container').getBoundingClientRect();
			// [X, Y] = [key_obj.left, key_obj.top]
		}
		case 'examples': {
			key_obj = document.querySelector('.examples_container').getBoundingClientRect();
			[X, Y] = [key_obj.left, key_obj.top];
			break;
		}
		case 'contacts': {
			key_obj = document.querySelector('.contacts_area').getBoundingClientRect();
			[X, Y] = [key_obj.left, key_obj.top];
			break;
		}
	}
	console.log(X, Y)
	window.scrollTo(X + window.pageXOffset, Y - add + window.pageYOffset)
}

for (let menu_button of document.querySelectorAll('.menu_item')) {
	menu_button.addEventListener('click', scroll)
	menu_button.addEventListener('touchstart', scroll)
}

var left = document.querySelector('.left_arrow')
var right = document.querySelector('.right_arrow')

left.addEventListener('click', go_left)
left.addEventListener('touchstart', go_left)

right.addEventListener('click', go_right)
right.addEventListener('touchstart', go_right)