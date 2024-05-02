$('rect').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	$(this).toggleClass('choiced not_choiced')
})

$('.submit_button').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	var ans = ''
	$('rect').each(function(index){ans += +$(this).hasClass('choiced') + ','})
	$('[name="answer"]').val(ans)
})