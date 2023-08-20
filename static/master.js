function confirm_answer(ev) {
	if (!confirm('Готовы отправить ответ? Передумать будет нельзя!'))
		ev.preventDefault()
}

for (let form of document.forms) {
	form.addEventListener('submit', confirm_answer)
}
