var def_horse = document.querySelector('.horse.passive');
var def_bishop = document.querySelector('.bishop.passive');
var board = document.querySelectorAll('rect');
var side = document.querySelector('rect').getAttribute('width');
var def_X_horse = def_horse.getAttribute('x');
var def_y_horse = def_horse.getAttribute('y');
var def_X_bishop = def_bishop.getAttribute('x');
var def_Y_bishop = def_bishop.getAttribute('y');
var svg_box = document.querySelector('.plot_area');
var width = def_horse.getAttribute('width');
var height = def_horse.getAttribute('height');

document.querySelector('button').onclick = function(e){
	var ans = '';
	for (square of document.querySelectorAll('rect'))
		ans += nearest_figure_type(square);
	document.querySelector("input[name='answer']").value = ans;
}

function nearest_figure_type(square){
	var all_figures = document.querySelectorAll('.active');
	for (const figure of all_figures){
		if (figure.classList.contains('choiced')){
			if (figure.getAttribute('y') == square.getAttribute('y') && figure.getAttribute('x') == square.getAttribute('x'))
			{
				if (figure.classList.contains('horse'))
					return 1;
				else
					return 2;
			}
		}
	}
	return '-';	
}
function check_if_empty(square){
	var all_figures = document.querySelectorAll('.active');
	for (const figure of all_figures){
		if (figure.classList.contains('choiced')){
			if (figure.getAttribute('y') == square.getAttribute('y') && figure.getAttribute('x') == square.getAttribute('x'))
				figure.parentNode.removeChild(figure);
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

function add_figure(type)	{
	var svgNS = "http://www.w3.org/2000/svg"
	var new_figure = document.createElementNS(svgNS, 'image');
	if (type == 'bishop'){
		new_figure.classList.add('bishop');
		new_figure.setAttribute('x', def_X_bishop);
		new_figure.setAttribute('y', def_Y_bishop);
		new_figure.setAttribute('href', '/static/bishop.png');
	}
	else{
		new_figure.classList.add('horse');
		new_figure.setAttribute('x', def_X_horse);
		new_figure.setAttribute('y', def_y_horse);
		new_figure.setAttribute('href', '/static/horse.png');
	}
	new_figure.setAttribute('width', width);
	new_figure.setAttribute('height', height);
	new_figure.classList.add('active');
	svg_box.appendChild(new_figure);
}

document.addEventListener('DOMContentLoaded', update_figures());

function update_figures()
{
	var drag_figures = document.querySelectorAll('.active');
	for (const figure of drag_figures){
		figure.onmousedown = function(event){
			if (!this.classList.contains('choiced')){
				if (this.classList.contains('horse') )
					add_figure('horse');
				else
					add_figure('bishop');
			}
			this.classList.add('targeted');
			this.classList.remove('choiced');
			svg_box.appendChild(this);
			var svg_box_X = svg_box.getBoundingClientRect().left;
			var svg_box_Y = svg_box.getBoundingClientRect().top;
			moveAt(event.clientX - svg_box_X - side / 2, event.clientY - svg_box_Y - side / 2);
			document.addEventListener('mousemove', move)
			update_figures();
		}
		figure.onmouseup = function(event){
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
			update_figures();
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
	update_figures();
}
