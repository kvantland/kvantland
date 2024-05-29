var allowed_drag_horse = document.querySelector('.allowed.active');
var rejected_drag_horse = document.querySelector('.rejected.active');
var board = document.querySelectorAll('rect');
var side = document.querySelector('rect').getAttribute('width');
var def_X_allowed = allowed_drag_horse.getAttribute('x');
var def_Y_allowed = allowed_drag_horse.getAttribute('y');
var def_X_rejected = rejected_drag_horse.getAttribute('x');
var def_Y_rejected = rejected_drag_horse.getAttribute('y');
var svg_box = document.querySelector('.plot_area');
var width = allowed_drag_horse.getAttribute('width');
var height = allowed_drag_horse.getAttribute('height');

const row_set = new Set();
const column_set = new Set()

for (square of board){
	row_set.add(square.getAttribute('x'))
	column_set.add(square.getAttribute('y'))
}

var in_row = row_set.size;
var in_column = column_set.size;

function check_if_empty(square){
	var all_horses = document.querySelectorAll('.horse');
	if (square.classList.contains('occupied'))
		return false;
	for (const horse of all_horses){
		if (horse.classList.contains('choiced')){
			if (horse.getAttribute('y') == square.getAttribute('y') && horse.getAttribute('x') == square.getAttribute('x'))
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
	a.parentNode.removeChild(a);
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

function add_horse(type)	{
	var svgNS = "http://www.w3.org/2000/svg"
	var new_horse = document.createElementNS(svgNS, 'image');
	if (type == 'rejected'){
		new_horse.classList.add('rejected');
		new_horse.setAttribute('x', def_X_rejected);
		new_horse.setAttribute('y', def_Y_rejected);
		new_horse.setAttribute('href', '/static/rejected_horse.png');
	}
	else{
		new_horse.classList.add('allowed');
		new_horse.setAttribute('x', def_X_allowed);
		new_horse.setAttribute('y', def_Y_allowed);
		new_horse.setAttribute('href', '/static/horse.png');
	}
	new_horse.setAttribute('width', width);
	new_horse.setAttribute('height', height);
	new_horse.classList.add('horse');
	new_horse.classList.add('active');
	svg_box.appendChild(new_horse);
}

document.addEventListener('DOMContentLoaded', update_horse());

function update_horse()
{
	var drag_horses = document.querySelectorAll('.active');
	for (const horse of drag_horses){
		horse.onmousedown = function(event){
			if (!this.classList.contains('choiced')){
				if (this.classList.contains('allowed') )
					add_horse('allowed');
				else
					add_horse('rejected');
			}
			this.classList.add('targeted');
			this.classList.remove('choiced');
			svg_box.appendChild(this);
			var svg_box_X = svg_box.getBoundingClientRect().left;
			var svg_box_Y = svg_box.getBoundingClientRect().top;
			moveAt(event.clientX - svg_box_X - side / 2, event.clientY - svg_box_Y - side / 2);
			document.addEventListener('mousemove', move)
			update_horse();
		}
		horse.onmouseup = function(event){
			var min_diff = 10 ** 9;
			var best_square = '';
			for (const square of board){
				let x_diff = square.getAttribute('x') - this.getAttribute('x');
				let y_diff = square.getAttribute('y') - this.getAttribute('y');
				let tot_diff = x_diff ** 2 + y_diff ** 2;
				if (tot_diff < min_diff){
					best_square = square;
					min_diff = tot_diff;
				}
			};
			if (min_diff < side ** 2 && check_if_empty(best_square))
				drop(best_square);
			else
				back_to_drag();
			update_horse();
		}
	}
}

var rel = document.querySelector('.reload');
rel.onclick = function(){
	var drag_horses = document.querySelectorAll('.active.choiced');
	for (var horse of drag_horses){
		horse.classList.remove('choiced');
		horse.parentNode.removeChild(horse);
	}
	update_horse();
}
