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

var rel = document.querySelector('.reload');
rel.onclick = function(){
	for (const u of unknowns){
		u.innerHTML = '*';
	}
}