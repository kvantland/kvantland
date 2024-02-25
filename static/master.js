window.confirm_answer = confirm_answer// HACK make it available to non-modules, for a reason you’d better not think of

function confirm_answer(ev) {
	if (!confirm('Готовы отправить ответ? Передумать будет нельзя!'))
		ev.preventDefault()
	else
		save_progress()
}

for (let button of document.querySelectorAll(".notification_hint.no")) {
	button.addEventListener('click', close_hint)
	button.addEventListener('touchstart', close_hint)
}

for (let button of document.querySelectorAll(".notifcation_confirm.no")) {
	button.addEventListener('click', close_confirm)
	button.addEventListener('touchstart', close_confirm)
}

for (let button of document.querySelectorAll(".hint_box")) {
	button.addEventListener('click', show_hint)
	button.addEventListener('touchstart', show_hint)
}

for (let button of document.querySelectorAll(".submit_button")) {
	button.addEventListener('click', show_confirm)
	button.addEventListener('touchstart', show_confirm)
}

for (let form of document.querySelectorAll("form.problem"))
	form.onsubmit = function(e){save_progress()}

for (let form of document.querySelectorAll("form.hint"))
	form.onsubmit = function(e){hint_save()}

var progress = document.createElement('input');
progress.type = 'hidden';
progress.name = 'progress';

if (document.querySelector('#problem_form') && !document.querySelector("input[name='progress']"))
	document.querySelector('#problem_form').appendChild(progress);


function hint_save(){
	var interactive = document.querySelector('#interactive_problem_form');
	var form = document.querySelector('#problem_form');
	if (interactive)
		localStorage.setItem("solution", interactive.outerHTML);
	else
		localStorage.setItem("solution", form.outerHTML);
	localStorage.setItem("answer", document.querySelector("input[name='answer']").value);
}

function save_progress(){
	var progress = document.querySelector("input[name='progress']");
	var interactive = document.querySelector('#interactive_problem_form');
	if (interactive)
		progress.value = document.querySelector('#interactive_problem_form').outerHTML;
	else
		progress.value = document.querySelector('#problem_form').outerHTML;
}

function show_hint(){
	close_confirm()
	let dialog = document.querySelector('.hint_notification')
	block_nav()
	let zone = document.createElement('div')
	zone.classList.add('shadow')
	document.body.append(zone)
	if (!dialog.classList.contains('show'))
		dialog.classList.add('show')
	//update_button()
}

function show_confirm() {
	close_hint()
	let dialog = document.querySelector('.confirm_notification')
	block_nav()
	let zone = document.createElement('div')
	zone.classList.add('shadow')
	document.body.append(zone)
	if (!dialog.classList.contains('show'))
		dialog.classList.add('show')
	//update_button()
}

function close_hint() {
	let zone = document.querySelector('.shadow')
	if (!zone)
		return;
	zone.remove()
	let dialog = document.querySelector('.hint_notification')
	dialog.classList.remove('show')
	//update_button()
}

function close_confirm() {
	let zone = document.querySelector('.shadow')
	if (!zone)
		return;
	zone.remove()
	let dialog = document.querySelector('.confirm_notification')
	dialog.classList.remove('show')
	//update_button()
}

function block_nav() {
	let nav = document.querySelector('.user_nav')
	if (!nav.classList.contains('blocked'))
		nav.classList.add('blocked')
}