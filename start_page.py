from bottle import route
from pathlib import Path

import nav
import user

def get_file(*paths):
	scripts = []
	for path_ in paths:
		path = Path(__file__).parent / f'static/design/{path_}.js'
		script = open(f'{path}', 'r', encoding="utf-8").read()
		scripts.append(script)
	return scripts

@route('/')
def display_start_page(db):
	scripts = get_file('start_page')

	user_id = user.current_user(db)
	link = f'/land' if user_id is not None else f'/login?path=/land'

	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	yield f'<title>Квантландия</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/start_page.css">'
	yield '<script type="module" src="/static/design/user.js"></script>'
	yield from user.display_banner(db)

	yield '<div class="content_wrapper">'

	yield '<div class="tournament">'
	yield '<img class="map" src="/static/map/land.png" />'
	yield '<div class="text_container">'
	yield '<div>'
	yield '<div class="header">Турнир</div>'
	yield '<div class="text">Твоя возможность проявить себя!</div>'
	yield '</div>'
	yield '<div class="text">Тебя ждут задачи из самых разных областей:  Головоломки, Логика, Комбинаторика, Арифметика, Геометрия</div>'
	yield f'<a href={link}>'
	yield '<div class="start_button"> Начать турнир </div>'
	yield '</a>'
	yield '</div>'
	yield '</div>'

	yield '<div class="info_container">'
	yield '<div class="page_header">О турнире</div>'
	yield '<div class="content">'

	yield '<div class="content_row">'
	yield '<div class="content_box">'
	yield '<img class="icon" src="/static/design/icons/screen.svg" />'
	yield '<div>'
	yield '<span class="bold_text"> Многие задачи интерактивны <br/></span>'
	yield '<span class="text"> <br/>Для их решения потребуется компьютер с мышкой или тачпадом, чтобы перетаскивать объекты и выделять клетки</span>'
	yield '</div>'
	yield '</div>'
	yield '<div class="content_box">'
	yield '<img class="icon" src="/static/design/icons/clock.svg" />'
	yield '<div>'
	yield '<span class="bold_text"> В турнире встречаются задачи разной сложности <br/> </span>'
	yield '<span class="text"> <br/> Но в среднем для решения задач нужно выделить примерно 60 минут </span>'
	yield '</div>'
	yield '</div>'
	yield '<div class="content_box">'
	yield '<img class="icon" src="/static/design/icons/calendar.svg" />'
	yield '<div>'
	yield '<span class="bold_text"> Турнир проходит в течение месяца. <br/> </span>'
	yield '<span class="text">  <br/>В любое время до закрытия турнира можно войти/зарегистрироваться и поучаствовать </span>'
	yield '</div>'
	yield '</div>'
	yield '</div>'

	yield '<div class="content_row">'
	yield '<div class="content_box">'
	yield '<img class="icon" src="/static/design/icons/planet.svg" />'
	yield '<div>'
	yield '<span class="text"> Примерно </span>'
	yield '<span class="bold_text"> 1200 детей <br/>из разных стран </span>'
	yield '<span class="text"> (Австралия, Болгария, Сербия, Россия, Казахстан, США, Белоруссия <br/>и др) поучаствовали в первом турнире </span>'
	yield '</div>'
	yield '</div>'
	yield '<div class="content_box">'
	yield '<img class="icon" src="/static/design/icons/gift.svg" />'
	yield '<div>'
	yield '<span class="text"> Победители по итогам сезона (несколько турниров) получат </span>'
	yield '<span class="bold_text">  призы от журнала "Квантик" </span>'
	yield '</div>'
	yield '</div>'
	yield '<div class="content_box">'
	yield '<img class="icon" src="/static/design/icons/medal.svg" />'
	yield '<div>'
	yield '<span class="bold_text"> В зачёт идут 3 лучших результата из 4. <br/> </span>'
	yield '<span class="text"> <br/>Взрослые тоже могут участвовать, но в отдельном зачёте. </span>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'

	yield '<div class="examples_container">'
	yield '<div class="page_header"> Примеры задач </div>'
	yield '<div class="content">'
	yield '<div class="problem">'

	yield '<div class="head">'
	yield '<div class="name"> Король и два придворных мудреца </div>'
	yield '<div class="cost"> 3 квантика </div>'
	yield '</div>'

	yield '<div class="body">'
	yield '<div class="text_container">'
	yield '<div>'
	yield '<span class="text"> Король решил проверить своих мудрецов: первый должен в тайне от второго записать 7 различных натуральных чисел с суммой 72 и сообщить второму мудрецу лишь 3-е по величине из загаданных чисел. После чего второй мудрец должен назвать все записанные числа. У мудрецов не было возможности сговориться, но тем не менее они справились с заданием. <br/><br/> </span>'
	yield '<span class="bold_text"> Какое число сообщил первый? </span>'
	yield '</div>'
	yield '</div>'
	yield '<img class="image" src="/static/design/problem_img/Mudrez.png" />'
	yield '</div>'

	yield '<div class="button_area">'
	yield '<div class="button"> Посмотреть ответ </div>'
	yield '<div class="button"> Посмотреть решение </div>'
	yield '</div>'
	yield '</div>'
			   
	yield '<div class="nav">'
	yield '<img src="/static/design/left_arrow.svg" />'
	yield '<div class="pages">'
	yield '<div class="page selected" num="1"></div>'
	yield '<div class="page" num="2"></div>'
	yield '<div class="page" num="3"></div>'
	yield '</div>'
	yield '<img src="/static/design/right_arrow.svg" />'
	yield '</div>'
	yield '</div>'
	yield '</div>'

	yield '<div class="contacts_area">'
	yield '<div class="page_header">Будем на связи</div>'
	yield '<div class="text">В наших социальных сетях мы регулярно публикуем интересные новости о проекте, анонсы ближайших событий и нестандартные задачки для всех!    </br></br>  Присоединяйтесь и будете всегда в курсе событий!</div>'
	yield '<div class="button_area">'
	yield '<div class="contact_button"> <img class="contact_icon" src="/static/design/icons/vk.svg" /> </div>'
	yield '<div class="contact_button"> <img class="contact_icon" src="/static/design/icons/tg.svg" /> </div>'
	yield '<div class="contact_button"> <img class="contact_icon" src="/static/design/icons/play.svg" /> </div>'
	yield '<div class="contact_button"> <img class="contact_icon" src="/static/design/icons/email.svg" /> </div>'
	yield '</div>'
	yield '</div>'

	yield '</div>'
	for script in scripts:
		if script:
			yield f'<script type="text/ecmascript">{script}</script>'
