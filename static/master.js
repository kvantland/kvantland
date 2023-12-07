window.confirm_answer = confirm_answer// HACK make it available to non-modules, for a reason you’d better not think of

function confirm_answer(ev) {
	if (!confirm('Готовы отправить ответ? Передумать будет нельзя!'))
		ev.preventDefault()
	else
		save_progress()
}

function confirm_hint(ev) {
	if (!confirm('Вы точно хотите получить подсказку? Её стоимость 1 квантик.'))
		ev.preventDefault()
	else
		hint_save()
}

for (let form of document.querySelectorAll("form.problem"))
	form.onsubmit = function(e){confirm_answer(e)}

for (let form of document.querySelectorAll("form.hint"))
	form.onsubmit = function(e){confirm_hint(e)}

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

