for (let field of document.querySelectorAll('.full_field')) {
	let inp = field.querySelector('input')
	if (!inp)
		inp = field.querySelector('select')
	if (!inp)
		continue;
	inp.addEventListener('invalid', function(e){
		e.preventDefault()
		let img = field.querySelector('.info')
		if (img)
			img.classList.remove('hidden')
		let text = field.querySelector('.err')
		text.innerHTML = 'Поле обязательно для заполнения'
		text.classList.remove('hidden')
	})
	inp.addEventListener('input', function(){
		let img = field.querySelector('.info')
		if (img)
			img.classList.add('hidden')
		let text = field.querySelector('.err')
		text.innerHTML = ''
		text.classList.add('hidden')
	})
}

// select mechanics

var tmp = 0

document.addEventListener('click', select_hide)
document.addEventListener('touch', select_hide)

function select_show(e) {
	if (e.touches)
		e.preventDefault();
	let name = e.currentTarget.getAttribute('name')
	let select = document.querySelector(`div.select_box[name=${name}`)
	if (!select.classList.contains('hidden')) {
		select.classList.add('hidden')
		select.classList.remove('shown')
	}
	else {
		select.classList.remove('hidden')
		select.classList.add('shown')
		tmp = 1
	}
}

function select_hide(e) {
	if (e.touches)
		e.preventDefault();
	if (tmp) {
		tmp = 0;
		return;
	}
	for (let select of document.querySelectorAll('div.select_box')) {
		if (!select.classList.contains('hidden')) {
			select.classList.add('hidden')
			select.classList.remove('shown')
		}
	}
}

function choiced(e) {
	if (e.touches)
		e.preventDefault();
	let curr = e.target
	let name = curr.parentNode.getAttribute('name')
	console.log(name)
	for (let option of curr.parentNode.querySelectorAll('.option')) {
		if (option.classList.contains('selected'))
			option.classList.remove('selected')
	}
	curr.classList.add('selected')
	let inp = document.querySelector(`input[name=${name}]`)
	inp.value = curr.innerHTML.trim()
}

for (let select of document.querySelectorAll('div.select_box')) {
	let name = select.getAttribute('name')
	console.log(name)
	let inp = document.querySelector(`div.select_line[name=${name}]`)
	inp.addEventListener('click', select_show)
	inp.addEventListener('touch', select_show)
	for (let option of select.querySelectorAll('.option'))
	{
		option.addEventListener('click', choiced)
		option.addEventListener('touch', choiced)
	}
}