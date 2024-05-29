var free_squares = document.querySelectorAll('.square');
var sender = document.getElementsByName('answer')[0];
var svg_box = document.querySelector('svg');
var width = svg_box.getAttribute('width');
var side = document.querySelector('rect').getAttribute('width');

function send(e) {
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

document.querySelector('button').addEventListener("click", (e) => send(e))
document.querySelector('button').addEventListener("touchstart", (e) => send(e))

function choose(e, obj) {
	if (e.targetTouches)
		e.preventDefault()
	if (obj.classList.contains('free')) {
			obj.classList.remove('free')
			obj.classList.add('choiced')
			svgNS = "http://www.w3.org/2000/svg"
			var cross = document.createElementNS(svgNS, 'text');
			cross.innerHTML = '✔';
			cross.setAttribute('x', width - obj.getAttribute('y') - side / 2 - side / 4);
			cross.setAttribute('y', obj.getAttribute('x') - -(3*side / 4));
			cross.setAttribute('column', obj.getAttribute('column'));
			cross.setAttribute('row', obj.getAttribute('row'));
			cross.classList.add('tick');
			svg_box.appendChild(cross);
		} else {
			obj.classList.remove('choiced')
			obj.classList.add('free')
			for (const tick of document.querySelectorAll('.tick')){
				if (tick.getAttribute('column') == obj.getAttribute('column') && tick.getAttribute('row') == obj.getAttribute('row')){
					tick.parentNode.removeChild(tick);
					break;
				}
			}
		}
}

for (const square of free_squares){
	square.addEventListener("click", (e) => choose(e, square))
	square.addEventListener("touchstart", (e) => choose(e, square))		
}