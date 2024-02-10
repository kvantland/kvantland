from config import config

def display_confirm_window():
	yield '<div class="approv hidden">'
	yield '<div class="header">'
	yield '<div> Согласие на обработку персональных данных </div>'
	yield '<div class="cross"> <img class="cross" src="/static/design/icons/cross.svg" /> </div>'
	yield '</div>'
	yield '<div class="content">'
	yield '''<div class="par">
				На­сто­я­щим я со­гла­ша­юсь с тем, что про­чи­тал <a href="/policy">По­ли­ти­ку 
				Конфиденциальности</a> и дал согласие на обработку моих 
				персональных данных: фамилия, имя, наименование и номер 
				школы, номер класса, город, e-mail и иных, указанных в <a href="/policy">Политике</a>, 
				в соответствии с её положени­я­ми. </div>'''
	yield '''<div class="par"> 
				Если мне меньше 14 лет,  я со­гла­ша­юсь с тем, что мои за­конные 
				пред­ста­ви­те­ли –  ро­ди­те­ли/усы­но­ви­те­ли/по­пе­чи­тель  прочитали 
				<a href="/policy">По­ли­ти­ку Конфиденци­аль­но­сти</a> и дали согласие на обработку 
				моих персональных данных: фамилия, имя, наименование и 
				номер школы, номер класса, город, e-mail и иных, указанных в 
				Политике,  в соответствии с её положениями.</div>'''
	yield f'''<div class="par">
				Я по­ни­маю, что могу ото­звать свое со­гла­сие в любой мо­мент по 
				адресу электронной почты <a href="mailto:{config['contacts']['support_email']}">{config['contacts']['support_email']}</a>.</div>'''
	yield '</div>'
	yield '</div>'