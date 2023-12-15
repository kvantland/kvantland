var free_squares = document.querySelectorAll('.free');
var svg_box = document.querySelector('svg');
var side = document.querySelector('rect').getAttribute('width');
var all_square = document.querySelectorAll('rect');
var sender = document.getElementsByName('answer')[0];

document.querySelector('button').onclick = function(e){
	var i = 0;
	for (const square of all_square){
		if (square.classList.contains('choiced'))
		{
			sender.value = i;
			break;
		}
		i += 1
	}
}

function free_board(){
	for (var square of all_square)
	{
		if (square.classList.contains('choiced'))
		{
			square.classList.remove('occupied', 'choiced');
			square.classList.add('free');
		}
	}
}

for (const square of free_squares){
	square.onclick = function(){
		free_board()
		this.classList.remove('free')
		this.classList.add('occupied', 'choiced')
		var curr_cross = document.querySelector('.ans')
		if (curr_cross)
			curr_cross.parentNode.removeChild(curr_cross);
		svgNS = "http://www.w3.org/2000/svg"
		var cross = document.createElementNS(svgNS, 'text');
		cross.innerHTML = '&#x274C;';
		cross.setAttribute('x', this.getAttribute('x') - -(side / 2));
		cross.setAttribute('y', this.getAttribute('y') - -(side / 2));
		cross.classList.add('ans');
		svg_box.appendChild(cross);
	}
}