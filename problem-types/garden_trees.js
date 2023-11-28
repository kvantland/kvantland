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
	a = document.querySelector('.targeted');
	a.parentNode.removeChild(a);
}

function drop(square){
	document.removeEventListener('mousemove', move);
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

function update_tree()
{
	var drag_trees = document.querySelectorAll('.active');
	for (const tree of drag_trees){
		tree.onmousedown = function(event){
			if (!this.classList.contains('choiced'))
				add_tree(def_X, def_Y)
			else
			{
				if (this.getAttribute('amount') > 1)
					reduce_tree_amount(get_square(this), 1)
				this.setAttribute('amount', '1')
				this.setAttribute('href', '/static/tree.png')
			}
			this.classList.add('targeted');
			this.classList.remove('choiced');
			svg_box.appendChild(this);
			var svg_box_X = svg_box.getBoundingClientRect().left;
			var svg_box_Y = svg_box.getBoundingClientRect().top;
			moveAt(event.clientX - svg_box_X - side / 2, event.clientY - svg_box_Y - side / 2);
			document.addEventListener('mousemove', move)
			update_tree();
		}
		tree.onmouseup = function(event){
			if (!document.querySelector('.targeted'))
				return 
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
			if (min_diff < side ** 2)
			{
				if (get_amount(best_square) == '0')
				{
					if (this.getAttribute('href') == '/static/tree.png')
						this.setAttribute('href', '/static/1_tree.png');
					drop(best_square);
				}
				else
				{
					increase_tree_amount(best_square, this.getAttribute('amount'));
					back_to_drag();
				}
			}
			else
				back_to_drag();
			update_tree();
		}
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
