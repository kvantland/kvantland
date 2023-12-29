var free_squares = document.querySelectorAll('.square');
var sender = document.getElementsByName('answer')[0];
var board = document.querySelectorAll('rect');
var side = document.querySelector('rect').getAttribute('width');
var svg_box = document.querySelector('.plot_area');

const row_set = new Set();
const column_set = new Set()

for (square of board){
	row_set.add(square.getAttribute('x'))
	column_set.add(square.getAttribute('y'))
}

var in_row = row_set.size;
var in_column = column_set.size;

document.querySelector('button').onclick = function(e){
	var curr = [];
	for (const square of free_squares){
		if (square.classList.contains('choiced')){
			var x = square.getAttribute('column');
			var y = square.getAttribute('row');
			curr.push([x, y]);
		}
	}
	sender.value = curr;
}

for (const square of free_squares){
	square.onclick = function(){
		if (this.classList.contains('free')) {
			this.classList.remove('free')
			this.classList.add('choiced')
		} else {
			this.classList.remove('choiced')
			this.classList.add('free')
		}
		
	}
}