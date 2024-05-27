var width = $('.inside_line').attr('width')
var height = $('.inside_line').attr('height')
var svg_box = document.querySelector('svg');

$('.inside_line').on('click touchstart', function(e){
	if (e.touches)
		e.preventDefault()
	$('.choiced').toggleClass('choiced not_choiced')
	$('.cross').remove()
	$(this).toggleClass('choiced not_choiced')
	svgNS = "http://www.w3.org/2000/svg"
	var cross = document.createElementNS(svgNS, 'text');
	cross.innerHTML = '&#x274C;';
	cross.setAttribute('x', $(this).attr('x') - -($(this).attr('width') / 2));
	cross.setAttribute('y', $(this).attr('y') - -($(this).attr('height') / 2));
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