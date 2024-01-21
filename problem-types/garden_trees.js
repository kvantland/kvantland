var drag_tree = document.querySelector('.active');
var board = document.querySelectorAll('rect');
var side = document.querySelector('rect').getAttribute('width');
var def_X = drag_tree.getAttribute('x');
var def_Y = drag_tree.getAttribute('y');
var svg_box = document.querySelector('.plot_area');
var width = drag_tree.getAttribute('width');
var height = drag_tree.getAttribute('height');
var sender = document.getElementsByName('answer')[0];

const row_set = new Set();
const column_set = new Set()

for (square of board){
	row_set.add(square.getAttribute('x'))
	column_set.add(square.getAttribute('y'))
}

var in_row = row_set.size;
var in_column = column_set.size;

document.querySelector('button').onclick = function(e){
	var ans = '';
	for (const square of board){
		ans += get_amount(square) + ','
	}
	sender.value = ans;
}

function get_amount(square){
	var all_trees = document.querySelectorAll('.tree');
	for (const tree of all_trees){
		if (tree.classList.contains('choiced')){
			if (tree.getAttribute('y') == square.getAttribute('y') && tree.getAttribute('x') == square.getAttribute('x'))
			{
				var amount = tree.getAttribute('amount');
				return amount
			}
		}
	}
	return 0;
}

function get_square(tree){
	for (const square of board)
		if (tree.getAttribute('y') == square.getAttribute('y') && tree.getAttribute('x') == square.getAttribute('x'))
			return square
}

function increase_tree_amount(square, amount){
	var all_trees = document.querySelectorAll('.tree');
	for (const tree of all_trees){
		if (tree.classList.contains('choiced')){
			if (tree.getAttribute('y') == square.getAttribute('y') && tree.getAttribute('x') == square.getAttribute('x'))
			{
				tree.setAttribute('amount', Math.max(1, (tree.getAttribute('amount') - (-amount)) % 5));
				tree.setAttribute('href', `/static/${tree.getAttribute('amount')}_tree.png`);
				return;
			}
		}
	}
}

function reduce_tree_amount(square, amount){
	var all_trees = document.querySelectorAll('.tree');
	for (const tree of all_trees)
		if (tree.classList.contains('choiced'))
			if (tree.getAttribute('y') == square.getAttribute('y') && tree.getAttribute('x') == square.getAttribute('x'))
				add_tree(tree.getAttribute('x'), tree.getAttribute('y'), tree.getAttribute('amount') - amount, choiced=true);
}

function moveAt(x, y){
	a = document.querySelector('.targeted');
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
	let add = 40
	let [x_diff, y_diff] = [0, 0]
	let [bott, right] = [document.documentElement.clientHeight, document.documentElement.clientWidth]
	if (x < add)
		x_diff = x - add
	if (y < add)
		y_diff = y - add
	if (y > bott - add)
		y_diff = y - bott + add
	if (x > right - add)
		x_diff = x - right + add
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
	autoscroll(cur_X, cur_Y)
	if (screen_border_check(cur_X, cur_Y))
		moveAt(cur_X - svg_box_X - side / 2, cur_Y - svg_box_Y - side / 2)
	else
		back_to_drag()
}

function back_to_drag(){
	document.removeEventListener("mousemove", move);
	document.removeEventListener("touchmove", move);
	a = document.querySelector('.targeted');
	a.parentNode.removeChild(a);
}

function drop(square){
	document.removeEventListener("mousemove", move);
	document.removeEventListener("touchmove", move);
	a = document.querySelector('.targeted');
	a.classList.remove('targeted');
	a.classList.add('choiced');	
    a.setAttribute('y', square.getAttribute('y'));
    a.setAttribute('x', square.getAttribute('x'));
}

function setAttributes(el, attrs) {
  for(var key in attrs) {
    el.setAttribute(key, attrs[key]);
  }
}

function add_tree(x, y, amount=false, choiced=false){
	svgNS = "http://www.w3.org/2000/svg"
	var new_tree = document.createElementNS(svgNS, 'image');
	if (!amount)
		setAttributes(new_tree, {'amount':'1', 'x':`${x}`, 'y':`${y}`, 'href':'/static/tree.png', 'width':`${width}`, 'height':`${height}`})
	else
		setAttributes(new_tree, {'amount':`${amount}`, 'x':`${x}`, 'y':`${y}`, 'href':`/static/${amount}_tree.png`, 'width':`${width}`, 'height':`${height}`});
	new_tree.classList.add('tree', 'active');
	if (choiced)
		new_tree.classList.add('choiced');
	svg_box.appendChild(new_tree);
}

document.addEventListener('DOMContentLoaded', update_tree());

function start(event, obj) {
	if (!obj.classList.contains('choiced'))
		add_tree(def_X, def_Y)
	else
	{
		if (obj.getAttribute('amount') > 1)
			reduce_tree_amount(get_square(obj), 1)
		obj.setAttribute('amount', '1')
		obj.setAttribute('href', '/static/tree.png')
	}
	obj.classList.add('targeted');
	obj.classList.remove('choiced');
	svg_box.appendChild(obj);
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
	var svg_box_X = svg_box.getBoundingClientRect().left;
	var svg_box_Y = svg_box.getBoundingClientRect().top;
	moveAt(posX - svg_box_X - side / 2, posY - svg_box_Y - side / 2);
	document.addEventListener("mousemove", move)
	document.addEventListener("touchmove", move)
	update_tree();
}

function end(event, obj) {
	if (!document.querySelector('.targeted'))
		return 
	var min_diff = 10 ** 9;
	var best_square = '';
	for (const square of board){
		let x_diff = square.getAttribute('x') - obj.getAttribute('x');
		let y_diff = square.getAttribute('y') - obj.getAttribute('y');
		let tot_diff = x_diff ** 2 + y_diff ** 2;
		if (tot_diff < min_diff){
			best_square = square;
			min_diff = tot_diff;
		}
	};
	if (min_diff < side ** 2)
	{
		if (get_amount(best_square) == '0')
		{
			if (obj.getAttribute('href') == '/static/tree.png')
				obj.setAttribute('href', '/static/1_tree.png');
			drop(best_square);
		}
		else
		{
			increase_tree_amount(best_square, obj.getAttribute('amount'));
			back_to_drag();
		}
	}
	else
		back_to_drag();
	update_tree();
}

function update_tree()
{
	var drag_trees = document.querySelectorAll('.active');
	for (const tree of drag_trees){
		tree.addEventListener("mousedown", (e) => start(e, tree))
		tree.addEventListener("touchstart", (e) => start(e, tree))
		tree.addEventListener("mouseup", (e) => end(e, tree))
		tree.addEventListener("touchend", (e) => end(e, tree))
	}
}

rel = document.querySelector('.reload');
rel.onclick = function(){
	var drag_trees = document.querySelectorAll('.active.choiced');
	for (var tree of drag_trees){
		tree.classList.remove('choiced');
		tree.parentNode.removeChild(tree);
	}
	update_tree();
}
