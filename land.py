#!/usr/bin/python3

from config import config
from bottle import route, redirect

import nav
import user
import footer

def lang_form(score):
	if score % 100 >= 10 and score % 100 < 20:
		return 'квантиков'
	else:
		if score % 10 in [2, 3, 4]:
			return 'квантика'
		elif score % 10 == 1:
			return 'квантик'
		else:
			return 'квантиков'

def finished(db, user_id):
	if user_id == None:
		return False
	db.execute('select is_finished from Kvantland.Student where student=%s', (user_id, ))
	(finish, ), = db.fetchall()
	return finish

def require_user(db):
	user_id = user.current_user(db)
	if user_id:
		db.execute('select * from Kvantland.Student where student = %s', (user_id, ))
		(stats), = db.fetchall()
		if None in stats:
			return None
	return user_id

@route('/land')
def show_land(db):
	user_id = require_user(db)
	if not user_id:
		redirect('/acc?empty=1')
	if finished(db, user_id):
		redirect("/final_page")
	yield '<!DOCTYPE html>'
	yield '<html lang="ru" class="map">'
	yield f'<title>Квантландия</title>'
	yield '<link rel="icon" href="/static/design/icons/logo.svg">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/nav.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/land.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/footer.css">'
	yield '<script type="module" src="/static/design/user.js"></script>'
	yield from user.display_banner_tournament(db)
	yield '<div class="content_wrapper">'
	yield from nav.display_breadcrumbs(('/land', 'Квантландия'))
	yield '<svg class="map" version="1.1" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
	yield '<defs>'
	yield '<clipPath id="map_border">'
	yield '''<path d="
			M 0 20
			v 680
			a 20 20 0 0 0 20 20
			h 1240
			a 20 20 0 0 0 20 -20
			v -680
			a 20 20 0 0 0 -20 -20
			h -1240
			a 20 20 0 0 0 -20 20
			z" />'''
	yield '</clipPath>'

	yield '<clipPath id="icon_border">'
	yield '''<path d="
			M -30 0
			a 30 30 0 0 0 30 30 
			a 30 30 0 0 0 30 -30
			a 30 30 0 0 0 -30 -30
			a 30 30 0 0 0 -30 30
			z" />'''
	yield '</clipPath>'
	yield '<filter id="dropshadow" height="130%">'
	yield '<feGaussianBlur in="SourceAlpha" stdDeviation="3"/>'
	yield '<feOffset dx="2" dy="2" result="offsetblur"/>'
	yield '<feComponentTransfer>'
	yield '<feFuncA type="linear" slope="0.5"/>'
	yield '</feComponentTransfer>'
	yield '<feMerge>' 
	yield '<feMergeNode/>'
	yield '<feMergeNode in="SourceGraphic"/>'
	yield '</feMerge>'
	yield '</filter>'
	yield '</defs>'

	yield f'<image href="/static/map/land.png" width="1280" height="720" preserveAspectRatio="xMinYMin" clip-path="url(#map_border)" meet/>'
	if user_id is not None:
		db.execute('select town, name, position, exists(select 1 from Kvantland.AvailableProblem join Kvantland.Variant using (variant) join Kvantland.Problem using (problem) where town = Kvantland.Town.town and student = %s and answer_given = false and tournament = %s) from Kvantland.Town', (user_id, config["tournament"]["version"]))
	else:
		db.execute('select town, name, position, true from Kvantland.Town')

	paths = [
	'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 154.96492919921874 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -154.96492919921874 a 6 6 0 0 0 -6 6 z',
	'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 230.9311767578125 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -230.9311767578125 a 6 6 0 0 0 -6 6 z',
	'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 183.9388214111328 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -183.9388214111328 a 6 6 0 0 0 -6 6 z',
	'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 92.43402252197265 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -92.43402252197265 a 6 6 0 0 0 -6 6 z',
	'm 0 6 v 21.72199043273926 a 6 6 0 0 0 6 6 h 265.24155578613284 a 6 6 0 0 0 6 -6 v -21.72199043273926 a 6 6 0 0 0 -6 -6 h -265.24155578613284 a 6 6 0 0 0 -6 6 z'
	]
	trans = [ 
	'-83.48246459960937 -76.86099521636963',
	'-121.46558837890625 -76.86099521636963',
	'-97.9694107055664 -76.86099521636963',
	'-52.217011260986325 -76.86099521636963',
	'-138.62077789306642 -76.86099521636963'
	]
	cnt = 0
	for town, name, (x, y), opened in db.fetchall():
		clazz = "town"
		if not opened:
			clazz += " town_completed"
		yield f'<a class="{clazz}" transform="translate({x} {y})" xlink:href="/town/{town}/">'
		yield f'<image href="/static/icon/icon-{town}.png" x="-40px" y ="-40px" width="80px" clip-path="url(#icon_border)" />'
		yield f'<circle class="town-icon" r="33px" />'
		yield f'<path class="town-name" num="{cnt}" d="{paths[cnt]}" transform="translate({trans[cnt]})" style="filter:url(#dropshadow)"/>'
		yield f'<text class="town-name" style="font-family:Montserrat Alternates" num="{cnt}" y="-60">{name}</text>'
		yield f'</a>'
		cnt += 1
	yield '</svg>'
	'''
	yield '<div class="contacts_block">'
	yield '<h2 class="contacts_header"> Контакты: </h2>'
	yield f'<p class="contact"> Техническая поддержка: <a href="mailto:{config["contacts"]["support_email"]}">{config["contacts"]["support_email"]}</a> </p>'
	yield '</div>'
	'''
	yield '</div>'
	yield from footer.display_basement()
	yield '<script type="module" src="/static/results.js"></script>'
	#yield '<script type="text/ecmascript" src="/static/design/land.js"></script>'

