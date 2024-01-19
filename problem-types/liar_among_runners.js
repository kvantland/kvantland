var drag_boys = document.querySelectorAll('.active');
var sender = document.getElementsByName('answer')[0];
var all_boys = document.querySelectorAll('.boy');
var cur_amount_text = document.querySelector('.amount');
var board = document.querySelectorAll('.top');
var side = document.querySelector('rect').getAttribute('width');
var cp = [];
for (const boy of drag_boys){
	cp.push([boy.getAttribute('x'), boy.getAttribute('y')]);
}
var def_X = drag_boys[0].getAttribute('x');
var def_Y = drag_boys[0].getAttribute('y');
var svg_box = document.querySelector('.plot_area');

const column_set = new Set()

for (square of board){
	column_set.add(square.getAttribute('y'))
}

var in_column = column_set.size;

document.querySelector('button').onclick = function(e){
	var curr = [];

	for (const square of board){
		for (const boy of drag_boys){
			if (boy.classList.contains('choiced') && boy.getAttribute('x') == square.getAttribute('x')){
				curr.push(boy.getAttribute('num'));
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
	document.removeEventListener("mousemove", move);
	document.removeEventListener("touchmove", move);
	var a = document.querySelector('.targeted');
	if (!a)
		return;
	a.classList.remove('targeted');
	a.classList.remove('choiced');
	var num = parseInt(a.getAttribute('num')) - 1
	a.setAttribute('x', cp[num][0]);
	a.setAttribute('y', cp[num][1]);
}

function drop(square){
	document.removeEventListener("mousemove", move);
	document.removeEventListener("touchmove", move);
	var a = document.querySelector('.targeted');
	if (!a)
		return;
	a.classList.remove('targeted');
	a.classList.add('choiced');
	if (square.getAttribute('num') != "*") {
		var num = parseInt(square.getAttribute('num')) - 1
		var b = drag_boys[num]
		b.setAttribute('x', cp[num][0]);
		b.setAttribute('y', cp[num][1]);
		b.classList.remove('choiced')
	}
	a.setAttribute('y', square.getAttribute('y'));
	a.setAttribute('x', square.getAttribute('x'));
	square.setAttribute('num', a.getAttribute('num'))
}

function start(event, obj) {
	obj.classList.add('targeted');
	obj.classList.remove('choiced');
	for (const square of board) {
		if (square.getAttribute('num') == obj.getAttribute('num')){
			square.setAttribute('num', "*")
		}
	}
	svg_box.appendChild(obj);
	var svg_box_X = svg_box.getBoundingClientRect().left;
	var svg_box_Y = svg_box.getBoundingClientRect().top;
	moveAt(event.clientX - svg_box_X - side / 2, event.clientY - svg_box_Y - side / 2);
	document.addEventListener("mousemove", move)
	document.addEventListener("touchmove", move)
}

function end(event, obj) {
	var min_diff = 10 ** 9;
	var best_square = '';
	var best_square_row = 0;
	var best_square_column = 0;
	let row = 0;
	let column = 0;
	for (const square of board){
		let x_diff = square.getAttribute('x') - obj.getAttribute('x');
		let y_diff = square.getAttribute('y') - obj.getAttribute('y');
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
	if (min_diff < side ** 2){
		obj.setAttribute('column', best_square_column);
		obj.setAttribute('row', best_square_row);
		drop(best_square);
	}
	else
		back_to_drag();
}

for (const boy of drag_boys){
	boy.addEventListener("mousedown", (e) => start(e, boy))
	boy.addEventListener("touchstart",  (e) => start(e, boy))
	boy.addEventListener("mouseup", (e) => end(e, boy))
	boy.addEventListener("touchend", (e) => end(e, boy))
}

var rel = document.querySelector('.reload');
rel.onclick = function(){
	for (const a of drag_boys){
		var num = parseInt(a.getAttribute('num')) - 1
		a.setAttribute('x', cp[num][0]);
		a.setAttribute('y', cp[num][1]);
	}
	for (const b of board){
		b.setAttribute('num', '*');
	}
}
