var drag_boys = document.querySelectorAll('.active');
var sender = document.getElementsByName('answer')[0];
var def_boys = document.querySelectorAll('.passive');
var all_boys = document.querySelectorAll('.boy');
var cur_amount_text = document.querySelector('.amount');
var board = document.querySelectorAll('rect');
var side = document.querySelector('rect').getAttribute('width');
var cp = [];
for (const boy of drag_boys){
	cp.push([boy.getAttribute('x'), boy.getAttribute('y')]);
}
var def_X = drag_boys[0].getAttribute('x');
var def_Y = drag_boys[0].getAttribute('y');
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

	for (const square of board){
		for (const boy of drag_boys){
			if (boy.classList.contains('choiced') && boy.getAttribute('x') == square.getAttribute('x')){
				if(boy.classList.contains('num_1'))
					curr.push(1);
				if(boy.classList.contains('num_2'))
					curr.push(2);
				if(boy.classList.contains('num_3'))
					curr.push(3);
				if(boy.classList.contains('num_4'))
					curr.push(4);
			}
		}	
	}
	sender.value = curr;
}

function check_if_empty(square){
	for (const boy of all_boys){
		if (boy.classList.contains('choiced')){
			if (boy.getAttribute('y') == square.getAttribute('y') && boy.getAttribute('x') == square.getAttribute('x'))
				return false;
		}
	}
	return true;
}

function moveAt(x, y){
	var a = document.querySelector('.targeted');
	a.setAttribute('x', x);
	a.setAttribute('y', y);
}

function move(event){
	var svg_box_X = svg_box.getBoundingClientRect().left;
	var svg_box_Y = svg_box.getBoundingClientRect().top;
	var cur_X = event.clientX - svg_box_X;
	var cur_Y = event.clientY - svg_box_Y;
	var right = document.documentElement.clientWidth - svg_box_X;
	var bottom = document.documentElement.clientHeight - svg_box_Y;
	var left = -svg_box_X;
	var top = -svg_box_Y;
	if (cur_X + side / 2 < right && cur_X - side / 2 > left && cur_Y - side / 2 > top && cur_Y + side / 2 < bottom)
		moveAt(cur_X - side / 2, cur_Y - side / 2);
	else
		back_to_drag();

}



function back_to_drag(){
	document.removeEventListener('mousemove', move);
	var a = document.querySelector('.targeted');
	if (!a)
		return;
	a.classList.remove('targeted');
	a.classList.remove('choiced');
	if(a.classList.contains('num_1')) {
		a.setAttribute('x', cp[0][0]);
		a.setAttribute('y', cp[0][1]);
	}
	if(a.classList.contains('num_2')) {
		a.setAttribute('x', cp[1][0]);
		a.setAttribute('y', cp[1][1]);
	}
	if(a.classList.contains('num_3')) {
		a.setAttribute('x', cp[2][0]);
		a.setAttribute('y', cp[2][1]);
	}
	if(a.classList.contains('num_4')) {
		a.setAttribute('x', cp[3][0]);
		a.setAttribute('y', cp[3][1]);
	}
}

function drop(square){
	document.removeEventListener('mousemove', move);
	var a = document.querySelector('.targeted');
	if (!a)
		return;
	a.classList.remove('targeted');
	a.classList.add('choiced');	
	a.setAttribute('y', square.getAttribute('y'));
	a.setAttribute('x', square.getAttribute('x'));
}

for (const boy of drag_boys){
	boy.onmousedown = function(event){
		this.classList.add('targeted');
		this.classList.remove('choiced');
		svg_box.appendChild(this);
		var svg_box_X = svg_box.getBoundingClientRect().left;
		var svg_box_Y = svg_box.getBoundingClientRect().top;
		moveAt(event.clientX - svg_box_X - side / 2, event.clientY - svg_box_Y - side / 2);
		document.addEventListener('mousemove', move)
		this.onmouseup = function(event){
			var min_diff = 10 ** 9;
			var best_square = '';
			var best_square_row = 0;
			var best_square_column = 0;
			let row = 0;
			let column = 0;
			for (const square of board){
				let x_diff = square.getAttribute('x') - this.getAttribute('x');
				let y_diff = square.getAttribute('y') - this.getAttribute('y');
				let tot_diff = x_diff ** 2 + y_diff ** 2;
				if (tot_diff < min_diff){
					best_square = square;
					min_diff = tot_diff;
					best_square_row = row;
					best_square_column = column;
				}
				row += 1;
				if (row == in_column){
					row = 0;
					column += 1;
				}
			};
			if (min_diff < side ** 2 && check_if_empty(best_square)){
				this.setAttribute('column', best_square_column);
				this.setAttribute('row', best_square_row);
				drop(best_square);
			}
			else
				back_to_drag();
		}
	}
}

var rel = document.querySelector('.reload');
rel.onclick = function(){
	for (const boy of drag_boys){
		if(boy.classList.contains('num_1')) {
			boy.setAttribute('x', cp[0][0]);
			boy.setAttribute('y', cp[0][1]);
		}
		if(boy.classList.contains('num_2')) {
			boy.setAttribute('x', cp[1][0]);
			boy.setAttribute('y', cp[1][1]);
		}
		if(boy.classList.contains('num_3')) {
			boy.setAttribute('x', cp[2][0]);
			boy.setAttribute('y', cp[2][1]);
		}
		if(boy.classList.contains('num_4')) {
			boy.setAttribute('x', cp[3][0]);
			boy.setAttribute('y', cp[3][1]);
		}
	}
}
