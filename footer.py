from config import config

def display_problem():
	yield f'<div class="problem_footer_border">'
	yield f'<div class="problem_footer">'
	yield f'<div class="problem_footer_text">Если возникли технические проблемы, напишите в нашу службу поддержки</div>'
	yield f'<a class="support_button_border" href="mailto:{config["contacts"]["support_email"]}">'
	yield f'<div class="support_button">{config["contacts"]["support_email"]}</div>'
	yield f'</a>'
	yield f'</div>'
	yield f'</div>'
