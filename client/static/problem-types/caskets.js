function open_casket(casket, config) {
    console.log('here!')
	if ($(casket).attr('tmp') >= 6) {
		clearInterval(movement)
		window.location.reload('true')
		return;
	}
	$(casket).attr('tmp', casket.getAttribute('tmp') - -1)
	$(casket).attr('src', '/problem_assets/casket/' + config + '_' + $(casket).attr('tmp') + '.png') 
}

function send_xhr(params) {
	let url = new URL(window.location.href + 'xhr')
	let casket = params['casket']
	$(casket).attr('src', '/problem_assets/casket/empty_6.png')
	let solution_empty = $('#problem_form')[0].outerHTML
	$(casket).attr('src', '/problem_assets/casket/full_6.png')
	let solution_full = $('#problem_form')[0].outerHTML
	$(casket).attr('src', '/problem_assets/casket/empty_1.png')
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
console.log('HEEEEELP')
console.log($('.casket'))
$('.casket').on('click', function(){console.log('some!')})

/*$(".casket").on("click", function(){confirm_action('Вы уверены, что хотите выбрать эту шкатулку? Больше попыток не будет.', 
	['Подтердить', 'Отмена'], 
	[send_xhr, function(){}],
	[{'casket': this}, {}])})*/