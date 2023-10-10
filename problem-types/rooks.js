var rooks = document.querySelectorAll('.rook');
var sender = document.getElementsByName('answer')[0];
var def_rooks = document.getElementsByTagName('image');
var cur_amount_text = document.querySelector('#amount');
var cur_amount = 2;

document.querySelector('button').onclick = function(e){
	var curr = [];
	for (const rook of rooks){
		if (rook.classList.contains('choiced')){
			var x = Math.floor((parseInt(rook.style.left, 10) - 7) / 80);
			var y = Math.floor((parseInt(rook.style.top, 10) - 7) / 80);
			curr.push([y, x]);
		}
	}
	sender.value = [curr[0].join(''), curr[1].join('')].join(' ');
}

function in_def(rook){
	for (const def of def_rooks){
		if (def.getAttribute('x') == rook.getAttribute('x')){
			if (def.getAttribute('y') == rook.getAttribute('y')){
				return true;
			}
		}
	}
	return false;
}

function check(square){
	for (const rook of rooks){
		if (rook.classList.contains('choiced')){
			if (parseInt(rook.style.top, 10) - square.getAttribute('y') == 6 && parseInt(rook.style.left, 10) - square.getAttribute('x') == 6)
				return false;
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
	moveAt(event.pageX, event.pageY);
}

function coord(rook){
	y = (rook.style.top - 1) / 80;
	x = (rook.style.left - 1) / 80;
	return [x, y];
}

for (const rook of document.getElementsByClassName('rook')){
	rook.onmousedown = function(event){
		this.classList.add('targeted');
		if (!this.classList.contains('choiced')){		
			cur_amount_text.innerHTML = (cur_amount - 1);
			cur_amount -= 1;
		}
		this.classList.remove('choiced');
		document.body.append(this);
		moveAt(event.clientX, event.clientY);
		document.addEventListener('mousemove', move)
		this.onmouseup = function(event){
			this.classList.remove('targeted');
			document.removeEventListener('mousemove', move);
			var board = document.getElementsByTagName('rect');
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
			if (min_diff < 80 ** 2 && check(best_square) && !in_def(best_square)){
				board_zone = document.querySelector('.board_zone');
				board_zone.append(this);
				this.style.top = best_square.getAttribute('y') - (-6) + 'px';
				this.style.left = best_square.getAttribute('x') - (-6) + 'px';
				this.classList.add('choiced');
			}
			else{
				used_square = '';
				cur_amount += 1;
				this.classList.remove('choiced');
				drag_zone = document.querySelector('.drag_zone');
				this.style.top = '';
				this.style.left = '';
				drag_zone.append(this);
				cur_amount_text.innerHTML = cur_amount;
			}
		}
	}
}

rel = document.querySelector('.reload');
rel.onclick = function(){
	for (const rook of rooks){
		drag_zone = document.querySelector('.drag_zone');
		rook.style.top = '';
		rook.style.left = '';
		rook.classList.remove('choiced');
		drag_zone.append(rook);
	}
	cur_amount = 2;
	cur_amount_text.innerHTML = cur_amount;
}
