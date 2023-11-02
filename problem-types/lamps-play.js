"use strict"

var buttons = document.querySelectorAll('.lamp_switch');

for (let button of buttons){
	button.onclick = function(){
		if (button.classList.contains('active'))
			button.classList.remove('active');
		else
			button.classList.add('active');
	}
}
document.addEventListener("DOMContentLoaded", () => {
	let answer = Array(switches.length).fill(0)

	function toggle_switch(id) {
		answer[id] ^= 1
		let sw = switches[id]
		for (let y = 0; y < h; y++)
			for (let x = 0; x < w; x++) {
				if (sw[y][x])
					document.getElementById(`lamp_${x}_${y}`).classList.toggle('lamp_on')
			}
		i_answer.value = JSON.stringify(answer)
	}

	for (let sw of document.getElementsByClassName("lamp_switch")) {
		let id = sw.dataset.id
		sw.addEventListener("click", (e) => toggle_switch(id))
	}
})
