from bottle import route
import json
from config import config
import problem


@route('/api/tournament_history')
def get_tournament_history():
	tournament_history = {}
	tournament_history['math'] = [
		{'event_name': 'Старт Турнира 1', 'event_date': '05.12.2023'},
		{'event_name': 'Финиш Турнира 1', 'event_date': '31.03.2024'},
		{'event_name': 'Старт Турнира 2', 'event_date': '24.02.2024'},
		{'event_name': 'Финиш Турнира 2', 'event_date': '31.03.2024'},
		{'event_name': 'Старт Турнира 3', 'event_date': '22.04.2024'},
		{'event_name': 'Финиш Турнира 3', 'event_date': '15.06.2024'},
		{'event_name': 'Старт Турнира 4', 'event_date': '08.08.2024'},
		{'event_name': 'Финиш Турнира 4', 'event_date': '09.09.2024'},
		]
	tournament_history['IT'] = [
		{'event_name': 'Старт Турнира 1', 'event_date': '25.10.2024'},
		{'event_name': 'Финиш Турнира 1', 'event_date': '30.11.2024'}
	]
	tournament_type = config['tournament']['type']
	events_amount = 4
	first_event = max(0, len(tournament_history[tournament_type]) - events_amount)
	return json.dumps(tournament_history[tournament_type][first_event:])


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
	problem_examples = {}
	problem_examples['math'] = [
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
	problem_examples['IT'] = [
			{
				'title': "Змейка",
				'desc': """<div style="display: flex; flex-direction: column; gap: 10px;"> 
						<p>Вам дана таблица размера \\(K \\times L\\). Обходя таблицу по змейке, 
						впишите в нее строку (см. пример). </p>
						<p><b>Входные данные.</b> </p>
						<p>На первой строке вводятся натуральные числа \\(K\\) и \\(L\\) \\((1 \\leq K \\cdot L \\leq 10^5)\\).
						Далее вводится строка длины \\(K \\cdot L\\).	</p>
						<p><b>Выходные данные.</b> </p>
						<p>Выведите \\(K\\) строк по \\(L\\) символов, разделенных пробелом.</p>
						<div style="display: grid; grid-template-columns: 1fr 1fr; width: 80%; background: black; column-gap: 1px; padding: 1px;">
							<div style="padding: 10px; background: white"> 
								<p> 3 3 </p>
								<p> kvantland </p>
							</div>
							<div style="padding: 10px; background: white"> 
								<p> k v a </p>
								<p> l t n </p>
								<p> a n d </p>
							</div>
						</div>
						</div>
						""",
				'cost': "2 квантика",
				'image': "IT_1.png",
			},
			{
			'title': 'Игра с компьютером',
			'desc': """Перед вами квадратное шахматное поле \\(10 \\times 10\\), некоторые клетки
			 		которого являюся запрещенными. В левом нижнем углу доски стоит король. 
					За один ход игрокам по очереди разрешается передвинуть короля на 1 клетку 
					либо вправо по горизонтали, либо вверх по вертикали, либо вправо-вверх по 
					диагонали, однако в запрещенные клетки ходить запрещено. Проигрывает тот, 
					кто не сможет сделать ход. Вы можете выбрать, ходить первым или вторым. 
					Напишите программу, которая выигрывает у компьютера!""",
			'cost': "3 квантика",
			'image': "IT_2.png"
			}
		]
		
	return json.dumps(problem_examples[config['tournament']['type']])


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
