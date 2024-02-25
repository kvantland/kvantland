for (let field of document.querySelectorAll('.full_field')) {
	let inp = field.querySelector('input')
	inp.addEventListener('invalid', function(e){
		e.preventDefault()
		let img = field.querySelector('.info')
		img.classList.remove('hidden')
		let text = field.querySelector('.err')
		text.innerHTML = 'Поле обязательно для заполнения'
		text.classList.remove('hidden')
	})
	inp.addEventListener('input', function(){
		let img = field.querySelector('.info')
		img.classList.add('hidden')
		let text = field.querySelector('.err')
		text.innerHTML = ''
		text.classList.add('hidden')
	})
}