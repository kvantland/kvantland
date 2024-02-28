$('rect').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	$(this).toggleClass('choiced not_choiced')
	$(this).attr('choiced', '1')
})

$('.submit_button').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	var ans = ''
	$('rect').each(function(index){ans += $(this).attr('choiced') + ','})
	$('[name="answer"]').val(ans)
})