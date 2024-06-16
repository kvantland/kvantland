from bottle import route

from config import config
from login import do_logout
import user

import footer

MODE = config['tournament']['mode']

@route('/policy')
def display_confidentiality(db):
	if MODE=='public':
		do_logout()
	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	yield f'<title>Квантландия</title>'
	yield '<link rel="icon" href="/static/design/icons/logo.svg">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/policy.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/footer.css">'
	yield '<script type="module" src="/static/design/user.js"></script>'
	yield from user.display_banner_policy(db)
	yield '<div class="content_wrapper">'
	yield '<div class="conf_content">'

	yield '<div class="header"> Политика конфиденциальности </div>'

	yield '<div class="par">'
	yield '<div class="header"> 1. Общие положения </div>'
	yield '<div class="content">'

	yield '''<div> 1. Настоящая Политика конфиденциальности составлена в соответствии с требованиями Федерального закона
				от 27.07.2006 № 152-ФЗ «О персональных данных» и определяет порядок обработки персональных данных
				Оператором и меры по обеспечению безопасности персональных данных. </div>'''

	yield '''<div> 2. Опе­ра­тор пер­со­наль­ных дан­ных ООО "Квантик", ИНН 7728344440 (далее – Опе­ра­тор) ста­вит важ­ней­шей 
				целью и усло­ви­ем осу­ществ­ле­ния своей де­я­тель­но­сти со­блю­де­ние прав и сво­бод че­ло­ве­ка и граж­да­ни­на при 
				об­ра­бот­ке его пер­со­наль­ных дан­ных, в том числе за­щи­ты прав на не­при­кос­но­вен­ность част­ной жизни, 
				личную и се­мей­ную тайну. </div>'''

	yield '''<div> 3. Настоящая Политика конфиденциальности Оператора применяется ко всей информации, которую Оператор 
				может получить о посетителях веб-сайта, размещенного в сети «Интернет» по адресу: <a href="https://www.kvantland.com"> https://
				www.kvantland.com</a></div>'''

	yield '</div>'
	yield '</div>'

	yield '<div class="par">'
	yield '<div class="header"> 2. Термины и понятия </div>'
	yield '<div class="content">'

	yield '''<div> 1. Персональные данные - любая информация, относящаяся к прямо или косвенно определенному 
				или определяемому физическому лицу (субъекту персональных данных); </div>'''

	yield '''<div> 2. Предоставление персональных данных – действия, направленные на раскрытие персональных данных 
				определенному лицу или определенному кругу лиц; </div>'''

	yield '''<div> 3. Настоящая Политика конфиденциальности Оператора применяется ко всей информации, которую Оператор 
				может получить о посетителях веб-сайта, размещенного в сети «Интернет» по адресу: <a href="https://www.kvantland.com"> https://
				www.kvantland.com</a></div>'''

	yield '''<div> 4. Обработка персональных данных – любое действие (операция) или совокупность действий (операций), 
				совершаемых с использованием средств автоматизации или без использования таких средств с 
				персональными данными, включая сбор, запись, систематизацию, накопление, хранение, уточнение 
				(обновление, изменение), извлечение, использование, передачу (распространение, предоставление, доступ), 
				обезличивание, блокирование, удаление, уничтожение персональных данных; </div>'''

	yield '''<div> 5. Автоматизированная обработка персональных данных – обработка персональных данных с помощью средств 
				вычислительной техники; </div>'''

	yield '''<div> 6. Обезличивание персональных данных (уничтожение) – действия, в результате которых становится 
				невозможным определить принадлежность персональных данных конкретному субъекту персональных 
				данных;	</div>'''

	yield '''<div> 7. Все действия по использованию Сайта, включая отправку любых сообщений, содержащих персональные 
				данные Пользователя через формы на сайте, возможны исключительно при наличии его свободного согласия 
				на обработку персональных данных в порядке, описанном в Политике. </div>'''

	yield '''<div> 8. Отправляя свои персональные данные в форме обратной связи на сайте <a href="https://www.kvantland.com"> https://www.kvantland.com</a>, 
				Пользователь выражает согласие с условиями обработки персональных данных, предусмотренных 
				Политикой, и подтверждает, что: – он ознакомлен с Политикой, и данный документ ему понятен. </div>'''

	yield f'''<div> 9. Согласие Пользователя на обработку персональных данных может быть отозвано путем направления 
				заявления по электронному адресу <a href="mailto:{config["contacts"]["support_email"]}">support@kvantland.com</a>. Для осуществления отзыва согласия 
				Пользователь обязан указать фамилию, имя и адрес электронной почты. </div>'''

	yield '''<div> 10. Согласие на обработку персональных данных действует до достижения цели получения согласия, если иной 
				срок обработки не следует из требований законодательства РФ. </div>'''

	yield '''<div> 11. При несогласии с любым указанным в Политике положением Пользователь обязан отказаться от совершения 
				действий на Сайте, для которых требуется использование Оператором его персональных данных. </div>'''

	yield '</div>'
	yield '</div>'

	yield '<div class="par">'
	yield '<div class="header"> 3. Цели обработки персональных данных </div>'
	yield '<div class="content">'

	yield '''<div> 1. Оператор собирает данные, полученные от пользователей в процессе их регистрации и/или использования 
				Сайта, для исполнения соглашения между Пользователем и Оператором в отношении использования Сайта 
				Оператора для эффективного обслуживания пользователей и обеспечения лучшей производительности 
				Сайта. Оператор использует собираемые данные для предоставления пользователям интерактивных 
				возможностей, для разработки и совершенствования функционала Сайта, в том числе обновлений, 
				безопасности и устранения неполадок, а также предоставления поддержки. </div>'''

	yield '''<div> 2. Цели использования Cookie-файлов («куки»-файлов). Файлы сookie представляют собой небольшие текстовые 
				файлы, размещенные на устройстве для хранения данных, считываемые веб-сервером в домене, в котором 
				они были созданы. Сookie-файлы содержат сведения о действиях пользователя на сайте, дату и время сессии, 
				которые обрабатываются Оператором и используются для хранения и поддержки параметров выполнения 
				входа на Сайт, обеспечения пользовательских предпочтений, борьбы с мошенничеством, анализа работы 
				Сайта (в том числе с использованием метрических программ Яндекс.Метрика, Google Analytics). Пользователю 
				доступно множество средств для управления данными, собираемыми cookie-файлами. Например, можно 
				использовать элементы управления в веб-браузере для ограничения использования cookie-файлов веб-сайта
				ми и запрете их использования. </div>'''

	yield '</div>'
	yield '</div>'

	yield '<div class="par">'
	yield '<div class="header"> 4. Состав персональных данных </div>'
	yield '<div class="content">'

	yield '''<div> 1. Сведениями, составляющими персональные данные, является любая информация, относящаяся к прямо или 
				косвенно определенному или определяемому физическому лицу (субъекту персональных данных). </div>'''

	yield '''<div> 2. Вы предоставляете некоторые из этих данных непосредственно, например, когда создаете учетную запись 
				(личный кабинет), восстанавливаете пароль от личного кабинета по e-mail, отвечаете на вопросы и задания, 
				размещенные на Сайте, отправляете поисковой запрос на Сайте, загружаете контент или же обращаетесь за 
				поддержкой. Также без ваших персональных данных не обойтись при определении победителей в турнире и 
				награждении победителей. </div>'''

	yield '''<div> 3. В объем собираемых данных могут входить следующие: фамилия, имя, наименование и номер школы, номер 
				класса, город; пароли, подсказки по паролям и другие данные, относящиеся к безопасности и используемые 
				для проверки подлинности и доступа к учетным записям; данные, которые вы предоставляете, чтобы 
				использовать Сайт: например, поисковые запросы, вводимые вами в поля поиска; информацию файлов 
				cookies: в том числе, данные об операционной системе, браузере, языковых параметрах, ip-адресе, 
				проведенное на Сайте время, посещенные страницы и аналогичные; сообщения и содержимое файлов 
				(текстовых, графических, аудиовизуальных), которые вы вводите, загружаете, отправляете, получаете, создаете 
				и контролируете посредством Сайта. </div>'''

	yield '</div>'
	yield '</div>'

	yield '<div class="par">'
	yield '<div class="header"> 5. Порядок обработки персональных данных </div>'
	yield '<div class="content">'

	yield '''<div> 1. Обработка персональных данных осуществляется на основе принципов законности целей и способов 
				обработки персональных данных, добросовестности, соответствия целей обработки персональных данных 
				целям, заранее определенным и заявленным при сборе персональных данных, соответствия объема и 
				характера обрабатываемых персональных данных, способов обработки персональных данных целям 
				обработки персональных данных. </div>'''

	yield '''<div> 2. Персональные данные пользователей хранятся исключительно на электронных носителях и обрабатываются 
				с использованием автоматизированных систем, за исключением случаев, когда неавтоматизированная 
				обработка персональных данных необходима в связи с исполнением требований законодательства. </div>'''

	yield '''<div> 3. Персональные данные Пользователей не передаются каким-либо третьим лицам. Предоставление 
				персональных данных пользователей по запросу государственных органов или органов местного самоуправ
				ления осуществляется в порядке, предусмотренном законодательством. </div>'''

	yield f'''<div> 4. Персональные данные пользователя уничтожаются при: удалении Оператором Аккаунта пользователя по его 
				запросу на электронную почту <a href="mailto:{config["contacts"]["support_email"]}">support@kvantland.com</a>. </div>'''

	yield '''<div> 5. Оператор оставляет за собой право в автоматическом режиме удалять данные пользователя по истечении 
				одного календарного года со дня последнего посещения пользователем Сайта Оператора. </div>'''

	yield '</div>'
	yield '</div>'

	yield '<div class="par">'
	yield '<div class="header"> 6. Меры по защите персональных данных </div>'
	yield '<div class="content">'

	yield '''<div> 1. Оператор принимает технические и организационно-правовые меры в целях обеспечения защиты 
				персональных данных Пользователя от неправомерного или случайного доступа к ним, уничтожения, 
				изменения, блокирования, копирования, распространения, а также от иных неправомерных действий </div>'''

	yield '''<div> 2. Оператор определяет угрозы безопасности персональных данных при их обработке, формирует на их основе 
				модели угроз; осуществляет разработку системы защиты персональных данных, обеспечивающей 
				нейтрализацию предполагаемых угроз с использованием методов и способов защиты персональных данных; 
				осуществляет установку и ввод в эксплуатацию средств защиты информации. </div>'''

	yield '''<div> 3. Оператор проводит технические мероприятия, направленные на предотвращение несанкционированного 
				доступа к персональным данным; защитные инструменты настроены на своевременное обнаружение фактов 
				несанкционированного доступа к персональным данным; технические средства автоматизированной 
				обработки персональных данных изолированы в целях недопущения воздействия на них, в результате 
				которого может быть нарушено их функционирование; Оператор производит резервное копирование 
				данных, с тем, чтобы иметь возможность незамедлительного восстановления персональных данных, 
				модифицированных или уничтоженных вследствие несанкционированного доступа к ним; осуществляет 
				постоянный контроль за обеспечением уровня защищенности персональных данных. </div>'''

	yield '''<div> 4. Для разработки и осуществления мероприятий по обеспечению безопасности персональных данных при их 
				обработке Оператором, им могут привлекаться специалисты в области защиты данных. С соблюдением всех 
				требования законодательства Оператор может предоставить доступ к персональным данным Пользователя 
				тем специалистам, которым эта информация необходима для обеспечения функционирования Сайта и 
				предоставления Пользователю доступа к его использованию. </div>'''

	yield '</div>'
	yield '</div>'

	yield '<div class="par">'
	yield '<div class="header"> 7. Права и обязанности оператора и субъекта персональных данных </div>'
	yield '<div class="content">'

	yield '''<div> 1. Оператор персональных данных вправе предоставлять персональные данные субъектов третьим лицам, если 
				это предусмотрено действующим законодательством (правоохранительным органам, судебным органам и 
				др.); использовать персональные данные субъекта без его согласия, в случаях предусмотренных 
				законодательством; отказывать в предоставлении персональных данных в случаях, предусмотренных 
				законодательством. </div>'''

	yield '''<div> 2. Субъект персональных данных имеет право требовать уточнения своих персональных данных, их 
				блокирования или уничтожения; требовать перечень своих персональных данных, обрабатываемых 
				Оператором; получать информацию о сроках обработки своих персональных данных, в том числе о сроках их 
				хранения. </div>'''

	yield '</div>'
	yield '</div>'

	yield '<div class="par">'
	yield '<div class="header"> 8. Заключительные положения </div>'
	yield '<div class="content">'

	yield '''<div> 1. Настоящая Политика подлежит изменению или дополнению в случае появления новых законодательных 
				актов и специальных нормативных документов по обработке и защите персональных данных. </div>'''

	yield '''<div> 2. Актуальная версия Политики расположена в свободном доступе в сети Интернет по адресу <a href="https://www.kvantland.com/policy"> https://
				kvantland.com/policy</a>. </div>'''

	yield f'''<div> 3. Все вопросы Пользователей по поводу настоящей Политики, а также запросы на уточнение, блокирование 
				или уничтожение их персональных данных они вправе направлять оператору по адресу электронной почты: 
				<a href="mailto:{config["contacts"]["support_email"]}">support@kvantland.com</a>. </div>'''

	yield '</div>'
	yield '</div>'

	yield '</div>'
	yield '</div>'
	yield from footer.display_basement()
	yield '<script type="text/javascript" src="/static/design/user.js"></script>'