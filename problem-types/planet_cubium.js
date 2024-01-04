var def_r = document.querySelector('.point').getAttribute('r')

for (point of document.querySelectorAll('.point'))
{
	point.onmouseover = function(){
		this.setAttribute('r', def_r - -2)
	}
	point.onmouseout = function(){
		this.setAttribute('r', def_r)
	}
	point.onclick = function(){
		if (this.classList.contains('selected'))
			this.classList.remove('selected')
		else
			this.classList.add('selected')
	}
}

document.querySelector('#send').onclick = function(){
	let ans = []
	for (point of document.querySelectorAll('.point'))
		if (point.classList.contains('selected'))
			ans.push(point.getAttribute('num'))
	document.querySelector('input[name="answer"]').value = ans.join(' ')
}