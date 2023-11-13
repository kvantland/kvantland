window.confirm_answer = confirm_answer // HACK make it available to non-modules, for a reason you’d better not think of

function confirm_answer(ev) {
	if (!confirm('Готовы отправить ответ? Передумать будет нельзя!'))
		ev.preventDefault()
}

function confirm_hint(ev) {
	if (!confirm('Точно запросить подсказку?'))
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
var form = document.querySelector('#problem_form');
form.style['z-index'] = 'inherit';

form.appendChild(progress);

function save_progress(){
	progress.value = form.outerHTML;
}

send_button.addEventListener('click', save_progress);

