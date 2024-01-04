var free_squares = document.querySelectorAll('.square');
var sender = document.getElementsByName('answer')[0];

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
		} else {
			this.classList.remove('choiced')
			this.classList.add('free')
		}
		
	}
}