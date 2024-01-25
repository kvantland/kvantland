let names = document.querySelectorAll('text.town-name')

for (let name of names) {

	let box = name.getBBox()
	let [h, v] = [box.width, box.height]
	let [h_p, v_p] = [13.3, 2.17]
	let r = 6
	let [x, y] = [h + 2 * h_p, v + 2 * v_p]
	let up = name.getAttribute('y')

	let rect = document.querySelector(`path.town-name[num="${name.getAttribute('num')}"]`)
	let path = `m 0 ${r} v ${v + v_p * 2 - r * 2} a ${r} ${r} 0 0 0 ${r} ${r} h ${h + h_p * 2 - r * 2} a ${r} ${r} 0 0 0 ${r} ${-r} v ${-v - v_p * 2 + r * 2} a ${r} ${r} 0 0 0 ${-r} ${-r} h ${-h - h_p * 2 + r * 2} a ${r} ${r} 0 0 0 ${-r} ${r} z`
	rect.setAttribute('d', path)
	let rect_box = rect.getBoundingClientRect()
	let [rect_x, rect_y] = [-x / 2, up - y / 2]
	rect.setAttribute('transform', `translate(${rect_x} ${rect_y})`)
	console.log(path, rect_x, rect_y)
}