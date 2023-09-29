from login import do_login, current_user
from bottle import route, request, response, redirect
import nav

@route('/reg')
def reg_from():
  if current_user() != None:
    redirect('/')
  yield from display_registration_form()

def display_registration_form():
  yield '<!DOCTYPE html>'
  yield '<title> Регистрация — Квантландия </title>'
  yield '<link rel="stylesheet" type="text/css" href="/static/master.css">'
  yield from nav.display_breadcrumbs(('/', 'Квантландия'))
  yield '<main>'
  yield '<div class="reg_form">'
  yield '<div class = "reg_form_header"> Регистрация </div>'
  yield '<form class="reg" method="post">'
  yield '<input name="login" type="text" placeholder="Логин" required />'
  yield '<input name="password" type="password" placeholder="Пароль" required />'
  yield '<input name="name" type="text" placeholder="Имя" />'
  yield '<input name="school" type="text" placeholder="Школа" />'
  yield '<input name="clas" type="text" placeholder="Класс" />'
  yield '<button type="submit" class="reg_button"> Зарегестрироваться </button>'
  yield '</form>'
  yield '<div class="back_to_log">'
  yield '<a href="/login"> Уже зарегестрированы? </a>'
  yield '</div>'
  yield '</div>'

def add_user(db, логин, пароль, имя, школа, класс):
  db.execute("insert into Ученик (логин, пароль, имя, школа, класс) values (%s, %s, %s, %s, %s) returning ученик", (логин, пароль, имя, школа, класс))
  (user, ), = db.fetchall()
  db.execute("insert into ДоступнаяЗадача (ученик, вариант) select distinct on (задача) %s, вариант from Вариант order by задача, random();", (user, ))
  return user

@route('/reg', method='POST')
def login_attempt(db):
  user = add_user(db, request.forms.login, request.forms.password, request.forms.name, request.forms.school, request.forms.clas)
  do_login(user)
  redirect('/')
  