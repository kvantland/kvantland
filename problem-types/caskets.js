function open_casket(casket, config) {
	if (casket.getAttribute('tmp') >= 6) {
		clearInterval(movement)
		window.location.reload('true')
		return;
	}
	casket.setAttribute('tmp', casket.getAttribute('tmp') - -1)
	casket.setAttribute('src', '/static/casket/' + config + '_' + casket.getAttribute('tmp') + '.png') 
}

function send_xhr(e) {
	if (e.touches)
		e.preventDefault()
	let url = new URL(window.location.href + 'xhr')
	let casket = e.currentTarget
	casket.setAttribute('src', '/static/casket/empty_6.png')
	let solution_empty = $('#problem_form')[0].outerHTML
	casket.setAttribute('src', '/static/casket/full_6.png')
	let solution_full = $('#problem_form')[0].outerHTML
	casket.setAttribute('src', '/static/casket/empty_1.png')
	$.post(url, JSON.stringify({'answer': casket.getAttribute('num'), 'solution_empty': solution_empty, 'solution_full': solution_full}), function(data){
		if (data == 'true')
			movement = setInterval(function(){open_casket(casket, 'full')}, 30)
		else if (data == 'false')
			movement = setInterval(function(){open_casket(casket, 'empty')}, 30)
		else 
			show_xhr('Попытки закончились!')
	})
}

var movement = ''
$(".casket").on("click touchstart", send_xhr)