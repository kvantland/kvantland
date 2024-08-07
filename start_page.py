from bottle import route
from pathlib import Path

import nav
import user
import footer
import json
from config import config


@route('/api/tournament_history')
def get_tournament_history():
	tournament_history = [
		{'event_name': 'Старт Турнира 1', 'event_date': '05.12.2023'},
		{'event_name': 'Финиш Турнира 1', 'event_date': '31.03.2024'},
		{'event_name': 'Старт Турнира 2', 'event_date': '24.02.2024'},
		{'event_name': 'Финиш Турнира 2', 'event_date': '31.03.2024'},
		{'event_name': 'Старт Турнира 3', 'event_date': '22.04.2024'},
		{'event_name': 'Финиш Турнира 3', 'event_date': '15.06.2024'},
		{'event_name': 'Старт Турнира 4', 'event_date': '08.08.2024'},
		{'event_name': 'Финиш Турнира 4', 'event_date': '09.09.2024'},
		]
	events_amount = 4
	first_event = max(0, len(tournament_history) - events_amount)
	return json.dumps(tournament_history[first_event:])


@route('/api/info_cards')
def get_common_info_cards():
	info_cards = [
		{   'image': "screen.svg",
            'desc':  """<span class="bold_text">Многие задачи интерактивны</span> <br/><br/>Для их
                        решения потребуется компьютер с мышкой или тачпадом,
                        чтобы перетаскивать объекты и выделять клетки"""},
						
		{   'image': "clock.svg",
            'desc': """<span class="bold_text">В турнире встречаются задачи разной сложности </span> 
			            <br/> </br>Для решения задач рекомендуем выделить примерно 60 - 90
						минут"""},
						
		{   'image': "calendar.svg",
            'desc': """<span class="bold_text">Турнир проходит в течение месяца</span> <br/> <br/>
			            В любое время до закрытия турнира можно войти/зарегистрироваться
						и поучаствовать"""},
						
        {   'image': "planet.svg",
		    'desc': """Примерно <span class="bold_text">1300 детей и взрослых из разных стран </span> 
			            (Австралия, Болгария, Сербия, Россия, Казахстан, США, 
						Белоруссия и других) поучаствовали в первом турнире"""},
						
		{   'image': "gift.svg",
            'desc': """Турнир индивидуальный и рассчитан на школьников 7-9 
			            классов и младше. Победители по итогам сезона  
						(несколько турниров) получат <span class="bold_text">призы от журнала 
						"Квантик"</span> """},
						
        {   'image': "medal.svg",
		    'desc': """<span class="bold_text">В зачёт идут 2 лучших результата из 4</span> <br/> 
			            <br/> Взрослые тоже могут участвовать, но в отдельном зачёте (с призами 
						для победителей)"""},
										
    ]
	return json.dumps(info_cards)


@route('/api/problem_examples')
def get_problem_examples():
	problem_examples = [
		{   
			'title': "Раздел участка",
            'image': "fields.png",
            'desc': """Двум братьям достался участок земли неправильной формы, схема 
			            которого ниже. Братья хотят разделить его на две равные по форме 
						и размеру части. <br/> <br/> <span class="bold_text"> Помогите им 
						это сделать (выделите клетки участка одного из братьев).</span>""",
			'solution_image': "fields.png",
			'solution_video_link': "https://www.youtube.com/embed/88lOJeuaHDw?enablejsapi=1",
			'cost': "3 квантика",
		},
			
        {   
			'title': "Кони-невидимки",
            'image': "invisible_horses.png",
			'desc': """На некоторых клетках доски 5×5 стоят невидимые шахматные кони, в каждой 
			            клетке не более одного. На некоторых клетках написали, сколько всего 
						коней бьют данную клетку (см. рисунок).<br/><br/> <span class="bold_text"> 
						Какое целое число должно стоять в центре доски? </span>""",
			'answer': "0",
			'solution_video_link': "https://www.youtube.com/embed/vqlC9c2LTV4?enablejsapi=1",
			'cost': "3 квантика",
        },
		
        {
			'title': "Как такое возможно?",
			'image': "how_possible.png",
			'desc': """Стоимость доставки в онлайн-магазине составляет 250 рублей, но 
			            если сумма заказа не менее 750 рублей, то доставка бесплатна. И Ваня, 
						и Маша купили с доставкой одну и ту же книгу. Но в честь ее дня рождения, 
						Маше предоставили скидку 10%. Маша была крайне удивлена, обнаружив, что 
						она заплатила на 170 рублей больше, чем Ваня. 
						<span class="bold_text"> Какова была цена книги? </span>""",
			'answer': "800",
			'solution_video_link': "https://www.youtube.com/embed/m7lA9CoOq_g?enablejsapi=1",
			'cost': "3 квантика",
        },
		
    ]
	return json.dumps(problem_examples)


