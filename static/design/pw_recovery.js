for (let field of document.querySelectorAll('.full_field')) {
	let inp = field.querySelector('input')
	if (!inp)
		inp = field.querySelector('select')
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