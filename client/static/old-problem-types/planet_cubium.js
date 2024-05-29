var def_r = document.querySelector('.point').getAttribute('r')

for (let point of document.querySelectorAll('.point'))
{
	point.addEventListener("mouseover", (e) => expanse(e, point))
	point.addEventListener("mouseout", (e) => compress(e, point))
	point.addEventListener("click", (e) => select(e, point))
	point.addEventListener("touchstart", (e) => select(e, point))
}

function compress(e, obj) {
	if (e.touches)
		e.preventDefault()
	else
		obj.setAttribute('r', def_r)
}

function expanse(e, obj) {
	if (e.touches)
		e.preventDefault()
	else
		obj.setAttribute('r', def_r - -2)
}

function select(e, obj) {
	if (e.touches)
		e.preventDefault()
	if (obj.classList.contains('selected'))
		obj.classList.remove('selected')
	else
		obj.classList.add('selected')
}

function send(e) {
	let ans = []
	for (point of document.querySelectorAll('.point'))
		if (point.classList.contains('selected'))
			ans.push(point.getAttribute('num'))
	document.querySelector('input[name="answer"]').value = ans.join(' ')
}

document.querySelector('#send').addEventListener("click", (e) => send(e))
document.querySelector("#send").addEventListener("touchstart", (e) => send(e)) 
