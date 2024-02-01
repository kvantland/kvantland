var dialogs = document.getElementsByClassName('reg_dialog');
var dialog = '';

if (dialogs.length > 0){
	var dialog = dialogs[0];
};

if (dialog){
	var blur = document.getElementsByTagName('main')[0];
	var button = document.getElementsByClassName('dialog_button')[0];
	blur.classList.add('blur_zone'); 
	button.onclick = function(e){
		blur.classList.remove('blur_zone')
	}
}
