from config import config
import json
from bottle import route

@route('/api/agreement_pars')
def get_agreements_pars():
	pars = [
		"""На­сто­я­щим я со­гла­ша­юсь с тем, что про­чи­тал <a class="policy" href="/policy">По­ли­ти­ку 
            Конфиденциальности</a> и дал согласие на обработку моих 
            персональных данных: фамилия, имя, наименование и номер 
            школы, номер класса, город, e-mail и иных, указанных в <a href="/policy">Политике</a>, 
            в соответствии с её положени­я­ми.""",
			
        """Если мне меньше 14 лет,  я со­гла­ша­юсь с тем, что мои за­конные 
            пред­ста­ви­те­ли –  ро­ди­те­ли/усы­но­ви­те­ли/по­пе­чи­тель  прочитали 
            <a class="policy" href="/policy">По­ли­ти­ку Конфиденци­аль­но­сти</a> и дали согласие на обработку 
            моих персональных данных: фамилия, имя, наименование и 
            номер школы, номер класса, город, e-mail и иных, указанных в 
            Политике,  в соответствии с её положениями.""",
			
        f"""Я по­ни­маю, что могу ото­звать свое со­гла­сие в любой мо­мент по 
			адресу электронной почты <a href="mailto:{config['contacts']['support_email']}">
			{config['contacts']['support_email']}</a>""",
    ]
	return json.dumps(pars)
