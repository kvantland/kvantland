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
						u.innerHTML = String(((parseInt(u.innerHTML) + 1) % 10 + 10) % 10);
					}
				}
			}
		} else {
			for (const u of unknowns) {
				if (button.getAttribute('column') == u.getAttribute('column')) {
					if (u.innerHTML == '*')
						u.innerHTML = '0';
					else {
						u.innerHTML = String(((parseInt(u.innerHTML) - 1) % 10 + 10) % 10);
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
	var conf = ''
	for (const u of unknowns) {
		conf += u.innerHTML;
	}
	var sol = conf;
	url.searchParams.set('conf', [conf])
	url.searchParams.set('sol', [sol])
	let xhr = new XMLHttpRequest()
	xhr.open('GET', url)
	xhr.responseType = 'text'
	xhr.send();
	xhr.onload = function() {
		if (xhr.status != 200)
			alert(`Ошибка ${xhr.status}: ${xhr.statusText}`)
		else
		{
			if (xhr.response == 'no_tries' || xhr.response == 'true')
				window.location.reload("true")
			else
			{
				let [text, amount] = document.querySelector('.remaining_checks p').innerHTML.split(':')
				document.querySelector('.remaining_checks p').innerHTML = text + ': ' + (amount - 1)
				sender.value = conf
			}
		}
	}
}