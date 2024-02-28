function confirm_action(text, button_arr, func_arr, kwargs_arr) {
	$('<div>', {'class': 'confirm_dialog show'})
		.append($('<div>', {'class': 'text_cont', 'text': text}))
		.append($('<div>', {'class': 'button_area'})
			.append($('<button>', {'class': 'confirm', 'text': button_arr[0]}))
			.append($('<button>', {'class': 'cancel', 'text': button_arr[1]})))
		.appendTo($('body'))
	$('<div>', {'class': 'shadow'}).appendTo($('body'))
	$('.confirm_dialog .button_area .confirm').on('click touchstart', function(e) {
		if (e.touches)
			e.preventDefault()
		$('.confirm_dialog, .shadow').detach()
		func_arr[0](kwargs_arr[0])
	})
	$('.confirm_dialog .button_area .cancel').on('click touchstart', function(e) {
		if (e.touches)
			e.preventDefault()
		$('.confirm_dialog, .shadow').detach()
		func_arr[1](kwargs_arr[1])
	})
}