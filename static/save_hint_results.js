function update_load(){
	var form = document.querySelector('#problem_form');
	var interactive = document.querySelector('#interactive_problem_form');
	var solution = localStorage.getItem('solution');
	var answer = localStorage.getItem('answer');
	if (solution)
	{
		if (interactive)
			interactive.outerHTML = solution;
		else
			form.outerHTML = solution;
	}
	if (answer)
		document.querySelector("input[name='answer']").value = answer;
	if (localStorage.length > 0)
	{
		var problem_scripts = document.querySelectorAll("script");
		for (let script of problem_scripts)
			eval(script.innerHTML);
		localStorage.clear();
	}
}

document.addEventListener("DOMContentLoaded", update_load())