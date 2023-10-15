var drag_rooks = document.querySelectorAll('.rook');
var sender = document.getElementsByName('answer')[0];
var def_rooks = document.getElementsByTagName('image');
var cur_amount_text = document.querySelector('#amount');
var drag_zone = document.querySelector('.drag_zone');
var board_zone = document.querySelector('.board_zone');
var board = document.getElementsByTagName('rect');
var side = document.querySelector('rect').getAttribute('width');
var line_width = document.querySelector('line').getAttribute('width');

document.querySelector('button').onclick = function(e){
	var curr = [];
	for (const rook of drag_rooks){
		if (rook.classList.contains('choiced')){
			var x = Math.floor((parseInt(rook.style.left, 10) - line_width) / side);
			var y = Math.floor((parseInt(rook.style.top, 10) - line_width) / side);
			curr.push([y, x]);
		}
	}
	sender.value = [curr[0].join(''), curr[1].join('')].join(' ');
}

function check_if_empty(square){
	for (const rook of drag_rooks){
		if (rook.classList.contains('choiced')){
			if (parseInt(rook.style.top, 10) == square.getAttribute('y') && parseInt(rook.style.left, 10) == square.getAttribute('x'))
				return false;
		}
	}
	for (const rook of def_rooks){
		if (rook.getAttribute('x') == square.getAttribute('x')){
			if (rook.getAttribute('y') == square.getAttribute('y')){
				return false;
			}
		}
	}
	return true;
}

function moveAt(x, y){
	a = document.querySelector('.targeted');
	a.style.left = x - a.offsetWidth / 2 + 'px';
	a.style.top = y - a.offsetHeight / 2 + 'px';
}

function move(event){
	width = document.documentElement.clientWidth;
	height = document.documentElement.clientHeight;
	if (event.pageX + side / 2 < width && event.pageY + side / 2 < height && event.pageX > side / 2 && event.pageY > side / 2)
		moveAt(event.pageX, event.pageY);
	else
		back_to_drag();

}

function update_remained_rooks_amount(){
	cur_amount_text.innerHTML = remained_rooks_amount()
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
	drag_zone = document.querySelector('.drag_zone');
	a.style.top = '';
	a.style.left = '';
	drag_zone.append(a);
	update_remained_rooks_amount();
}

function drop(square){
	document.removeEventListener('mousemove', move);
	a = document.querySelector('.targeted');
	a.classList.remove('targeted');
	a.classList.add('choiced');	
	a.style.top = square.getAttribute('y')  + 'px';
	a.style.left = square.getAttribute('x') + 'px';
	board_zone.append(a);
	update_remained_rooks_amount();
}

for (const rook of drag_rooks){
	rook.onmousedown = function(event){
		this.classList.add('targeted');
		this.classList.remove('choiced');
		cur_amount_text.innerHTML = remained_rooks_amount();
		document.body.append(this);
		moveAt(event.clientX, event.clientY);
		document.addEventListener('mousemove', move)
		this.onmouseup = function(event){
			var min_diff = 10 ** 9;
			var best_square = '';
			for (const square of board){
				let x_diff = square.getBoundingClientRect().left - this.getBoundingClientRect().left;
				let y_diff = square.getBoundingClientRect().top - this.getBoundingClientRect().top;
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
		}
	}
}

rel = document.querySelector('.reload');
rel.onclick = function(){
	for (const rook of drag_rooks){
		drag_zone = document.querySelector('.drag_zone');
		rook.style.top = '';
		rook.style.left = '';
		rook.classList.remove('choiced');
		drag_zone.append(rook);
	}
	cur_amount_text.innerHTML = remained_rooks_amount();
}