# type "personal" used for personal cards, "list" - for cards with listed members
@route('/api/team_cards')
def get_team_cards():
	team_cards = [
		{
			'type': "personal",
			'id': "M_Evdokimov",
			'name': "Михаил Евдокимов",
			'desc': """Автор многих олимпиадных задач по математике: Турнир Городов, 
			            Московская олимпиада, Всероссийская, Матпраздник и других.<br/><br/>
						Автор книг «Сто граней математики» и «От задачек к задачам», один из 
						авторов журнала «Квантик».""",
			'image': "M_Evdokimov.png",
        },
		
        {
			'type': "personal",
			'id': "A_Shapovalov",
			'name': "Александр Шаповалов",
			'desc': """Автор дюжины книг по кружковой и олимпиадной математике, автор 
			            около 1000 олимпиадных задач.<br/><br/> Преподаватель летних 
						школ и онлайн-кружков, ответственный редактор серии «Школьные 
						математические кружки».""",
			'image': "A_Shapovalov.png",
        },
		
        {
			'type': "personal",
			'id': "A_Gribalco",
			'name': "Александр Грибалко",
			'desc': """Автор многих олимпиадных задач по математике: Турнир Городов, 
			            Московская олимпиада, Матпраздник и других.<br/><br/>Председатель 
						жюри турнира математических боев имени А.П. Савина. Автор трех 
						книг по материалам турнира.""",
			'image': "A_Gribalco.png",
        },
		
        {
			'type': "personal",
			'id': "E_Bakaev",
			'name': "Егор Бакаев",
			'desc': """Автор многих олимпиадных задач по математике: Турнир Городов, 
			            Московская олимпиада, Всероссийская, Матпраздник и других олимпиад.
						<br/><br/>Преподаватель кружков по олимпиадной математике в ведущих 
						школах Москвы. Редактор журнала “Квант”.""",
			'image': "E_Bakaev.png",
        },
		
        {
			'type': "personal",
			'id': "B_Butyrin",
			'name': "Богдан Бутырин",
			'desc': """Автор олимпиадных задач по математике: Турнир Городов, Московская 
			            олимпиада. Призёр Всероссийской олимпиады.<br/><br/>Автор Youtube-канала 
						MathOlymp, студент ФКН ВШЭ.""",
			'image': "B_Butyrin.png",
        },
		
        {
			'type': "list",
			'id': "DevTeam",
			'desc': [
				{
                    'title': "Редакторы",
                    'team_members': ["С. Дориченко", "Г. Мерзон", "Т. Корчемкина", "М. Прасолов"]
                },
				{
					'title': "IT",
					'team_members': ["Д. Чертоляс", "В. Аксенов", "Д. Миронов", "В. Лобачевский"]
                },
				{
					'title': "Дизайнер",
					'team_members': ["А.Москаленко"]
                },
				{
					'title': "Художник",
					'team_members': ["А.Вайнер"]
                },
            ]
        },
		
    ]
	return json.dumps(team_cards)


@route('/api/contacts')
def get_contacts():
	contacts = [
		{
			'id': "vk",
			'image': "vk.svg",
			'source_link': config['contacts']['vk_link']
        },
		
        {
			'id': "telegram",
			'image': "tg.svg",
			'source_link': config['contacts']['tg_link']
        },
		
        {
			'id': "youtube",
			'image': "play.svg",
			'source_link': config['contacts']['youtube_link']
        },
		
        {
			'id': "email",
			'image': "email.svg",
			'source_link': "mailto:" + config['contacts']['support_email']
        }
    ]
	
	return json.dumps(contacts)
	

