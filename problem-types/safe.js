var buttons = document.querySelectorAll('.active');
var svg_box = document.querySelector('svg');
var all_square = document.querySelectorAll('rect');
var unknowns = document.querySelectorAll('.unknown');
var sender = document.getElementsByName('answer')[0];

document.querySelector('button').onclick = function(e){
	var curr = "";
	for (const u of unknowns) {
		curr += u.innerHTML;
	}
	sender.value = curr;
}

for (const button of buttons){
	button.onclick = function(){
		if (button.classList.contains('top')) {
			for (const u of unknowns) {
				if (button.getAttribute('column') == u.getAttribute('column')) {
					if (u.innerHTML == '*')
						u.innerHTML = '0';
					else {
						u.innerHTML = (u.innerHTML - -1) % 10;
					}
				}
			}
		} else {
			for (const u of unknowns) {
				if (button.getAttribute('column') == u.getAttribute('column')) {
					if (u.innerHTML == '*')
						u.innerHTML = '0';
					else {
						u.innerHTML = (u.innerHTML - -9) % 10;
					}
				}
			}
		}
	}
}

document.querySelector('.reload').onclick = function(){
	for (const u of unknowns){
		u.innerHTML = '*';
	}
}

document.querySelector('.check ').onclick = function(){
	let url = new URL(window.location.href + 'xhr')
	let ans = ''
	for (const u of unknowns) {
		ans += u.innerHTML;
	}
	let solution = document.querySelector('#interactive_problem_form').outerHTML
	let xhr = new XMLHttpRequest()
	xhr.open('POST', url)
	xhr.responseType = 'text'
	xhr.send(JSON.stringify({'answer': ans, 'solution': solution}));
	xhr.onload = function() {
		if (xhr.status != 200)
			alert(`Ошибка ${xhr.status}: ${xhr.statusText}`)
		else
		{
			if (xhr.response == 'no_tries')
				alert('Больше нельзя делать проверок!')
			else
				{
					if (xhr.response == 'false')
						alert('Неверная комбинация!')
					else
						alert('Верная комбинация!')
					let text = document.querySelector('.remaining_checks p').innerHTML.split(': ')[0]
					let cur_amount = document.querySelector('.remaining_checks p').innerHTML.split(': ')[1]
					document.querySelector('.remaining_checks p').innerHTML = text + ': ' + (cur_amount - 1)
					if (xhr.response == 'true' || !cur_amount)
						window.location.reload('true')
				}
		}
	}
}