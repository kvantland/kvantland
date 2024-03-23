$('.submit_button').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	var ans = ''
	$('.fieldinput').each(function(index){ans += $(this).val()})
	$('[name="answer"]').val(ans)
})