@route('/rules')
def show_land(db):
	user_id = require_user(db)
	if not user_id:
		redirect('/acc?empty=1')
	yield '<!DOCTYPE html>'
	yield '<html lang="ru">'  # TODO поместить в общий шаблон
	yield f'<title>Правила — Квантландия</title>'
	yield '<link rel="icon" href="/static/design/icons/logo.svg">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/nav.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/rules.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/footer.css">'
	yield '<script type="module" src="/static/design/user.js"></script>'
	#yield from user.display_banner(db)
	yield from user.display_banner_tournament(db)
	yield '<div class="content_wrapper">'
	yield from nav.display_breadcrumbs(('/land', 'Квантландия'), ('/rules', 'Правила'))
	yield '<div class="content_box">'
	yield '<div class="rules_box">'
	yield '<div class="header">Правила турнира</div>'
	yield '<div class="rules_content">'
	yield '<div class="rules_wrapper">'
	yield '<div class="span_position"><span class="span_text">Игрок путешествует по стране Квантландия, оказываясь в разных городах и областях (Головоломск, Остров Лжецов, Республика Комби, Чиселбург, Геома), и зарабатывает виртуальную валюту «квантик» за решение задач соответствующей темы: Головоломки, Логика, Комбинаторика, Арифметика, Геометрия. <br/><br/></span><span>Цель игры — получить как можно больше квантиков.</span></div>'
	yield '</div>'
	yield '<div class="rules_wrapper">'
	yield '<div class="span_position"><span class="span_text">В начале игры каждому дается 10 квантиков, которые можно тратить на подсказки к задачам. Для того чтобы получить задачу, нужно выбрать одну из монет в соответствующем городе или области (кликнуть на монету). На монете указывается количество квантиков, которое дается за ее правильное решение. <br/><br/></span><span>Есть задачи проще (1 или 2 квантика за решение) и сложнее (3 или 4 квантика за решение).</span></div>'
	yield '</div>'
	yield '<div class="span_wrapper"><span class="span_text">Можно свободно возвращаться к карте города или страны. Но если вы уже давали ответ на задачу, то задача становится неактивной и пройти ее повторно нельзя. <br/><br/></span><span>Поэтому не торопитесь и внимательно проверяйте, прежде чем отправить ответ. </span></div>'
	yield '<div class="span_wrapper"><span class="span_text">Обратите внимание, что некоторые задачи интерактивны. В них требуется произвести действия, которые описаны в условии, чтобы получить нужный результат. <br/><br/></span><span>Читайте условия внимательно! </span></div>'
	yield f'<div class="span_wrapper"><span class="span_text">Для решения задач вам понадобится компьютер и компьютерная мышь или ноутбук с тачпадом (не планшет), чтобы перетаскивать и выделять объекты. <br/><br/></span><span>Если возникла техническая проблема, то можно написать в техподдержку </span><u><a class="mail_link" href="mailto:{config["contacts"]["support_email"]}">{config["contacts"]["support_email"]}</a></u><span> с описанием проблемы и скриншотом компьютера.</span></div>'
	yield '<div class="span_wrapper span_text">Выберите время в течение месяца, чтобы вас ничего не отвлекало. Итоги соревнования подводятся по числу квантиков, которое у вас на счету к концу игры. Это число всегда отображается в правом вверху экрана. Удачи!</div>'
	yield '</div>'
	yield '<div class="conformation_box">'
	yield '<div class="conformation_wrapper">'
	yield '<div class="conformation_text">С правилами ознакомился(-лась) и готов(а) приступить!</div>'
	yield '<div class="start_button_border">'
	yield '<a href="/land">'
	yield '<div class ="start_button">'
	yield '<div class="start_button_text"> Открыть турнир </div>'
	yield '</div>'
	yield '</a>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	#yield from footer.display_footer()
	yield '</div>'	
	yield '</div>'
	yield from footer.display_basement()
