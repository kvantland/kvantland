#!/usr/bin/python3
import sys 

from bottle import route, request, redirect, HTTPError, response
import json
from enum import Enum, auto
from importlib import import_module
from pathlib import Path
import psycopg

import nav
import user
import footer
from config import config
from login import do_logout, check_token


@route('/api/get_hint', method="POST")
def get_hint(db):
	resp = {
		'status': False,
		'hint': '',
	}
	try:
		variant = json.loads(request.body.read())['variant']
	except:
		return json.dumps(resp)

	token_status = check_token(request)
	if token_status['error']:
		return json.dumps(resp)
	user_id = token_status['user_id']
	
	try:
		db.execute('''select Kvantland.Hint.content, Kvantland.Hint.cost 
				from Kvantland.Problem join Kvantland.Variant using (problem)
			 	join Kvantland.Hint using (problem) where variant = %s''', (variant,))
		(hint, hint_cost, ), = db.fetchall()
		db.execute('select score from Kvantland.Student where student=%s', (user_id, ))
		(score, ), = db.fetchall()
		if score >= hint_cost:
			db.execute('update Kvantland.Student set score=%s where student=%s', (score - hint_cost, user_id, ))
			resp['hint'] = hint
	except:
		return json.dumps(resp)
	
	resp['status'] = True
	print('hint: ', resp, file=sys.stderr)
	return json.dumps(resp)



@route('/api/problem_breadcrumbs', method="POST")
def get_problem_breadcrumbs(db):
	resp = {
		'status': False,
		'breadcrumbs': [],
	}
	try:
		variant = json.loads(request.body.read())['variant']
	except:
		return json.dumps(resp)

	token_status = check_token(request)
	if token_status['error']:
		return json.dumps(resp)
	login = token_status['login']
	
	try:
		db.execute('''select town,  Kvantland.Town.name
				from Kvantland.Problem join Kvantland.Variant using (problem) join 
				Kvantland.Town using (town) where variant = %s''', (variant,))
		(town, town_name, ), = db.fetchall()
		resp['breadcrumbs'].append({'name': 'Квантландия', 'link': '/land'})
		resp['breadcrumbs'].append({'name': town_name, 'link': f'/land/town/{town}'})
	except:
		return json.dumps(resp)
	
	print('resp: ', resp, file=sys.stderr)
	resp['status'] = True
	return json.dumps(resp)