@route('/')
def display_start_page(db):

	user_id = user.current_user(db)
	link = f'/rules' if user_id is not None else f'/login?path=/land'

	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	yield f'<title>Квантландия</title>'
	yield f'<link rel="icon" href="/static/design/icons/logo.svg" type="image/svg+xml">'
	yield f'<link rel="icon" href="/static/design/icons/favicon.ico" sizes="48x48">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/footer.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/start_page.css">'
	yield '<script type="module" src="/static/design/user.js"></script>'
	yield from user.display_banner(db)
	yield '<div class="content_wrapper">'

	yield '<div class="tournament">'
	yield '<div class="curr_tournament">'
	yield '<img class="map" loading="lazy" src="/static/map/land.png" />'
	yield '<div class="text_container">'
	yield '<div>'
	yield '<div class="header">Турнир</div>'
	yield '<div class="text">Твоя возможность проявить себя!</div>'
	yield '</div>'
	yield '<div class="text">Тебя ждут задачи из самых разных областей математики:  Головоломки, Логика, Комбинаторика, Арифметика, Геометрия</div>'
	yield f'<a href={link}>'
	yield '<div class="start_button"> Открыть турнир </div>'
	yield '</a>'
	yield '</div>'
	yield '</div>'

	tournament_history = [
		{'event_name': 'Старт Турнира 1', 'event_date': '05.12.2023'},
		{'event_name': 'Финиш Турнира 1', 'event_date': '31.03.2024'},
		{'event_name': 'Старт Турнира 2', 'event_date': '24.02.2024'},
		{'event_name': 'Финиш Турнира 2', 'event_date': '31.03.2024'},
		{'event_name': 'Старт Турнира 3', 'event_date': '22.04.2024'},
		{'event_name': 'Финиш Турнира 3', 'event_date': '15.06.2024'}
		]
	tournament_amount = len(tournament_history)

	yield '<div class="history">'
	yield '<div class="content">'
	
	for tournament_ind in range(tournament_amount - 4, tournament_amount):
		yield '<div class="item">'
		yield '<div class="text_cont">'
		yield f'<div class="header"> {tournament_history[tournament_ind]["event_date"]} </div>'
		yield f'<div class="text"> {tournament_history[tournament_ind]["event_name"]} </div>'
		yield '</div>'
		yield '<div class="rect"> </div>'
		yield '</div>'

	yield '</div>'
	yield '<hr size="2" color="white" noshade />'
	yield '</div>'
	yield '</div>'

	yield '<div class="info_container">'
	yield '<div class="page_header">О турнире</div>'
	yield '<div class="content">'

	yield '<div class="content_row">'
	yield '<div class="content_box">'
	yield '<img class="icon" loading="lazy" src="/static/design/icons/screen.svg" />'
	yield '<div>'
	yield '<span class="bold_text"> Многие задачи интерактивны <br/></span>'
	yield '<span class="text"> <br/>Для их решения потребуется компьютер с мышкой или тачпадом, чтобы перетаскивать объекты и выделять клетки</span>'
	yield '</div>'
	yield '</div>'
	yield '<div class="content_box">'
	yield '<img class="icon" loading="lazy" src="/static/design/icons/clock.svg" />'
	yield '<div>'
	yield '<span class="bold_text"> В турнире встречаются задачи разной сложности <br/> </span>'
	yield '<span class="text"> <br/> Для решения задач рекомендуем выделить примерно 60 - 90 минут </span>'
	yield '</div>'
	yield '</div>'
	yield '<div class="content_box">'
	yield '<img class="icon" loading="lazy" src="/static/design/icons/calendar.svg" />'
	yield '<div>'
	yield '<span class="bold_text"> Турнир проходит в течение месяца <br/> </span>'
	yield '<span class="text">  <br/>В любое время до закрытия турнира можно войти/зарегистрироваться и поучаствовать </span>'
	yield '</div>'
	yield '</div>'
	yield '</div>'

	yield '<div class="content_row">'
	yield '<div class="content_box">'
	yield '<img class="icon" loading="lazy" src="/static/design/icons/planet.svg" />'
	yield '<div>'
	yield '<span class="text"> Примерно </span>'
	yield '<span class="bold_text"> 1300 детей и взрослых из разных стран </span>'
	yield '<span class="text"> (Австралия, Болгария, Сербия, Россия, Казахстан, США, Белоруссия и других) поучаствовали в первом турнире </span>'
	yield '</div>'
	yield '</div>'
	yield '<div class="content_box">'
	yield '<img class="icon" loading="lazy" src="/static/design/icons/gift.svg" />'
	yield '<div>'
	yield '<span class="text"> Турнир индивидуальный и рассчитан на школьников 7-9 классов и младше. Победители по итогам сезона (несколько турниров) получат </span>'
	yield '<span class="bold_text">  призы от журнала "Квантик" </span>'
	yield '</div>'
	yield '</div>'
	yield '<div class="content_box">'
	yield '<img class="icon" loading="lazy" src="/static/design/icons/medal.svg" />'
	yield '<div>'
	yield '<span class="bold_text"> В зачёт идут 2 лучших результата из 4 <br/> </span>'
	yield '<span class="text"> <br/>Взрослые тоже могут участвовать, но в отдельном зачёте (с призами для победителей) </span>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'

	yield '<div class="examples_container">'

	yield '<div class="dialog answer" num="0">'
	yield '<div class="head">'
	yield '<div> Раздел участка </div>'
	yield '<div> <img class="cross" loading="lazy" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="body">'
	yield '<img class="ans" loading="lazy" src="/static/design/answer/fields.png" />'
	yield '</div>'
	yield '<div class="button solution"> Посмотреть решение </div>'
	yield '</div>'

	yield '<div class="dialog answer" num="1">'
	yield '<div class="head">'
	yield '<div> Кони-невидимки </div>'
	yield '<div> <img class="cross" loading="lazy" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="body">'
	yield '<span class="bold_text"> Ответ:</span> <span class="text"> 0 </span>'
	yield '</div>'
	yield '<div class="button solution"> Посмотреть решение </div>'
	yield '</div>'

	yield '<div class="dialog answer" num="2">'
	yield '<div class="head">'
	yield '<div> Как такое возможно? </div>'
	yield '<div> <img class="cross" loading="lazy" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="body">'
	yield '<span class="bold_text"> Ответ:</span> <span class="text"> 800 </span>'
	yield '</div>'
	yield '<div class="button solution"> Посмотреть решение </div>'
	yield '</div>'

	yield '<div class="dialog solution" num="0">'
	yield '<div class="head">'
	yield '<div> Раздел участка </div>'
	yield '<div> <img class="cross" loading="lazy" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="body">' 
	yield '''<iframe loading="lazy" width="560" height="315"
			src="https://www.youtube.com/embed/88lOJeuaHDw?enablejsapi=1"
			frameborder="0"  allowfullscreen></iframe>'''
	yield '</div>'
	yield '<div class="button answer"> Посмотреть ответ </div>'
	yield '</div>'

	yield '<div class="dialog solution" num="1">'
	yield '<div class="head">'
	yield '<div> Кони-невидимки </div>'
	yield '<div> <img class="cross" loading="lazy" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="body">' 
	yield '''<iframe loading="lazy" width="560" height="315"
			src="https://www.youtube.com/embed/vqlC9c2LTV4?enablejsapi=1" 
			frameborder="0" allowfullscreen></iframe>'''
	yield '</div>'
	yield '<div class="button answer"> Посмотреть ответ </div>'
	yield '</div>'
	
	yield '<div class="dialog solution" num="2">'
	yield '<div class="head">'
	yield '<div> Как такое возможно? </div>'
	yield '<img class="cross" loading="lazy" src="/static/design/icons/cross.svg" />'
	yield '</div>'
	yield '<div class="body">' 
	yield '''<iframe loading="lazy" width="560" height="315"
			src="https://www.youtube.com/embed/m7lA9CoOq_g?enablejsapi=1" 
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
	yield '<img class="image" loading="lazy" src="/static/design/problem_img/fields.png" />'
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
	yield '<span class="text"> На некоторых клетках доски 5×5 стоят невидимые шахматные кони, в каждой клетке не более одного. На некоторых клетках написали, сколько всего коней бьют данную клетку (см. рисунок). <br/><br/> </span>'
	yield '<span class="bold_text"> Какое целое число должно стоять в центре доски? </span>'
	yield '</div>'
	yield '</div>'
	yield '<img class="image" loading="lazy" src="/static/design/problem_img/invisible_horses.png" />'
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
	yield '<img class="image" loading="lazy" src="/static/design/problem_img/how_possible.png" />'
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

	yield '<div class="team_container">'
	yield '<div class="page_header">Авторы и команда</div>'
	yield '<div class="content">'

	yield '<div class="content_row">'
	yield '<div class="content_box">'
	yield '<img class="photo" loading="lazy" src="/static/design/photo/M_Evdokimov.png" />'
	yield '<div class="name"> Михаил Евдокимов </div>'
	yield '''<div> 
		Автор многих олимпиадных 
		задач по математике: Турнир 
		Городов, Московская олимпиада, 
		Всероссийская, Матпраздник и 
		других.<br/><br/>
		Автор книг «Сто граней 
		математики» и «От задачек к 
		задачам», один из авторов 
		журнала «Квантик».</div>'''
	yield '</div>'

	yield '<div class="content_box">'
	yield '<img class="photo" loading="lazy" src="/static/design/photo/A_Shapovalov.png" />'
	yield '<div class="name"> Александр Шаповалов </div>'
	yield '''<div> 
		Автор дюжины книг по 
		кружковой и олимпиадной 
		математике, автор около 1000 
		олимпиадных задач.<br/><br/>
		Преподаватель летних школ и 
		онлайн-кружков, ответственный 
		редактор серии «Школьные 
		математические кружки».</div>'''
	yield '</div>'

	yield '<div class="content_box">'
	yield '<img class="photo" loading="lazy" src="/static/design/photo/A_Gribalco.png" />'
	yield '<div class="name"> Александр Грибалко </div>'
	yield '''<div> 
		Автор многих олимпиадных 
		задач по математике: Турнир 
		Городов, Московская олимпиада, 
		Матпраздник и других.<br/><br/>
		Председатель жюри турнира 
		математических боев имени 
		А.П. Савина. Автор трех книг
		по материалам турнира.</div>'''
	yield '</div>'
	yield '</div>'

	yield '<div class="content_row">'
	yield '<div class="content_box">'
	yield '<img class="photo" loading="lazy" src="/static/design/photo/E_Bakaev.png" />'
	yield '<div class="name"> Егор Бакаев </div>'
	yield '''<div> 
		Автор многих олимпиадных 
		задач по математике: Турнир 
		Городов, Московская олимпиада, 
		Всероссийская, Матпраздник и других олимпиад.<br/><br/>
		Преподаватель кружков
		по олимпиадной математике 
		в ведущих школах Москвы. 
		Редактор журнала “Квант”.</div>'''
	yield '</div>'

	yield '<div class="content_box">'
	yield '<img class="photo" loading="lazy" src="/static/design/photo/B_Butyrin.png" />'
	yield '<div class="name"> Богдан Бутырин </div>'
	yield '''<div> 
		Автор олимпиадных задач 
		по математике: Турнир Городов, 
		Московская олимпиада. Призёр 
		Всероссийской олимпиады.<br/><br/>
		Автор Youtube-канала
		MathOlymp, студент ФКН ВШЭ.</div>'''
	yield '</div>'

	yield '<div class="content_box">'
	yield '<div class="list">'
	yield '<div class="par">'
	yield '<div class="header"> Редакторы: </div>'
	yield '<div class="body"> С. Дориченко, <br/> Г. Мерзон, <br/> Т. Корчемкина, <br/> М. Прасолов </div>'
	yield '</div>'

	yield '<div class="par">'
	yield '<div class="header"> IT: </div>'
	yield '<div class="body"> Д. Чертоляс, <br/> В. Аксенов, <br/> Д. Миронов, <br/> В. Лобачевский </div>'
	yield '</div>'

	yield '<div class="par">'
	yield '<div class="header"> Дизайнер: </div>'
	yield '<div class="body"> А. Москаленко </div>'
	yield '</div>'

	yield '<div class="par">'
	yield '<div class="header"> Художник: </div>'
	yield '<div class="body"> А. Вайнер </div>'
	yield '</div>'

	yield '</div>'
	yield '</div>'

	yield '</div>'
	yield '</div>'
	yield '</div>'


	yield from footer.display_starter()

	yield '</div>'
	yield from footer.display_basement()
	yield '<script type="text/javascript" src ="/static/design/start_page.js"></script>'
