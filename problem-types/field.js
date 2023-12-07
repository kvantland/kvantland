"use strict";

const checked = 'checked';
const base = document.querySelector('.grid');
const sender = document.createElement('input');
sender.type = 'hidden';
sender.name = 'answer';
base.parentNode.appendChild(sender);

base.addEventListener('click', function(e) {
	let tile = e.target.closest('.tile');
	if (!tile || !base.contains(tile))
		return;
	tile.classList.toggle('checked');

	let answer = [];
	for (const row of base.rows) {
		if (row.classList.contains('pad'))
			continue;
		let answer_row = [];
		for (const cell of row.cells) {
			if (cell.classList.contains('pad'))
				continue;
			answer_row.push(cell.classList.contains(checked) ? 'x' : '-');
		}
		answer.push(answer_row.join(''))
	}
	sender.value = answer.join('\n')
});

