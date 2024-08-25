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

@route('/api/xhr', method='POST')
def get_xhr_request(db):
	print('xhr_request', file=sys.stderr)
	resp = {
		'status': False,
		'xhr_answer': None,
	}
	try:
		var_id = json.loads(request.body.read())['variant']
		params = json.loads(request.body.read())['xhr_params']
	except:
		return json.dumps(resp)
	
	token_status = check_token(request)
	if token_status['error']:
		return json.dumps(resp)
	user_id = token_status['user_id']
	
	print('var_id: ', var_id, file=sys.stderr)
	#print(xhr_request(db, user_id, var_id, params), file=sys.stderr)
	resp['xhr_answer'] = xhr_request(db, user_id, var_id, params)
	print(resp['xhr_answer'], file=sys.stderr)
	resp['status'] = True
	return json.dumps(resp)


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
			db.execute('update Kvantland.AvailableProblem set hint_taken=True where student=%s and variant=%s', (user_id, variant, ))
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
		resp['breadcrumbs'].append({'name': town_name, 'link': f'/town/{town}'})
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
			'componentType': "",
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
		(town, town_name, type_, name, db_description, image, points, content, hint, hint_cost), = db.fetchall()
		try:
			typedesc = import_module(f'problem-types.{type_}')
			description = typedesc.description(content)
		except:
			description = db_description
		print('description:', description)
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
	if image:
		resp['problem']['image'] = f'/old-problem_assets/integer_img/{image}'
	resp['problem']['cost'] = f'{points} {lang_form(points)}'
	resp['problem']['type'] = type_
	if 'correct' in content.keys(): # пользователь не должен знать ответ)
		del content['correct']
	print(content, file=sys.stderr)
	resp['problem']['variantParams'] = content

	db.execute('select hint_taken from Kvantland.AvailableProblem where variant = %s and student = %s', (variant, user_id))
	(hint_taken, ), = db.fetchall()
	print('hint_taken', hint_taken, file=sys.stderr)
	resp['problem']['hint']['status'] = not(hint_taken) and hint
	resp['problem']['hint']['cost'] = hint_cost
	if hint_taken:
		resp['problem']['hint']['description'] = hint
	
	try:
		typedesc.entry_form()
		isNewProblem = False
	except:
		isNewProblem = True
		
	if isNewProblem:
		if type_ == 'integer':
			resp['problem']['inputType'] = 'IntegerTypeInput'
		if type_ == 'radio':
			resp['problem']['inputType'] = 'InteractiveTypeInput'
			resp['problem']['componentType'] = 'radio'
		if 'inputType' in content.keys():
			resp['problem']['inputType'] = content['inputType']
		if 'componentType' in content.keys():
			resp['problem']['componentType'] = content['componentType']
		# print('newProblemData: ', resp, file=sys.stderr)
		resp['status'] = True
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
		solution = data['solution']
	except:
		return json.dumps(resp)
	
	db.execute('select Kvantland.Type_.code, content from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (variant,))
	(type_, content), = db.fetchall()
	db.execute('select curr, answer_given from Kvantland.AvailableProblem where variant = %s and student = %s', (variant, user_id))
	(curr, answer_given, ), = db.fetchall()
	if curr:
		content = curr
		
	if answer_given:
		return json.dumps(resp)
	print(type_, file=sys.stderr)
	print(content, file=sys.stderr)
	typedesc = import_module(f'problem-types.{type_}')
	print(answer, file=sys.stderr)
	is_answer_correct = typedesc.validate(content, answer)
	
	try:
		if isinstance(answer, str):
			answer_to_str = answer
		else:
			answer_to_str = json.dumps(answer)
	except:
		answer_to_str = ''
	
	db.execute('update Kvantland.AvailableProblem set answer_true=%s, answer=%s, solution=%s where variant = %s and student = %s', (is_answer_correct, answer_to_str, solution, variant, user_id))
	if is_answer_correct:
		db.execute('update Kvantland.Student set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s', (variant, user_id))
		db.execute('update Kvantland.Score set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s and tournament = %s', (variant, user_id, config["tournament"]["version"]))

	resp['status'] = True
	return json.dumps(resp)

	

MODE = config['tournament']['mode']


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
