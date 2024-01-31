from config import config

def display_problem():
	yield f'<div class="support_area">'
	yield f'<div class="text">Если возникли технические проблемы, напишите в нашу службу поддержки</div>'
	yield f'<a class="border" href="mailto:{config["contacts"]["support_email"]}">'
	yield f'<div class="button">{config["contacts"]["support_email"]}</div>'
	yield f'</a>'
	yield f'</div>'

def display_starter():
	yield '<div class="contacts_area">'
	yield '<div class="page_header">Будем на связи</div>'
	yield '<div class="text">В наших социальных сетях мы регулярно публикуем интересные новости о проекте, анонсы ближайших событий и нестандартные задачки для всех!    </br></br>  Присоединяйтесь и будете всегда в курсе событий!</div>'
	yield '<div class="button_area">'
	yield f'<a class="contact_button" href="{config["contacts"]["vk_link"]}"> <img class="contact_icon" src="/static/design/icons/vk.svg" /> </a>'
	yield f'<a class="contact_button" href="{config["contacts"]["tg_link"]}"> <img class="contact_icon" src="/static/design/icons/tg.svg" /> </a>'
	yield f'<a class="contact_button" href="{config["contacts"]["youtube_link"]}"> <img class="contact_icon" src="/static/design/icons/play.svg" /> </a>'
	yield f'<a class="contact_button" href="mailto:{config["contacts"]["support_email"]}"> <img class="contact_icon" src="/static/design/icons/email.svg" /> </a>'
	yield '</div>'
	yield '</div>'
