function close_answer(e) {
	if (e.touches)
		e.preventDefault()
	let zone = document.querySelector('.shadow')
	zone.remove()
	let num = document.querySelector('.problem.active').getAttribute('num')
	let dialog = document.querySelector(`.dialog.answer[num="${num}"]`)
	dialog.classList.remove('show')
}

function show_answer() {
	let num = document.querySelector('.problem.active').getAttribute('num')
	let dialog = document.querySelector(`.dialog.answer[num="${num}"]`)
	let cross = dialog.querySelector('.cross')
	block_nav()
	let zone = document.createElement('div')
	zone.classList.add('shadow')
	document.body.append(zone)
	if (!dialog.classList.contains('show'))
		dialog.classList.add('show')
	cross.addEventListener('click', close_answer)
	cross.addEventListener('touchstart', close_answer)
}

function show_solution() {
	let num = document.querySelector('.problem.active').getAttribute('num')
	let dialog = document.querySelector(`.dialog.solution[num="${num}"]`)
	block_nav()
	dialog.classList.add('show')
}

function update_button() {
	let answer = document.querySelector('.problem.active .answer')
	let solution = document.querySelector('.problem.active .solution')
	answer.addEventListener('click', show_answer)
	answer.addEventListener('touchstart', show_answer)
	solution.addEventListener('click', show_solution)
	answer.addEventListener('touchstart', show_answer)
}

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
	update_button()
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
	update_button()
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

update_button()