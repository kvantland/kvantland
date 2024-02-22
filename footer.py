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
	yield f'<a class="contact_button" href="{config["contacts"]["vk_link"]}" target="_blank"> <img class="contact_icon" src="/static/design/icons/vk.svg" /> </a>'
	yield f'<a class="contact_button" href="{config["contacts"]["tg_link"]}" target="_blank"> <img class="contact_icon" src="/static/design/icons/tg.svg" /> </a>'
	yield f'<a class="contact_button" href="{config["contacts"]["youtube_link"]}" target="_blank"> <img class="contact_icon" src="/static/design/icons/play.svg" /> </a>'
	yield f'<a class="contact_button" href="mailto:{config["contacts"]["support_email"]}" target="_blank" title="{config["contacts"]["support_email"]}"> <img class="contact_icon" src="/static/design/icons/email.svg" /> </a>'
	yield '</div>'
	yield f'<div> Адрес техподдержки: <a  href="mailto:{config["contacts"]["support_email"]}" target="_blank"> {config["contacts"]["support_email"]} </a></div>'
	yield '</div>'

def display_basement():
	yield '<div class="basement">'

	yield '<hr size="1" color="#1E8B93" noshade />'

	yield '<div class="content">'
	yield '<a href="/">'
	yield '<div class="logo_area">'
	yield '<img class="logo" src="/static/design/icons/logo.svg" />'
	yield '<div class="logo_name"> КВАНТ<br/>ЛАНДИЯ </div>'
	yield '</div>'
	yield '</a>'

	yield '<div class="confidentiality"><a href="/policy"> Политика конфиденциальности </a></div>'

	yield '<div class="organization"> © ООО "Квантик", 2024 </div>'
	yield '</div>'

	yield '</div>'
