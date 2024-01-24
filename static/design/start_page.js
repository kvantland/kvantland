function scroll(e) {
	let add = document.querySelector('nav').getBoundingClientRect().height
	if (e.touches)
		e.preventDefault()
	let id = e.target.id
	let X, Y, box, key_obj
	switch(id) {
		case 'info': {
			key_obj = document.querySelector('.info_container').getBoundingClientRect();
			[X, Y] = [key_obj.left, key_obj.top];
			break;
		}
		case 'team': {
			[X, Y] = [-window.pageXOffset, -window.pageYOffset];
			break;
			// key_obj = document.querySelector('.team_container').getBoundingClientRect();
			// [X, Y] = [key_obj.left, key_obj.top]
		}
		case 'examples': {
			key_obj = document.querySelector('.examples_container').getBoundingClientRect();
			[X, Y] = [key_obj.left, key_obj.top];
			break;
		}
		case 'contacts': {
			key_obj = document.querySelector('.contacts_area').getBoundingClientRect();
			[X, Y] = [key_obj.left, key_obj.top];
			break;
		}
	}
	console.log(X, Y)
	window.scrollTo(X + window.pageXOffset, Y - add + window.pageYOffset)
}

for (let menu_button of document.querySelectorAll('.menu_item')) {
	menu_button.addEventListener('click', scroll)
	menu_button.addEventListener('touchstart', scroll)
}
