var points = document.getElementsByClassName('point');
var area = document.getElementsByClassName('plot_area')[0];
var curr_point = '';
var curr_point_name = '';

for (let i = 0; i < points.length; i++){
	points[i].onmouseover = function(e){
		if (points[i].style.fill != 'red'){
			points[i].style.fill = 'rgba(1, 0, 0, 0.5)';
		}
	};

	points[i].onmouseout = function(e){
		if (points[i].style.fill != 'red'){
			points[i].style.fill = 'rgba(0, 0, 0, 0)';
		}
	};

	points[i].onclick = function(e){
		if (curr_point){
			curr_point.style.fill = 'rgba(0, 0, 0, 0)';
			curr_point_name = document.getElementById("curr_point_name");
			curr_point_name.remove();
		}
		points[i].style.fill = 'red';
		curr_point = points[i];
		curr_point_name = document.createElement('div');
		curr_point_name.className = "point_name";
		curr_point_name.innerHTML = 'D';
		curr_point_name.id = "curr_point_name";
		var x = parseInt(curr_point.getAttribute('cx'), 10);
		var y = parseInt(curr_point.getAttribute('cy'), 10);
		curr_point_name.style.top = String(y - 26) + 'px';
		curr_point_name.style.left = String(x - 26) + 'px';
		area.append(curr_point_name);
	}
};

var curr_form = document.getElementById('problem_form');
var sender = document.createElement('input');
sender.name = 'answer';
sender.type= 'hidden';
curr_form.append(sender);
var x = 0;
var y = 0;



document.querySelector('button').onclick = function(e){
	x = parseInt(curr_point.getAttribute('cx'), 10);
	y = parseInt(curr_point.getAttribute('cy'), 10);
	var i = Math.floor((x - 6) / 40);
	var j = Math.floor((y - 6) / 40);
	var answer = [j, i];
	sender.value = answer.join('');
}