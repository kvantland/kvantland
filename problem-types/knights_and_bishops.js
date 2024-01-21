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

function screen_border_check(x, y) {
	let [right, f_right] = [document.documentElement.clientWidth, document.documentElement.scrollWidth]
	let [bott, f_bott] = [document.documentElement.clientHeight, document.documentElement.scrollHeight]
	if (x >= right && window.scrollX >= f_right - right)
		return false
	if (x <= 0 && window.scrollX <= 0)
		return false
	if (y <= 0 && window.scrollY <= 0)
		return false
	if (y >= bott && window.scrollY >= f_bott - bott)
		return false
	return true
}

function autoscroll(x, y) {
	let [x_diff, y_diff] = [0, 0]
	let [bott, right] = [document.documentElement.clientHeight, document.documentElement.clientWidth]
	if (x < 0)
		x_diff = x
	if (y < 0)
		y_diff = y
	if (y > bott)
		y_diff = y - bott
	if (x > right)
		x_diff = x - right
	scrollBy(x_diff, y_diff)
}

function move(event) {
	let svg_box_X = svg_box.getBoundingClientRect().left;
	let svg_box_Y = svg_box.getBoundingClientRect().top;
	let cur_X, cur_Y
	if (event.targetTouches) {
		cur_X = event.targetTouches[0].clientX
		cur_Y = event.targetTouches[0].clientY
		event.preventDefault()
	}
	else {
		cur_X = event.clientX
		cur_Y = event.clientY
	}
	if (screen_border_check(cur_X, cur_Y)) {
		autoscroll(cur_X, cur_Y)
		moveAt(cur_X - svg_box_X - side / 2, cur_Y - svg_box_Y - side / 2)
	}
	else
		back_to_drag()
}

function back_to_drag(){
	document.removeEventListener("mousemove", move);
	document.removeEventListener("touchmove", move);
	var a = document.querySelector('.targeted');
	if (!a)
		return;
	a.parentNode.removeChild(a);
}

function drop(square){
	document.removeEventListener("mousemove", move);
	document.removeEventListener("touchmove", move);
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
		new_figure.setAttribute('href', '/static/chess/bishop_w.png');
	}
	else{
		new_figure.classList.add('horse');
		new_figure.setAttribute('x', def_X_horse);
		new_figure.setAttribute('y', def_y_horse);
		new_figure.setAttribute('href', '/static/chess/horse_b.png');
	}
	new_figure.setAttribute('width', width);
	new_figure.setAttribute('height', height);
	new_figure.classList.add('active');
	svg_box.appendChild(new_figure);
}

document.addEventListener('DOMContentLoaded', update_figures());

function start(event, obj) {
	if (!obj.classList.contains('choiced')){
		if (obj.classList.contains('horse') )
			add_figure('horse');
		else
			add_figure('bishop');
	}
	obj.classList.add('targeted');
	obj.classList.remove('choiced');
	svg_box.appendChild(obj);
	var svg_box_X = svg_box.getBoundingClientRect().left;
	var svg_box_Y = svg_box.getBoundingClientRect().top;
	let posX, posY
	if ((event.clientX) && (event.clientY))
	{
		posX = event.clientX
		posY = event.clientY
	}
	else if (event.targetTouches) {
		posX = event.targetTouches[0].clientX
		posY = event.targetTouches[0].clientY
		event.preventDefault()
	}
	moveAt(posX - svg_box_X - side / 2, posY - svg_box_Y - side / 2);
	document.addEventListener("mousemove", move);
	document.addEventListener("touchmove", move);
	update_figures();
}

function end(event, obj) {
	if (!document.querySelector('.targeted'))
		return;
	let min_diff = 10 ** 9;
	let best_square = '';
	for (const square of board){
		let x_diff = square.getAttribute('x') - obj.getAttribute('x');
		let y_diff = square.getAttribute('y') - obj.getAttribute('y');
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

function update_figures()
{
	var drag_figures = document.querySelectorAll('.active');
	for (const figure of drag_figures){
		figure.addEventListener("mousedown", (e) => {start(e, figure)})
		figure.addEventListener("touchstart", (e) => {start(e, figure)})
		figure.addEventListener("mouseup", (e) => {end(e, figure)}) 
		figure.addEventListener("touchend", (e) => {end(e, figure)})
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
