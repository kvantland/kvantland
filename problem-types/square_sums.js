function exchange(){
}

for (card of document.querySelectorAll('.card'))
{
	card.onclick = function(){
		if (!document.querySelector('.exchange'))
		{
			if (this.classList.contains('selected'))
			{
				this.classList.remove('selected')
				this.setAttribute('transform', 'translate(' + `${this.getAttribute('transform').split('(')[1].split(' ')[0]}` + ' ' + `${this.getAttribute('transform').split(' ')[1].split(')')[0] - -10}` + ')')
			}
			else
			{
				this.classList.add('selected')
				this.setAttribute('transform', 'translate(' + `${this.getAttribute('transform').split('(')[1].split(' ')[0]}` + ' ' + `${this.getAttribute('transform').split(' ')[1].split(')')[0] - 10}` + ')')
			}
		}
	}
}

document.addEventListener('click', exchange())