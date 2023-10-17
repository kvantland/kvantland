var drag_rooks = document.querySelectorAll('.active');
var sender = document.getElementsByName('answer')[0];
var def_rooks = document.querySelectorAll('.passive');
var all_rooks = document.querySelectorAll('.rook');
var cur_amount_text = document.querySelector('.amount');
var board = document.querySelectorAll('rect');
var side = document.querySelector('rect').getAttribute('width');
var def_X = drag_rooks[0].getAttribute('x');
var def_Y = drag_rooks[0].getAttribute('y');
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
	for (const rook of drag_rooks){
		if (rook.classList.contains('choiced') && rook.classList.contains('active')){
			var x = rook.getAttribute('column');
			var y = rook.getAttribute('row');
			curr.push([y, x]);
		}
	}
	sender.value = [curr[0].join(''), curr[1].join('')].join(' ');
}

function check_if_empty(square){
	for (const rook of all_rooks){
		if (rook.classList.contains('choiced')){
			if (rook.getAttribute('y') == square.getAttribute('y') && rook.getAttribute('x') == square.getAttribute('x'))
				return false;
		}
	}
	return true;
}

function moveAt(x, y){
	a = document.querySelector('.targeted');
	a.setAttribute('x', x);
	a.setAttribute('y', y);
}

function move(event){
	var svg_box_X = svg_box.getBoundingClientRect().left;
	var svg_box_Y = svg_box.getBoundingClientRect().top;
	var cur_X = event.pageX - svg_box_X;
	var cur_Y = event.pageY - svg_box_Y;
	var right = document.documentElement.clientWidth - svg_box_X;
	var bottom = document.documentElement.clientHeight - svg_box_Y;
	var left = -svg_box_X;
	var top = -svg_box_Y;
	if (cur_X + side / 2 < right && cur_X - side / 2 > left && cur_Y - side / 2 > top && cur_Y + side / 2 < bottom)
		moveAt(cur_X - side / 2, cur_Y - side / 2);
	else
		back_to_drag();

}

function update_remained_rooks_amount(){
	cur_amount_text.textContent = remained_rooks_amount()
}

function remained_rooks_amount(){
	let amount = 0;
	for (rook of drag_rooks){
		if (rook.classList.contains('choiced'))
			continue;
		if (rook.classList.contains('targeted'))
			continue;
		amount += 1;
	}
	return amount;
}

function back_to_drag(){
	document.removeEventListener('mousemove', move);
	a = document.querySelector('.targeted');
	a.classList.remove('targeted');
	a.classList.remove('choiced');
	a.setAttribute('x', def_X);
	a.setAttribute('y', def_Y);
	update_remained_rooks_amount();
}

function drop(square){
	document.removeEventListener('mousemove', move);
	a = document.querySelector('.targeted');
	a.classList.remove('targeted');
	a.classList.add('choiced');	
	a.setAttribute('y', square.getAttribute('y'));
	a.setAttribute('x', square.getAttribute('x'));
	update_remained_rooks_amount();
}

for (const rook of drag_rooks){
	rook.onmousedown = function(event){
		this.classList.add('targeted');
		this.classList.remove('choiced');
		update_remained_rooks_amount();
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

rel = document.querySelector('.reload');
rel.onclick = function(){
	for (const rook of drag_rooks){
		rook.classList.remove('choiced');
		rook.setAttribute('x', def_X);
		rook.setAttribute('y', def_Y);
	}
	update_remained_rooks_amount()
}
