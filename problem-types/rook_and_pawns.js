var free_squares = document.querySelectorAll('.free');
var clear_squares = document.querySelectorAll('.clear');
var svg_box = document.querySelector('svg');
var rook = document.querySelector('.rook');
var side = document.querySelector('rect').getAttribute('width');
var width = svg_box.getAttribute('width');
var def_X = rook.getAttribute('x');
var def_Y = rook.getAttribute('y');
var def_column = rook.getAttribute('column');
var def_row = rook.getAttribute('row');
var sender = document.getElementsByName('answer')[0];

function send(e) {
	sender.value = [rook.getAttribute('column'), rook.getAttribute('row')]
}

document.querySelector('button').addEventListener("click", (e) => send(e))
document.querySelector('button').addEventListener("touchstart", (e) => send(e))

function free_board(){
	for (var square of free_squares)
	{
		if (square.classList.contains('choiced'))
		{
			square.classList.remove('choiced');
			square.classList.add('free');
		}
	}
}

function clear_board(){
	for (var square of clear_squares)
	{
		square.classList.remove('unclear')
		square.classList.add('clear')
	}
	for (const tick of document.querySelectorAll('.cross'))
	{
		tick.parentNode.removeChild(tick);
	}
}

function choose(e, obj) {
	if (e.targetTouches)
		e.preventDefault()
	free_board();
	obj.classList.remove('free');
	obj.classList.add('choiced');
	rook.setAttribute('x', obj.getAttribute('x'));
	rook.setAttribute('y', obj.getAttribute('y'));
	rook.setAttribute('column', obj.getAttribute('column'));
	rook.setAttribute('row', obj.getAttribute('row'));
}

function attempt(e, obj) {
	if (e.targetTouches)
		e.preventDefault()
	if (obj.classList.contains('clear')) {
		obj.classList.remove('clear');
		obj.classList.add('unclear');
		svgNS = "http://www.w3.org/2000/svg"
		var cross = document.createElementNS(svgNS, 'text');
		cross.innerHTML = '&#x274C;';
		cross.setAttribute('x', obj.getAttribute('x') - -(side / 2));
		cross.setAttribute('y', obj.getAttribute('y') - -(side / 2));
		cross.setAttribute('column', obj.getAttribute('column'));
		cross.setAttribute('row', obj.getAttribute('row'));
		cross.classList.add('cross');
		svg_box.appendChild(cross);
	}
	else {
		obj.classList.remove('unclear');
		obj.classList.add('clear');
		for (const tick of document.querySelectorAll('.cross')){
			if (tick.getAttribute('column') == obj.getAttribute('column') && tick.getAttribute('row') == obj.getAttribute('row')){
				tick.parentNode.removeChild(tick);
				break;
			}
		}
	}
	
}

for (const square of free_squares){
	square.addEventListener("click", (e) => choose(e, square))
	square.addEventListener("touchstart", (e) => choose(e, square))
}

for (const square of clear_squares){
	square.addEventListener("click", (e) => attempt(e, square))
	square.addEventListener("touchstart", (e) => attempt(e, square))
}

function reload(e) {
	if (e.targetTouches)
		e.preventDefault()
	rook.setAttribute('x', def_X);
	rook.setAttribute('y', def_Y);
	rook.setAttribute('column', def_column);
	rook.setAttribute('row', def_row);
	free_board();
	clear_board();
}

var rel = document.querySelector('.reload');
rel.addEventListener("click", (e) => reload(e))
rel.addEventListener("touchstart", (e) => reload(e))