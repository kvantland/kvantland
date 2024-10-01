var inputs = document.querySelectorAll('input[type=radio]');

for (let i = 0; i < inputs.length; i++){
	inputs[i].onclick = function(event){
		this.setAttribute('checked', 'checked');
		for (let j = 0; j < inputs.length; j++)
			if (inputs[j].hasAttribute('checked') && j != i)
				inputs[j].removeAttribute('checked');
	}
}