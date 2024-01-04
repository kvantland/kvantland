var free_squares = document.querySelectorAll('.free');
var svg_box = document.querySelector('svg');
var rook = document.querySelector('.rook');
var side = document.querySelector('rect').getAttribute('width');
var all_square = document.querySelectorAll('rect');
var def_X = rook.getAttribute('x');
var def_Y = rook.getAttribute('y');
var def_column = rook.getAttribute('column');
var def_row = rook.getAttribute('row');
var sender = document.getElementsByName('answer')[0];

document.querySelector('button').onclick = function(e){
	sender.value = [rook.getAttribute('column'), rook.getAttribute('row')]
}

for (const square of free_squares){
	square.onclick = function(){
		if (rook.classList.contains('free')){
			this.classList.remove('free')
			this.classList.add('choiced')
		}
		rook.setAttribute('x', this.getAttribute('x'));
		rook.setAttribute('y', this.getAttribute('y'));
		rook.setAttribute('column', this.getAttribute('column'));
		rook.setAttribute('row', this.getAttribute('row'));
	}
}

var rel = document.querySelector('.reload');
rel.onclick = function(){
	rook.classList.remove('choiced');
	rook.classList.add('free');
	rook.setAttribute('x', def_X);
	rook.setAttribute('y', def_Y);
	rook.setAttribute('column', def_column);
	rook.setAttribute('row', def_row);
}