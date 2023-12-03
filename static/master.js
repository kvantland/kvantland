window.confirm_answer = confirm_answer // HACK make it available to non-modules, for a reason you’d better not think of

function confirm_answer(ev) {
	if (!confirm('Готовы отправить ответ? Передумать будет нельзя!'))
		ev.preventDefault()
}

function confirm_hint(ev) {
	if (!confirm('Вы точно хотите получить подсказку? Её стоимость 1 квантик.'))
		ev.preventDefault()
	hint_save()
}

for (let form of document.querySelectorAll("form.problem")) {
	form.addEventListener('submit', confirm_answer)
}

for (let form of document.querySelectorAll("form.hint")) {
	form.addEventListener('submit', confirm_hint)
}

var answer_zone = document.getElementsByName('answer')[0]
var anwer_value = answer_zone.value;

var send_button = document.querySelector('#send');
var interactive = document.querySelector('#interactive_problem_form');
var form = document.querySelector('#problem_form');

var progress = document.createElement('input');
progress.type = 'hidden';
progress.name = 'progress';

if (form)
	form.appendChild(progress);

function hint_save(){
	if (interactive)
		localStorage.setItem("solution", interactive.outerHTML);
	else
		localStorage.setItem("solution", form.outerHTML)
	localStorage.setItem("answer", document.getElementsByName('answer')[0].value);
}

function save_progress(){
	if (interactive)
		progress.value = interactive.outerHTML;
	else
		progress.value = form.outerHTML;
}

function update_load(){
	var solution = localStorage.getItem('solution');
	var answer = localStorage.getItem('answer');
	if (solution)
	{
		if (interactive)
			interactive.outerHTML = solution;
		else
			form.outerHTML = solution;
		localStorage.removeItem('solution');
	}
	if (answer)
	{
		answer_zone.value = answer;
		localStorage.removeItem('answer');
	}
}

send_button.addEventListener('click', save_progress);

update_load()