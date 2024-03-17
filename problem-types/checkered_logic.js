$('.field').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	$(this).toggleClass('choiced not_choiced')
	if (this.classList.contains('choiced')) {
		$(this).attr('choiced', '1')

	} else {
		$(this).attr('choiced', '0')

	}
})

$('.submit_button').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	var ans = ''
	$('.field').each(function(index){ans += $(this).attr('choiced') + ','})
	$('[name="answer"]').val(ans)
})