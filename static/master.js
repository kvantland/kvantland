window.confirm_answer = confirm_answer // HACK make it available to non-modules, for a reason you’d better not think of

function confirm_answer(ev) {
	if (!confirm('Готовы отправить ответ? Передумать будет нельзя!'))
		ev.preventDefault()
}

function confirm_hint(ev) {
	if (!confirm('Точно запросить подсказку? Её стоимость составляет 1 квантик.'))
		ev.preventDefault()
}

for (let form of document.querySelectorAll("form.problem")) {
	form.addEventListener('submit', confirm_answer)
}

for (let form of document.querySelectorAll("form.hint")) {
	form.addEventListener('submit', confirm_hint)
}

var progress = document.createElement('input');
progress.type = 'hidden';
progress.name = 'progress';

var send_button = document.querySelector('#send');
var interactive = document.querySelector('#interactive_problem_form');
var form = document.querySelector('#problem_form');

form.appendChild(progress);

function save_progress(){
	if (interactive)
		progress.value = interactive.outerHTML;
	else
		progress.value = form.outerHTML;
}

send_button.addEventListener('click', save_progress);

