$('.submit_button').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	var ans = ''
	$('.fieldinput').each(function(index){ans += $(this).val()})
	$('[name="answer"]').val(ans)
})

$('input[type="number"]').on('keypress', function (e) {
    var maxlength = $(this).prop('maxlength');
    if (maxlength !== -1) {
        var length = $(this).val().trim().length;
        if (length + 1 > maxlength) e.preventDefault();
    }
});