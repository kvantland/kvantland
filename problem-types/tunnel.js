var cur = null

$('.inside_line').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	if (cur != null) {
		$(cur).toggleClass('choiced not_choiced')
	}
	$(this).toggleClass('choiced not_choiced')
	cur = this
})

$('.submit_button').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	var ans = ''
	$('.choiced').each(function(index){ans = $(this).attr('pos') + ',' + $(this).attr('column') + ',' + $(this).attr('row')})
	$('[name="answer"]').val(ans)
})