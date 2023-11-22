window.confirm_ending = confirm_ending // HACK make it available to non-modules, for a reason you’d better not think of

function confirm_ending(ev) {
	if (!confirm('Готовы завершить турнир? Передумать будет нельзя!'))
		ev.preventDefault()
}

var to_results = document.querySelector('.to_results');
to_results.addEventListener('click', confirm_ending);