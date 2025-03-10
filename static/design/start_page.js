function stopVideo() {
	let num = document.querySelector('.problem.active').getAttribute('num')
	let video = document.querySelector(`.dialog.solution[num="${num}"] iframe`)
	video.contentWindow.postMessage('{"event":"command","func":"stopVideo","args":""}', '*')
}


function close_answer() {
	let zone = document.querySelector('.shadow')
	if (!zone)
		return;
	zone.remove()
	let num = document.querySelector('.problem.active').getAttribute('num')
	let dialog = document.querySelector(`.dialog.answer[num="${num}"]`)
	let cross = dialog.querySelector('.cross')
	cross.addEventListener('click', close_answer)
	cross.addEventListener('touchstart', close_answer)
	dialog.classList.remove('show')
	update_button()
}

function close_solution() {
	let zone = document.querySelector('.shadow')
	if (!zone)
		return;
	zone.remove()
	let num = document.querySelector('.problem.active').getAttribute('num')
	let dialog = document.querySelector(`.dialog.solution[num="${num}"]`)
	let cross = dialog.querySelector('.cross')
	cross.addEventListener('click', close_solution)
	cross.addEventListener('touchstart', close_solution)
	dialog.classList.remove('show')
	update_button()
	stopVideo()
}

function show_answer() {
	close_solution()
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
	update_button()
}

function show_solution() {
	close_answer()
	let num = document.querySelector('.problem.active').getAttribute('num')
	let dialog = document.querySelector(`.dialog.solution[num="${num}"]`)
	let cross = dialog.querySelector('.cross')
	block_nav()
	let zone = document.createElement('div')
	zone.classList.add('shadow')
	document.body.append(zone)
	if (!dialog.classList.contains('show'))
		dialog.classList.add('show')
	cross.addEventListener('click', close_solution)
	cross.addEventListener('touchstart', close_solution)
	update_button()
}

function update_button() {
	let answer_button = document.querySelectorAll('.button.answer')
	let solution_button = document.querySelectorAll('.button.solution')
	for (let answer of answer_button) {
		answer.addEventListener('click', show_answer)
		answer.addEventListener('touchstart', show_answer)
	}
	for (let solution of solution_button) {
		solution.addEventListener('click', show_solution)
		solution.addEventListener('touchstart', show_answer)
	}
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
	let id = e.currentTarget.id
	let X, Y, box, key_obj
	switch(id) {
		case 'info': {
			key_obj = document.querySelector('.info_container').getBoundingClientRect();
			[X, Y] = [key_obj.left, key_obj.top];
			break;
		}
		case 'team': {
			key_obj = document.querySelector('.team_container').getBoundingClientRect();
			[X, Y] = [key_obj.left, key_obj.top]
			break;
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
	block_nav()
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