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
	link = f'/rules' if user_id is not None else f'/login?path=/land'

	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	yield f'<title>Квантландия</title>'
	yield '<link rel="icon" href="/static/design/icons/logo.svg">'
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

	yield '<div class="dialog answer" num="0">'
	yield '<div class="head">'
	yield '<div> Раздел участка </div>'
	yield '<div> <img class="cross" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="body">'
	yield '<img class="ans" src="/static/design/answer/fields.png" />'
	yield '</div>'
	yield '<div class="button solution"> Посмотреть решение </div>'
	yield '</div>'

	yield '<div class="dialog answer" num="1">'
	yield '<div class="head">'
	yield '<div> Кони-невидимки </div>'
	yield '<div> <img class="cross" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="body">'
	yield '<span class="bold_text"> Ответ:</span> <span class="text"> 3 </span>'
	yield '</div>'
	yield '<div class="button solution"> Посмотреть решение </div>'
	yield '</div>'

	yield '<div class="dialog answer" num="2">'
	yield '<div class="head">'
	yield '<div> Как такое возможно? </div>'
	yield '<div> <img class="cross" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="body">'
	yield '<span class="bold_text"> Ответ:</span> <span class="text"> 800 </span>'
	yield '</div>'
	yield '<div class="button solution"> Посмотреть решение </div>'
	yield '</div>'

	yield '<div class="dialog solution" num="0">'
	yield '<div class="head">'
	yield '<div> Раздел участка </div>'
	yield '<div> <img class="cross" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="body">' 
	yield '''<iframe width="560" height="315"
			src="https://www.youtube.com/embed/88lOJeuaHDw?enablejapi=1"
			frameborder="0"  allowfullscreen></iframe>'''
	yield '</div>'
	yield '<div class="button answer"> Посмотреть ответ </div>'
	yield '</div>'

	yield '<div class="dialog solution" num="1">'
	yield '<div class="head">'
	yield '<div> Кони-невидимки </div>'
	yield '<div> <img class="cross" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="body">' 
	yield '''<iframe width="560" height="315" class="video"
			src="https://www.youtube.com/embed/vqlC9c2LTV4?enablejsapi=1" 
			frameborder="0" allowfullscreen></iframe>'''
	yield '</div>'
	yield '<div class="button answer"> Посмотреть ответ </div>'
	yield '</div>'
	
	yield '<div class="dialog solution" num="2">'
	yield '<div class="head">'
	yield '<div> Как такое возможно? </div>'
	yield '<img class="cross" src="/static/design/icons/cross.svg" />'
	yield '</div>'
	yield '<div class="body">' 
	yield '''<iframe width="560" height="315"
			src="https://www.youtube.com/embed/m7lA9CoOq_g?enablejsapi=1&origin=http://localhost:8080" 
			frameborder="0" allowfullscreen></iframe>'''
	yield '</div>'
	yield '<div class="button answer"> Посмотреть ответ </div>'
	yield '</div>'

	yield '<div class="page_header"> Примеры задач </div>'
	yield '<div class="content">'
	yield '<div class="problem active" num="0">'

	yield '<div class="head">'
	yield '<div class="name"> Раздел участка </div>'
	yield '<div class="cost"> 3 квантика </div>'
	yield '</div>'

	yield '<div class="body">'
	yield '<div class="text_container">'
	yield '<div>'
	yield '<span class="text"> Двум братьям достался участок земли неправильной формы, схема которого ниже. Братья хотят разделить его на две равные по форме и размеру части. <br/><br/> </span>'
	yield '<span class="bold_text"> Помогите им это сделать (выделите клетки участка одного из братьев). </span>'
	yield '</div>'
	yield '</div>'
	yield '<img class="image" src="/static/design/problem_img/fields.png" />'
	yield '</div>'

	yield '<div class="button_area">'
	yield '<div class="button answer"> Посмотреть ответ </div>'
	yield '<div class="button solution"> Посмотреть решение </div>'
	yield '</div>'

	yield '</div>'

	yield '<div class="problem" num="1">'

	yield '<div class="head">'
	yield '<div class="name"> Кони-невидимки </div>'
	yield '<div class="cost"> 3 квантика </div>'
	yield '</div>'

	yield '<div class="body">'
	yield '<div class="text_container">'
	yield '<div>'
	yield '<span class="text"> На некоторых клетках доски 5×5 стоят невидимые шахматные кони, в каждой клетке не более одного. На некоторых клетках написали сколько всего коней бьют данную клетку (см. рисунок). <br/><br/> </span>'
	yield '<span class="bold_text"> Какое целое число должно стоять в центре доски? </span>'
	yield '</div>'
	yield '</div>'
	yield '<img class="image" src="/static/design/problem_img/invisible_horses.png" />'
	yield '</div>'

	yield '<div class="button_area">'
	yield '<div class="button answer"> Посмотреть ответ </div>'
	yield '<div class="button solution"> Посмотреть решение </div>'
	yield '</div>'

	yield '</div>'

	yield '<div class="problem" num="2">'

	yield '<div class="head">'
	yield '<div class="name"> Как такое возможно? </div>'
	yield '<div class="cost"> 3 квантика </div>'
	yield '</div>'

	yield '<div class="body">'
	yield '<div class="text_container">'
	yield '<div>'
	yield '<span class="text"> Стоимость доставки в онлайн-магазине составляет 250 рублей, но если сумма заказа не менее 750 рублей, то доставка бесплатна. И Ваня, и Маша купили с доставкой одну и ту же книгу. Но в честь ее дня рождения, Маше предоставили скидку 10%. Маша была крайне удивлена, обнаружив, что она заплатила на 170 рублей больше, чем Ваня. <br/><br/> </span>'
	yield '<span class="bold_text"> Какова была цена книги? </span>'
	yield '</div>'
	yield '</div>'
	yield '<img class="image" src="/static/design/problem_img/how_possible.png" />'
	yield '</div>'

	yield '<div class="button_area">'
	yield '<div class="button answer"> Посмотреть ответ </div>'
	yield '<div class="button solution"> Посмотреть решение </div>'
	yield '</div>'

	yield '</div>'
			   
	yield '<div class="nav">'
	yield '<img class="left_arrow" src="/static/design/left_arrow.svg" />'
	yield '<div class="pages">'
	yield '<div class="page selected" num="0"></div>'
	yield '<div class="page" num="1"></div>'
	yield '<div class="page" num="2"></div>'
	yield '</div>'
	yield '<img class="right_arrow" src="/static/design/right_arrow.svg" />'
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
