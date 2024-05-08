
function block_nav() {
	let nav = document.querySelector('.user_nav')
	if (!nav.classList.contains('blocked'))
		nav.classList.add('blocked')
}


function scroll(e) {
	let add = document.querySelector('nav').getBoundingClientRect().height
	if (e.touches)
		e.preventDefault()
	let id = e.currentTarget.id
	let X, Y, box, key_obj
    
	switch(id) {
		case 'info': {
			key_obj = document.querySelector('.info_container').getBoundingClientRect();
			[X, Y] = [key_obj.left, key_obj.top];
			break;
		}
		case 'team': {
			key_obj = document.querySelector('.team_container').getBoundingClientRect();
			[X, Y] = [key_obj.left, key_obj.top]
			break;
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
	block_nav()
	window.scrollTo(X + window.pageXOffset, Y - add + window.pageYOffset)
}

for (let menu_button of document.querySelectorAll('.menu_item')) {
	menu_button.addEventListener('click', scroll)
	menu_button.addEventListener('touchstart', scroll)
}
