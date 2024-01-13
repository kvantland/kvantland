var free_squares = document.querySelectorAll('.square');
var sender = document.getElementsByName('answer')[0];
var svg_box = document.querySelector('svg');
var width = svg_box.getAttribute('width');
var side = document.querySelector('rect').getAttribute('width');

document.querySelector('button').onclick = function(e){
	var curr = [];
	for (const square of free_squares){
		if (square.classList.contains('choiced')){
			var x = square.getAttribute('column');
			var y = square.getAttribute('row');
			curr.push([x, y]);
		}
	}
	sender.value = curr;
}

for (const square of free_squares){
	square.onclick = function(){
		if (this.classList.contains('free')) {
			this.classList.remove('free')
			this.classList.add('choiced')
			svgNS = "http://www.w3.org/2000/svg"
			var cross = document.createElementNS(svgNS, 'text');
			cross.innerHTML = '✔';
			cross.setAttribute('x', width - this.getAttribute('y') - side / 2 - side / 4);
			cross.setAttribute('y', this.getAttribute('x') - -(3*side / 4));
			cross.setAttribute('column', this.getAttribute('column'));
			cross.setAttribute('row', this.getAttribute('row'));
			cross.classList.add('tick');
			svg_box.appendChild(cross);
		} else {
			this.classList.remove('choiced')
			this.classList.add('free')
			for (const tick of document.querySelectorAll('.tick')){
				if (tick.getAttribute('column') == this.getAttribute('column') && tick.getAttribute('row') == this.getAttribute('row')){
					tick.parentNode.removeChild(tick);
					break;
				}
			}
		}
		
	}
}