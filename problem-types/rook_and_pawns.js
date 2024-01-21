var free_squares = document.querySelectorAll('.free');
var svg_box = document.querySelector('svg');
var rook = document.querySelector('.rook');
var side = document.querySelector('rect').getAttribute('width');
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

for (const square of free_squares){
	square.addEventListener("click", (e) => choose(e, square))
	square.addEventListener("touchstart", (e) => choose(e, square))
}

function reload(e) {
	if (e.targetTouches)
		e.preventDefault()
	rook.setAttribute('x', def_X);
	rook.setAttribute('y', def_Y);
	rook.setAttribute('column', def_column);
	rook.setAttribute('row', def_row);
	free_board();
}

var rel = document.querySelector('.reload');
rel.addEventListener("click", (e) => reload(e))
rel.addEventListener("touchstart", (e) => reload(e))