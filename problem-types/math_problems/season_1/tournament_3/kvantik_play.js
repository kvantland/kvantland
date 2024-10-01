$('.submit_button').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	var ans = ''
	$('.fieldinput').each(function(index){ans += $(this).val()})
	$('[name="answer"]').val(ans)
})

$('input[type="text"]').on('keypress', function (e) {
	if (e.key.length === 1 && /\D/.test(e.key)) {
    	e.preventDefault();
    }
    var maxlength = $(this).prop('maxlength');
    if (maxlength !== -1) {
        var length = $(this).val().trim().length;
        if (length + 1 > maxlength) e.preventDefault();
    }
});

$('input[type="text"]').on('keyup', function (e) {
	$(this).attr("value", $(this).val())
});