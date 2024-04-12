var cur = null
var width = $('.inside_line').attr('width')
var height = $('.inside_line').attr('height')
var svg_box = document.querySelector('svg');

$('.inside_line').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	if (cur != null) {
		$(cur).toggleClass('choiced not_choiced')
		$('.cross').remove()
	}
	$(this).toggleClass('choiced not_choiced')
	cur = this
	svgNS = "http://www.w3.org/2000/svg"
	var cross = document.createElementNS(svgNS, 'text');
	cross.innerHTML = '&#x274C;';
	cross.setAttribute('x', $(cur).attr('x') - -($(cur).attr('width') / 2));
	cross.setAttribute('y', $(cur).attr('y') - -($(cur).attr('height') / 2));
	cross.classList.add('cross');
	svg_box.appendChild(cross);
})

$('.submit_button').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	var ans = ''
	$('.choiced').each(function(index){ans = $(this).attr('pos') + ',' + $(this).attr('column') + ',' + $(this).attr('row')})
	$('[name="answer"]').val(ans)
})