@route('/api/problem_data', method="POST")
def get_problem_data(db):
	resp = {
		'status': False,
		'problem':
		{
			'description': "",
			'title': "",
			'answer': "",
			'solution': "",
			'answerGiven': False,
			'answerStatus': None,
			'cost': "",
			'image': "",
			'type': "",
			'variantParams': "",
			'hint': {'status':"", 'cost':1, 'description': ''},
			'inputType': "",
			'problemComponent': "",
			'problemHTML': "",
			'problemCSS': "",
			'problemJS': "",
		}
	}
	try:
		variant = json.loads(request.body.read())['variant']
	except:
		return json.dumps(resp)

	token_status = check_token(request)
	if token_status['error']:
		return json.dumps(resp)
	user_id = token_status['user_id']

	is_answer_correct = get_past_answer_correctness(db, user_id, variant)
	if is_answer_correct is not None:
		resp['problem']['answerGiven'] = True
		resp['problem']['answerStatus'] = is_answer_correct
		db.execute('select answer, solution from Kvantland.AvailableProblem where variant = %s and student = %s', (variant, user_id))
		(answer, solution, ), = db.fetchall()
		resp['problem']['answer'] = answer
		resp['problem']['solution'] = solution
	
	try:
		db.execute('''select town, Kvantland.Town.name, Kvantland.Type_.code, Kvantland.Problem.name, 
				description, image, points, Kvantland.Variant.content, Kvantland.Hint.content, Kvantland.Hint.cost 
				from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) join 
				Kvantland.Town using (town) left join Kvantland.Hint using (problem) where variant = %s''', (variant,))
		(town, town_name, type_, name, description, image, points, content, hint, hint_cost), = db.fetchall()
		default = content
		db.execute('select xhr_amount, curr from Kvantland.AvailableProblem where variant = %s and student = %s', (variant, user_id))
		(step, curr, ), = db.fetchall()
		if curr:
			content = curr
	except:
		return json.dumps(resp)
	try:
		typedesc = import_module(f'problem-types.{type_}')
	except:
		typedesc = ''
	kwargs = {'step': step, 'default': default}
	script = try_read_file(f'problem-types/{type_}.js')
	style = try_read_file(f'problem-types/{type_}.css')
	
	resp['problem']['description'] = description
	resp['problem']['title'] = name
	resp['problem']['image'] = image
	resp['problem']['cost'] = f'{points} {lang_form(points)}'
	resp['problem']['type'] = type_
	resp['problem']['variantParams'] = content
	resp['problem']['hint']['status'] = bool(hint)
	resp['problem']['hint']['cost'] = hint_cost
	
	if not(typedesc):   # Задача нового типа
		if type_ == 'integer':
			resp['problem']['inputType'] = 'integerTypeInput'
		if content['inputType']:
			resp['problem']['inputType'] = content['inputType']
		if content['componentType']:
			resp['problem']['componentType'] = content['componentType']
		return json.dumps(resp)
	
	resp['problem']['problemHTML'] = ''.join(line for line in typedesc.entry_form(content, kwargs)).replace('/static', '').replace('problem_assets', 'old-problem_assets')
	if style:
		resp['problem']['problemCSS'] = f'/old-problem-types/{type_}.css'
	if script:
		resp['problem']['problemJS'] = f'/old-problem-types/{type_}.js'

	try:
		show_default_buttons = not typedesc.CUSTOM_BUTTONS
	except AttributeError:
		show_default_buttons = True

	try:
		hybrid = typedesc.HYBRID
	except AttributeError:
		hybrid = False

	try:
		without_buttons = typedesc.WITHOUT_BUTTONS
	except AttributeError:
		without_buttons = False

	try:
		hint_only = typedesc.HINT_ONLY
	except AttributeError:
		hint_only = False

	if not(without_buttons):
		if hint_only and not(hybrid):
			resp['problem']['inputType'] = 'HintOnlyInput'
		elif show_default_buttons and not(hybrid):
			resp['problem']['inputType'] = 'InteractiveTypeInput'
		else:
			resp['problem']['inputType'] = 'IntegerTypeInput'

	print('resp: ', resp, file=sys.stderr)
	resp['status'] = True
	return json.dumps(resp)


