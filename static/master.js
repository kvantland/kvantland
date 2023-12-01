window.confirm_answer = confirm_answer // HACK make it available to non-modules, for a reason you’d better not think of

function confirm_answer(ev) {
	if (!confirm('Готовы отправить ответ? Передумать будет нельзя!'))
		ev.preventDefault()
}

function confirm_hint(ev) {
	if (!confirm('Вы точно хотите получить подсказку? Её стоимость 1 квантик.'))
		ev.preventDefault()
	else
		save_progress()
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

var hint_progress = document.createElement('input')
hint_progress.type = 'hidden';
hint_progress.name = 'hint_progress';


var hint_answer = document.createElement('input')
hint_answer.type = 'hidden';
hint_answer.name = 'hint_answer';

var anwer_value = document.getElementsByName('answer')[0].value;

var send_button = document.querySelector('#send');
var interactive = document.querySelector('#interactive_problem_form');
var form = document.querySelector('#problem_form');
var hint_form = document.querySelector('#hint');

form.appendChild(progress);
hint_form.appendChild(hint_progress);

function save_progress(){
	if (interactive)
	{
		progress.value = interactive.outerHTML;
		hint_progress.value = interactive.outerHTML;
		hint_answer.value = answer.value;
	}
	else
	{
		progress.value = form.outerHTML;
		hint_progress.value = form.outerHTML;
		hint_answer.value = answer.value;
	}
}

send_button.addEventListener('click', save_progress);

