from login import do_login, current_user
from bottle import route, request, response, redirect
from passlib.hash import pbkdf2_sha256 as pwhash
import nav
import json
from config import config
import urllib.request as urllib2
import urllib.parse

secret = config['reg']['secret']
reg_url = config['reg']['reg_url']

@route('/reg')
def reg_from():
  if current_user() != None:
    redirect('/')
  yield from display_registration_form()

def display_registration_form(err=None):
  yield '<!DOCTYPE html>'
  yield '<title> Регистрация — Квантландия </title>'
  yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
  if err:
    yield '<dialog open="open" class="reg_dialog">'
    if err[0] == 'r':
      yield '<p>К сожаление, пользователь с таким логином уже существует,</p>'
      yield '<p align="left">попробуйте другой логин. </p>'
    elif err[0] == 'c':
      yield '<p>Заполните капчу!</p>'
    else:
      yield '<p>Ошибка заполнения капчи</p>'
    yield '<form method="dialog">'
    yield '<button type="submit" class="dialog_button">Закрыть</button>'
    yield '</form>'
    yield '</dialog>'
  yield '<main>'
  yield from nav.display_breadcrumbs(('/', 'Квантландия'))
  yield '<div class="reg_form">'
  yield '<div class = "reg_form_header"> Регистрация </div>'
  yield '<form class="reg" method="post">'
  yield '<input name="login" type="text" placeholder="Логин" required />'
  yield '<input name="password" type="password" placeholder="Пароль" required />'
  yield '<input name="name" type="text" placeholder="Имя" required/>'
  yield '<input name="surname" type="text" placeholder="Фамилия" required/>'
  yield '<input name="school" type="text" placeholder="Школа" required/>'
  yield '<select name="clas" required>'
  yield '<option value="" disabled selected> Класс </option>'
  yield '<option> 1 </option>'
  yield '<option> 2 </option>'
  yield '<option> 3 </option>'
  yield '<option> 4 </option>'
  yield '<option> 5 </option>'
  yield '<option> 6 </option>'
  yield '<option> 7 </option>'
  yield '<option> 8 </option>'
  yield '<option> 9 </option>'
  yield '<option> 10 </option>'
  yield '<option> 11 </option>'
  yield '</select>'
  yield '<div class="g-recaptcha" data-sitekey="6LcWR2MoAAAAABz4UpMRZlmwmWZlvne32dKbc1Kx"></div>'
  yield '<button type="submit" class="reg_button"> Зарегистрироваться </button>'
  yield '</form>'
  yield '<div class="back_to_log">'
  yield '<a href="/login"> Уже зарегистрированы? </a>'
  yield '</div>'
  yield '</div>'
  yield '</main>'
  yield '<script type="text/javascript" src ="/static/registration.js"></script>'
  yield '<script src="https://www.google.com/recaptcha/api.js" async defer></script>'

def add_user(db, логин, пароль, имя, фамилия, школа, класс):
  db.execute("insert into Ученик (логин, пароль, имя, фамилия, школа, класс) values (%s, %s, %s, %s, %s, %s) returning ученик", (логин, pwhash.hash(пароль), имя, фамилия, школа, класс))
  (user, ), = db.fetchall()
  db.execute("insert into ДоступнаяЗадача (ученик, вариант) select distinct on (задача) %s, вариант from Вариант order by задача, random();", (user, ))
  return int(user)

def check_login(db, логин):
  db.execute("select ученик from Ученик where логин = %s", (логин,))
  try:
    (user,) = db.fetchall()
  except ValueError:
    return None
  return user

@route('/reg', method='POST')
def login_attempt(db):
  if len(request.forms['g-recaptcha-response']) != 0:
    params = {
    "secret": secret,
    "response": request.forms['g-recaptcha-response']
    }
    out = reg_url + '?' + urllib.parse.urlencode(params)
    cont = urllib2.urlopen(out)
    not_robot = json.loads(cont.read())['success']
    if not_robot:
      if check_login(db, request.forms.login):
        yield from display_registration_form('reg_error')
      else:
        user = add_user(db, request.forms.login, request.forms.password, request.forms.name, request.forms.surname, request.forms.school, request.forms.clas)
        do_login(user)
        redirect('/')
    else:
      yield from display_registration_form('not_human!')
  else:
    yield from display_registration_form('captcha_error')
  