@route('/api/check_answer', method="POST")
def check_user_answer(db):
	resp = {
		'status': False,
	}
	
	access_token_status = check_token(request)
	if access_token_status['error']:
		return json.dumps(resp)
	user_id = access_token_status['user_id']
	
	try:
		data = json.loads(request.body.read())
		variant = data['variant']
		answer = data['answer']
	except:
		return json.dumps(resp)
	
	db.execute('select Kvantland.Type_.code, content from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (variant,))
	(type_, content), = db.fetchall()
	db.execute('select curr from Kvantland.AvailableProblem where variant = %s and student = %s', (variant, user_id))
	(curr, ), = db.fetchall()
	if curr:
		content = curr
	typedesc = import_module(f'problem-types.{type_}')
	is_answer_correct = typedesc.validate(content, answer)
	
	db.execute('update Kvantland.AvailableProblem set answer_true=%s, answer=%s where variant = %s and student = %s', (is_answer_correct, answer, variant, user_id))
	if is_answer_correct:
		db.execute('update Kvantland.Student set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s', (variant, user_id))
		db.execute('update Kvantland.Score set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s and tournament = %s', (variant, user_id, config["tournament"]["version"]))

	resp['status'] = True
	return json.dumps(resp)

	

MODE = config['tournament']['mode']
_key = config['keys']['cookie']

result_text = {
	True: 'Верно!',
	False: 'Неверно',
}

class HintMode(Enum):
	NONE = auto()
	SHOW = auto()
	AFFORDABLE = auto()
	TOO_EXPENSIVE = auto()

def try_read_file(path):
	path = Path(__file__).parent / path
	try:
		with open(path, 'r',encoding="utf-8") as f:
			return f.read()
	except OSError:
		return None

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

def show_answer_area(data, clas, kwargs, value='',):
	if clas == 'with_input':
		attrs = [
		'name="answer"',
		'type="number"',
		'required'
		]
		if lim := data.get('range'):
			if (a := lim.get('min')) != None:
				attrs.append(f'min="{a}"')
			if (b := lim.get('max')) != None:
				attrs.append(f'max="{b}"')
		attrs.append(f'value="{value}"')
		attrs = ' '.join(attrs)
		yield '<div class="answer_box space">'
		yield '<div class="input_zone">'
		yield '<div class="input_text">Введите ответ:</div>'
		yield f'<form method="post" id="problem_form" class="problem answer_zone">'
		yield f'<input class="answer_input" {attrs}/>'
		yield f'</form>'
		yield from show_submit_button(**kwargs)
		yield from show_hint_button(**kwargs)
		yield '</div>'
		yield '</div>'
	if clas == 'hint_only':
		yield '<div class="answer_box space">'
		yield '<div class="input_zone">'
		yield '</div>'
		yield from show_hint_button(**kwargs)
		yield '</div>'
	if clas == 'without_input':
		yield '<div class="answer_box space">'
		yield '<div class="input_zone">'
		yield from show_submit_button(**kwargs)
		yield from show_hint_button(**kwargs)
		yield '</div>'
		yield '</div>'

def show_submit_button(**kwargs):
	yield '<button class="submit_button button">'
	yield 'Отправить'
	yield '</div>'
	yield '</button>'

def show_hint_button(*, hint_mode: HintMode, hint_cost: int, **kwargs):
	if hint_mode == HintMode.AFFORDABLE:
		yield f'<button class="hint_box" title="Получить подсказку (стоимость: {hint_cost})">'
		yield '<img class="hint_icon" src="/static/design/icons/hint_icon.svg" />'
		yield '<div class="text">Подсказка</div>'
		yield '</button>'

def show_question(db, variant, hint_mode):
	step = 0
	if MODE == 'private':
		user_id = require_user(db)
		if user_id == None:
			redirect('/')
	elif MODE == 'public':
		do_logout()
		user_id = None
	db.execute('select town, Kvantland.Town.name, Kvantland.Type_.code, Kvantland.Problem.name, description, image, points, Kvantland.Variant.content, Kvantland.Hint.content, Kvantland.Hint.cost from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) join Kvantland.Town using (town) left join Kvantland.Hint using (problem) where variant = %s', (variant,))
	(town, town_name, type_, name, description, image, points, content, hint, hint_cost), = db.fetchall()
	default = content
	if MODE == 'private':
		db.execute('select xhr_amount, curr from Kvantland.AvailableProblem where variant = %s and student = %s', (variant, user_id))
		(step, curr, ), = db.fetchall()
		if curr:
			content = curr

	kwargs = {'hint_mode': hint_mode, 'hint_cost': hint_cost, 'step': step, 'default': default}
	typedesc = import_module(f'problem-types.{type_}')
	script = try_read_file(f'problem-types/{type_}.js')
	style = try_read_file(f'problem-types/{type_}.css')

	if MODE == 'public':
		HAS_STEPS = True
		try:
			typedesc.steps
		except AttributeError:
			HAS_STEPS = False
		if HAS_STEPS:
			redirect(f'/town/{town}/')

	try:
		save_progress = typedesc.SAVE_PROGRESS
	except AttributeError:
		save_progress = True

	try:
		show_default_buttons = not typedesc.CUSTOM_BUTTONS
	except AttributeError:
		show_default_buttons = True

	try:
		hybrid = typedesc.HYBRID
	except AttributeError:
		hybrid = False

	try:
		without_buttons = typedesc.WITHOUT_BUTTONS
	except AttributeError:
		without_buttons = False

	try:
		hint_only = typedesc.HINT_ONLY
	except AttributeError:
		hint_only = False

	yield '<!DOCTYPE html>'
	yield f'<title>{name}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/nav.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/footer.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/problem.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/confirm_action.css">'
	yield '<script src="/static/jQuery/jquery-3.7.1.js"></script>'
	yield '<script type="module" src="/static/master.js"></script>'
	yield '<script type="module" src="/static/design/user.js"></script>'
	if style:
		yield f'<style type="text/css">{style}</style>'
	yield from user.display_banner_tournament(db)
	yield '<div class="content_wrapper">'
	yield '<div class="content_box">'
	yield '<div class="problem_wrapper">'
	yield from nav.display_breadcrumbs(('/land', 'Квантландия'), (f'/town/{town}/', town_name))
	yield '<div class="problem_box">'
	yield '<div class="problem_desc">'
	yield '<div class="header">'
	yield f'<div class="header_text">{name}</div>'
	yield f'<div class="problem_cost">{points} {lang_form(points)}</div>'
	yield '</div>'
	yield '<div class="problem_desc_box">'
	yield f'<div class="problem_text"><span class="span_text">{description}</div>'
	if save_progress:
		if hybrid:
			yield f'<div id="interactive_problem_form">'
		else:
			yield f'<form method="post" id="problem_form" class="problem answer_area answer_area_{type_}">'
	yield from typedesc.entry_form(content, kwargs)
	if save_progress and not hybrid:
		yield '</form>'
	elif hybrid:
		yield '</div>'
	if image:
		yield f'<img class="picture" src="/static/problem_assets/integer_img/{image}">'
	if hint_mode == HintMode.SHOW:
		yield f'<div class="hint_wrapper">'
		yield f'<div class="header">'
		yield '<img class="hint_icon" src="/static/design/icons/hint_icon.svg" />'
		yield f'<div class="text_area">'
		yield f'<div class="text">Подсказка</div>'
		yield f'</div>'
		yield f'</div>'
		yield f'<div class="text_zone">'
		yield f'<div class="text">{hint}</div>'
		yield f'</div>'
		yield f'</div>'
	yield '</div>'
	if not without_buttons:
		if hint_only:
			yield from show_answer_area(content, 'hint_only', kwargs)
		elif show_default_buttons:
			yield from show_answer_area(content, 'without_input', kwargs)
		else:
			yield from show_answer_area(content, 'with_input', kwargs)
	yield '</div>'
	yield '</div>'
	yield from footer.display_problem()
	yield '</div>'
	yield '</div>'
	yield '</div>'

	if hint_cost:
		yield '<div class="hint_notification">'
		yield '<div class="text_area">'
		yield f'<div class="text">Подсказка стоит {hint_cost} {lang_form(hint_cost)}. <br/>Хотите воспользоваться?</div>'
		yield '</div>'
		yield '<div class="button_area">'
		yield '<div class="buttons">'
		yield '<button class="button notification_hint yes" form="hint" type="submit">'
		yield '<form id="hint" action="hint" method="post" class="hint">'
		yield '<div class="text">Да</div>'
		yield '</form>'
		yield '</button>'
		yield '<button class="button notification_hint no">'
		yield '<div class="text">Нет</div>'
		yield '</button>'
		yield '</div>'
		yield '</div>'
		yield '</div>'

	yield f'<div class="confirm_notification">'
	yield f'<div class="text_area">'
	yield f'<div class="text">Готовы отправить ответ? <br/>Изменить его позже будет нельзя!</div>'
	yield f'</div>'
	yield f'<div class="button_area">'
	yield f'<div class="buttons">'
	yield f'<button class="button notifcation_confirm yes" id="send" type="submit" form="problem_form">'
	yield f'<div class="text">Да</div>'
	yield f'</button>'
	yield f'<button class="button notifcation_confirm no">'
	yield f'<div class="text">Нет</div>'
	yield f'</button>'
	yield f'</div>'
	yield f'</div>'
	yield f'</div>'
	#
	yield '<div class="xhr_notification">'
	yield '<div class="header_area">'
	yield '<img class="warning_icon" src="/static/design/icons/warning.svg" />'
	yield '<div class="header_text">'
	yield '<div class="text">Обратите внимание</div>'
	yield '<div><img class="cross" src="/static/design/icons/cross.svg"></div>'
	yield '</div>'
	yield '</div>'
	yield '<div class="text_area">'
	yield '<div class="text">Больше нельзя делать взвешивания!</div>'
	yield '</div>'
	yield '</div> '
	yield from footer.display_basement()
	#
	if hint_mode == HintMode.SHOW:
		yield '<script type="text/ecmascript" src="/static/focus_on_hint.js"></script>'
	yield '<script type="text/ecmascript" src="/static/save_hint_results.js"></script>'
	yield '<script type="text/ecmascript" src="/static/design/xhr_dialog.js"></script>'
	yield '<script type="text/ecmascript" src="/static/confirm_action.js"></script>'
	if script:
		yield f'<script type="text/ecmascript">{script}</script>'

def check_answer(db, var_id, user_id, answer):
	db.execute('select Kvantland.Type_.code, content from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (var_id,))
	(type_, content), = db.fetchall()
	if MODE == 'private':
		db.execute('select curr from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
		(curr, ), = db.fetchall()
		if curr:
			content = curr
	typedesc = import_module(f'problem-types.{type_}')
	return typedesc.validate(content, answer)


def _display_result(db, var_id, answer_is_correct, answer=None, solution=None):
	db.execute('select Kvantland.Type_.code from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (var_id,))
	(type_, ), = db.fetchall()
	db.execute('select town, Kvantland.Town.name, Kvantland.Type_.code, Kvantland.Problem.name, description, image, points, Kvantland.Variant.content, Kvantland.Hint.content, Kvantland.Hint.cost from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) join Kvantland.Town using (town) left join Kvantland.Hint using (problem) where variant = %s', (var_id,))
	(town, town_name, type_, name, description, image, points, content, hint, hint_cost), = db.fetchall()
	
	typedesc = import_module(f'problem-types.{type_}')
	style = try_read_file(f'problem-types/{type_}.css')

	try:
		show_default_buttons = not typedesc.CUSTOM_BUTTONS
	except AttributeError:
		show_default_buttons = True

	try:
		save_progress = typedesc.SAVE_PROGRESS
	except AttributeError:
		save_progress = True

	try:
		hybrid = typedesc.HYBRID
	except AttributeError:
		hybrid = False

	yield '<!DOCTYPE html>'
	yield f'<title>{name}</title>'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/master.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/user.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/nav.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/footer.css">'
	yield '<link rel="stylesheet" type="text/css" href="/static/design/problem.css">'
	yield '<script type="module" src="/static/master.js"></script>'
	yield '<script type="module" src="/static/design/user.js"></script>'
	if style:
		yield f'<style type="text/css">{style}</style>'
	yield from user.display_banner_tournament(db)
	yield '<div class="content_wrapper">'
	yield '<div class="content_box">'
	yield '<div class="problem_wrapper">'
	yield from nav.display_breadcrumbs(('/land', 'Квантландия'), (f'/town/{town}/', town_name))
	yield '<div class="problem_box">'
	yield '<div class="problem_desc">'
	yield '<div class="header">'
	yield f'<div class="header_text">{name}</div>'
	yield f'<div class="problem_cost">{points} {lang_form(points)}</div>'
	yield '</div>'
	yield '<div class="problem_desc_box">'
	yield f'<div class="problem_text"><span class="span_text">{description}</div>'
	if save_progress:
		yield '<div class="solution_hide">'
		yield solution
		yield '</div>'
	if image:
		yield f'<img class="picture" src="/static/problem_assets/integer_img/{image}">'
	yield '</div>'
	yield '<div class="answer_box">'
	yield '<div class="result_box">'
	if answer_is_correct:
		yield f'<div class="result_text_true">{result_text[answer_is_correct]}</div>'
		if type_ == 'integer' or hybrid:
			yield f'<div>Ваш ответ: {answer}</div>'
	else:
		yield f'<div class="result_text_false">{result_text[answer_is_correct]}</div>'
		if type_ == 'integer' or hybrid:
			yield f'<div>Ваш ответ: {answer}</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield '</div>'
	yield from footer.display_problem()
	yield '</div>'
	yield '</div>'
	yield from footer.display_basement()
	yield '<script type="text/ecmascript" src="/static/focus_on_answer.js"></script>'

def require_user(db):
	user_id = user.current_user(db)
	if user_id:
		db.execute('select * from Kvantland.Student where student = %s', (user_id, ))
		(stats), = db.fetchall()
		if None in stats:
			return None
	return user_id

def has_current_problem(db, user):
	db.execute('select exists(select 1 from Kvantland.CurrentProblem where student = %s)', (user, ))
	(has, ), = db.fetchall()
	return has

def get_past_answer_correctness(db, user_id, var_id):
	db.execute('select answer_true from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
	try:
		(is_answer_correct, ), = db.fetchall()
	except ValueError:
		return None
	return is_answer_correct

def is_current_tournament(db, var_id):
	db.execute('select tournament from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s', (var_id,))
	tourn, = db.fetchall()
	return tourn[0] == config["tournament"]["version"]


@route('/problem/<var_id:int>/')
def problem_show(db, var_id):
	if not is_current_tournament(db, var_id):
		redirect('/')
	hint_mode = HintMode.NONE

	if MODE == 'public':
		do_logout()
		user_id = None
	elif MODE == 'private':
		user_id = require_user(db)
		if user_id == None:
			redirect('/')
		is_answer_correct = get_past_answer_correctness(db, user_id, var_id)
		if is_answer_correct is not None:
			db.execute('select answer, solution from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
			(answer, solution, ), = db.fetchall()
			print(answer, solution, file=sys.stderr)
			return _display_result(db, var_id, is_answer_correct, answer, solution)

		try:
			db.execute('select hint_taken from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
			(hinted, ), = db.fetchall()
		except ValueError:
			redirect('/')
		if hinted:
			hint_mode = HintMode.SHOW
		else:
			db.execute('select score >= cost from Kvantland.Hint join Kvantland.Variant using (problem), Kvantland.Student where variant = %s and student = %s', (var_id, user_id))
			try:
				(can_afford_hint, ), =db.fetchall()
				hint_mode = HintMode.AFFORDABLE if can_afford_hint else HintMode.TOO_EXPENSIVE
			except ValueError:
				hint_mode = HintMode.NONE
	
	return show_question(db, var_id, hint_mode)

@route('/problem/<var_id:int>/', method='POST')
def problem_answer(db, var_id):
	db.execute('select Kvantland.Type_.code from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (var_id,))
	type_ = db.fetchall()[0][0]
	
	if MODE == 'private':
		user_id = require_user(db)
		if user_id == None:
			redirect('/')
		is_answer_correct = get_past_answer_correctness(db, user_id, var_id)
		if is_answer_correct is not None:
			redirect('')
	elif MODE == 'public':
		do_logout()
		user_id = None

	answer = request.forms.answer
	solution = request.forms.progress

	typedesc = import_module(f'problem-types.{type_}')

	try:
		save_progress = typedesc.SAVE_PROGRESS
	except AttributeError:
		save_progress = True

	is_answer_correct = check_answer(db, var_id, user_id, answer)
	if MODE == 'private':
		if save_progress:
			db.execute('update Kvantland.AvailableProblem set answer_true=%s, solution=%s, answer=%s where variant = %s and student = %s', (is_answer_correct, solution, answer, var_id, user_id))
		else:
			db.execute('update Kvantland.AvailableProblem set answer_true=%s, answer=%s where variant = %s and student = %s', (is_answer_correct, answer, var_id, user_id))
		if is_answer_correct:
			db.execute('update Kvantland.Student set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s', (var_id, user_id))
			db.execute('update Kvantland.Score set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s and tournament = %s', (var_id, user_id, config["tournament"]["version"]))
	
	yield from _display_result(db, var_id, is_answer_correct, answer, solution)


def _request_hint(db, var_id):
	user_id = require_user(db)
	if user_id == None:
		redirect('/')
	is_answer_correct = get_past_answer_correctness(db, user_id, var_id)
	if is_answer_correct is not None:
		return

	db.execute('select hint_taken from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
	(hinted, ), = db.fetchall()
	if hinted:
		return

	db.execute('update Kvantland.AvailableProblem set hint_taken=true where variant = %s and student = %s', (var_id, user_id))
	try:
		db.execute('update Kvantland.Student set score=score - (select cost from Kvantland.Hint join Kvantland.Variant using (problem) where variant = %s) where student = %s', (var_id, user_id))
		db.execute('update Kvantland.Score set score=score - (select cost from Kvantland.Hint join Kvantland.Variant using (problem) where variant = %s) where student = %s and tournament = %s', (var_id, user_id, config["tournament"]["version"]))
	except psycopg.errors.CheckViolation:
		pass

@route('/problem/<var_id:int>/hint', method='POST')
def problem_request_hint(db, var_id):
	_request_hint(db, var_id)
	redirect('.')

def xhr_request(db, user_id, var_id, params):
	db.execute('update Kvantland.AvailableProblem set xhr_amount = xhr_amount + 1 where variant = %s and student = %s returning xhr_amount', (var_id, user_id))
	(xhr_amount, ), = db.fetchall()
	if (xhr_amount >= config['xhr']['dead_step']):
		raise Exception("Слишком много запросов!")
	db.execute('select Kvantland.Type_.code from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (var_id,))
	(type_, ), = db.fetchall()
	db.execute('select content from Kvantland.Variant where variant = %s', (var_id,))
	(cont, ), = db.fetchall()
	db.execute('select curr from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
	(curr, ), = db.fetchall()
	if curr:
		cont = curr
	typedesc = import_module(f'problem-types.{type_}')
	resp = typedesc.steps(xhr_amount, params, cont)
	try: 
		db.execute('update Kvantland.AvailableProblem set curr = %s where variant = %s and student= %s', (json.dumps(resp['data_update']), var_id, user_id))
	except KeyError:
		pass
	try: 
		db.execute('update Kvantland.AvailableProblem set answer_true=%s, answer=%s where variant = %s and student = %s', (resp['answer_correct'], resp['user_answer'], var_id, user_id))
		db.execute('update Kvantland.Student set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) * %s where student = %s', (var_id, int(resp['answer_correct']), user_id))
		db.execute('update Kvantland.Score set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s and tournament = %s', (var_id, user_id, config["tournament"]["version"]))
	except KeyError:
		pass
	try:
		db.execute('update Kvantland.AvailableProblem set solution=%s where variant = %s and student = %s', (resp['solution'], var_id, user_id))
	except KeyError:
		pass
	return resp['answer']


@route('/problem/<var_id:int>/xhr', method='GET')
def xhr_short(db, var_id):
	user_id = require_user(db)
	if user_id == None:
		redirect('/')
	params = request.query
	return xhr_request(db, user_id, var_id, params)

@route('/problem/<var_id:int>/xhr', method='POST')
def xhr_long(db, var_id):
	user_id = require_user(db)
	if user_id == None:
		redirect('/')
	params = json.loads(request.body.read())
	return xhr_request(db, user_id, var_id, params)
