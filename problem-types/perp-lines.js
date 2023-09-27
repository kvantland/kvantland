var points = document.getElementsByClassName('point');
var area = document.getElementsByClassName('plot_area')[0];
var curr_point = '';
var curr_point_name = '';

for (let i = 0; i < points.length; i++){
	points[i].onclick = function(e){
		if (curr_point){
			curr_point.classList.remove('base_point');
			curr_point_name.remove();
		}
		points[i].classList.add('base_point');
		curr_point = points[i];
		curr_point_name = document.createElement('div');
		curr_point_name.className = "point_name";
		curr_point_name.innerHTML = 'D';
		var x = parseInt(curr_point.getAttribute('cx'), 10);
		var y = parseInt(curr_point.getAttribute('cy'), 10);
		curr_point_name.style.top = String(y - 26) + 'px';
		curr_point_name.style.left = String(x - 26) + 'px';
		area.append(curr_point_name);
	}
};

var curr_form = document.getElementById('problem_form');
var sender = document.getElementsByName('answer')[0];


document.querySelector('button').onclick = function(e){
	var x = parseInt(curr_point.getAttribute('cx'), 10);
	var y = parseInt(curr_point.getAttribute('cy'), 10);
	var i = Math.floor((x - 6) / 40);
	var j = Math.floor((y - 7) / 40);
	var answer = [j, i];
	sender.value = answer.join('');
}