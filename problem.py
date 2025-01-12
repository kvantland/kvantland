#!/usr/bin/python3
import sys

from bottle import route, request
import json
from importlib import import_module
from pathlib import Path
from copy import deepcopy

from config import config
from login import check_token

import urllib.request as urllib2
import urllib.parse
from urllib.error import HTTPError, URLError

relative_tournament_version = None

@route('/api/reset_problem', method="POST")
def reset_problem(db):
	print()
	print('========================')
	print('reset problem request')
	if not config['tournament']['test']:
		return 'not test mode'
	try:
		variant = json.loads(request.body.read())['variant']
	except:
		return 'no variant'
	
	db.execute("update Kvantland.AvailableProblem set answer='', solution='', answer_given=DEFAULT, answer_true=null, curr=null, curr_points=null where variant=%s", (variant, ))
	return 'success'


@route('/api/get_hint', method="POST")
def get_hint(db):
	print()
	print('==========================')
	print('get hint request')
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
		db.execute('select hint_taken from Kvantland.AvailableProblem where student=%s and variant=%s', (user_id, variant, ))
		(hint_taken, ), = db.fetchall()
		if hint_taken:
			return json.dumps(resp)
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


@route('/api/problem_data', method="POST")
def get_problem_data(db):
	print('========================')
	print('get problem data')
	print()
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
			'componentPath': "",
			'descriptionPath': "",
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

	set_relative_tournament_num(db)
	print(relative_tournament_version)

	is_answer_correct = get_past_answer_correctness(db, user_id, variant)
	if is_answer_correct is not None:
		resp['problem']['answerGiven'] = True
		resp['problem']['answerStatus'] = is_answer_correct
		db.execute('select answer, solution from Kvantland.AvailableProblem where variant = %s and student = %s', (variant, user_id))
		(answer, solution, ), = db.fetchall()
		resp['problem']['answer'] = answer
		resp['problem']['solution'] = solution

	try:
		db.execute('''select Kvantland.Type_.code, Kvantland.Problem.name, 
				description, image, points, Kvantland.Variant.content, Kvantland.Hint.content, Kvantland.Hint.cost 
				from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) join 
				Kvantland.Town using (town) left join Kvantland.Hint using (problem) where variant = %s''', (variant,))
		(type_, name, db_description, image, points, content, hint, hint_cost), = db.fetchall()
		db.execute('select xhr_amount, curr, curr_points, hint_taken from Kvantland.AvailableProblem where variant = %s and student = %s', (variant, user_id))
		(step, curr, curr_points, hint_taken), = db.fetchall()
	except:
		return json.dumps(resp)

	typedesc = get_problem_typedesc(type_)
	try:
		description = typedesc.description(content)
	except:
		description = db_description
	resp['problem']['description'] = description
	
	default = content
	if 'correct' in content.keys(): # пользователь не должен знать ответ)
		del content['correct']
	if curr:
		content = curr
	if curr_points:
		points = curr_points
	resp['problem']['variantParams'] = content
	resp['problem']['cost'] = f'{points} {lang_form(points)}'

	print('hint_taken: ', hint_taken, file=sys.stderr)
	resp['problem']['hint']['status'] = not(hint_taken) and bool(hint)
	resp['problem']['hint']['cost'] = hint_cost
	if hint_taken:
		resp['problem']['hint']['description'] = hint
	
	resp['problem']['title'] = name
	if image:
		resp['problem']['image'] = f'/old-problem_assets/integer_img/{image}'
	resp['problem']['type'] = type_
	
	try:
		typedesc.entry_form()
		isNewProblem = False
	except:
		isNewProblem = True
		
	if isNewProblem:
		print(resp['problem']['componentPath'])
		if type_ == 'integer':
			resp['problem']['inputType'] = 'IntegerTypeInput'
		if type_ == 'multy_integer':
			resp['problem']['inputType'] = 'MultyIntegerTypeInput'
		if type_ == 'radio':
			resp['problem']['inputType'] = 'InteractiveTypeInput'
			resp['problem']['componentPath'] = get_component_path('radio')
		if 'inputType' in content.keys():
			resp['problem']['inputType'] = content['inputType']
		if 'componentType' in content.keys():
			resp['problem']['componentPath'] = get_component_path(content['componentType'])
			resp['problem']['descriptionPath'] = get_description_path(content['componentType'])
		else:
			componentType = convert_to_camel_case(type_)
			print('component type: ', componentType)
			resp['problem']['componentPath'] = get_component_path(componentType)
			resp['problem']['descriptionPath'] = get_description_path(componentType)
		if 'descriptionType' in content.keys():
			resp['problem']['descriptionPath'] = get_description_path(content['descriptionType'])
		# print('newProblemData: ', resp, file=sys.stderr)
		resp['status'] = True
		return json.dumps(resp)
	
	kwargs = {'step': step, 'default': default}
	script = try_read_file(f'problem-types/{type_}.js') # надо в будущем написать функцию для получения валидного пути
	style = try_read_file(f'problem-types/{type_}.css') # надо в будущем написать функцию для получения валидного пути
	
	resp['problem']['problemHTML'] = ''.join(line for line in typedesc.entry_form(content, kwargs)).replace('/static', '').replace('problem_assets', 'old-problem_assets')
	if style:
		resp['problem']['problemCSS'] = f'/old-problem-types/{type_}.css'
	if script:
		resp['problem']['problemJS'] = f'/old-problem-types/{type_}.js'

	resp['problem']['inputType'] = get_old_problem_input_type(typedesc)

	# print('resp: ', resp, file=sys.stderr)
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
	
	try:
		classes = data['classes']
	except:
		classes = "all"
	
	db.execute('select Kvantland.Type_.code, content from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (variant,))
	(type_, content), = db.fetchall()
	db.execute('select curr, answer_given from Kvantland.AvailableProblem where variant = %s and student = %s', (variant, user_id))
	(curr, answer_given, ), = db.fetchall()
	if curr:
		content = curr
		
	if answer_given:
		return json.dumps(resp)
	print('type: ', type_, file=sys.stderr)
	typedesc = get_problem_typedesc(type_)
	print('answer: ', answer, file=sys.stderr)
	is_answer_correct = typedesc.validate(content, answer)
	
	try:
		if isinstance(answer, str):
			answer_to_str = answer
		else:
			answer_to_str = json.dumps(answer)
	except:
		answer_to_str = ''
	
	try:
		db.execute("select * from Kvantland.Score where student=%s and tournament=%s and classes=%s", 
						 (user_id, config["tournament"]["version"], classes))
	except:
		db.execute("insert into Kvantland.Score (student, tournament, classes) values (%s, %s, %s)", 
						 (user_id, config["tournament"]["version"], classes))
	db.execute('update Kvantland.AvailableProblem set answer_true=%s, answer=%s, solution=%s where variant = %s and student = %s', (is_answer_correct, answer_to_str, solution, variant, user_id))
	if is_answer_correct:
		db.execute('update Kvantland.Student set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s', (variant, user_id))
		db.execute('update Kvantland.Score set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s and tournament = %s and classes=%s', (variant, user_id, config["tournament"]["version"], classes))

	resp['status'] = True
	return json.dumps(resp)


@route('/api/program_available_languages', method="GET")
def get_languages():
	print('=======================')
	print('start getting languages')
	print()
	token = config['ejudge']['token']
	apiUrl = config['ejudge']['masterUrl']
	try:
		try:
			request_params = {
				'contest_id': config['ejudge']['contest_id'],
			}
		except:
			return json.dumps([])
		langUrl = apiUrl + '/list-languages'
		request = urllib2.Request(url=langUrl + '?' + urllib.parse.urlencode(request_params), 
						headers={'Authorization': f'Bearer AQAA{token}'}, method='GET')
		try:
			cont = urllib2.urlopen(request)
		except HTTPError as e:
			print(f"HTTP Error: {e.code}")
		except URLError as e:
			print(f"URL Error: {e.reason}")
		except Exception as ex:
			print(f"Unknown Error: {ex}")
		full_response = json.loads(cont.read().decode('utf8').replace("'", '"'))
		response_languages = full_response['languages']
		available_languages = []
		for language in response_languages.values():
			try:
				long_name = language['long_name']
			except:
				long_name = None
			try:
				short_name = language['short_name']
			except:
				short_name = None
			try:
				id = language['id']
			except:
				id = None
			available_languages.append({'shortName': short_name, 'longName': long_name, 'id': id})
		print('available languages:', available_languages)
		return json.dumps(available_languages)
	except:
		return json.dumps([])


MODE = config['tournament']['mode']


def choose_most_relevant_path(paths: list):
	most_relevant_path = None
	for path in paths:
		if try_read_file('/'.join(path)):
			most_relevant_path = path
	return most_relevant_path


def get_description_path(description_type: str):
	client_mode = config['client']['mode']
	if client_mode == 'dev':
		path_start = 'client/static/problemModules/'
	elif client_mode == 'prod':
		path_start = 'client/problemModules/'

	paths = [
		[
			path_start,
			f"{config['tournament']['type']}",
			f"season-{config['tournament']['season']}",
			f"tournament-{relative_tournament_version}",
			description_type,
			"description.vue"
		],
		[
			path_start,
			f"{config['tournament']['type']}",
			"common",
			description_type,
			"description.vue"
		],
		[
			path_start,
			"common",
			description_type,
			"description.vue"
		]
	]

	most_relevant_path = choose_most_relevant_path(paths)
	if most_relevant_path:
		return '/'.join(most_relevant_path[1:])
	return None


def get_component_path(component_type: str):
	client_mode = config['client']['mode']
	if client_mode == 'dev':
		path_start = 'client/static/problemModules/'
	elif client_mode == 'prod':
		path_start = 'client/problemModules/'

	paths = [
		[
			path_start,
			f"{config['tournament']['type']}",
			f"season-{config['tournament']['season']}",
			f"tournament-{relative_tournament_version}",
			component_type,
			f"{component_type}.vue"
		],
		[
			path_start,
			f"{config['tournament']['type']}",
			"common",
			component_type,
			f"{component_type}.vue"
		],
		[
			path_start,
			"common",
			component_type,
			f"{component_type}.vue"
		]
	]

	most_relevant_path = choose_most_relevant_path(paths)
	if most_relevant_path:
		return '/'.join(most_relevant_path[1:])
	return None


def get_problem_typedesc(problem_type: str):
	usual_problem_path = [
		"problem-types",
		f"{config['tournament']['type']}_problems",
		f"season_{config['tournament']['season']}",
		f"tournament_{relative_tournament_version}",
		problem_type,
	]
	try:
		usual_problem_typedesc = import_module('.'.join(usual_problem_path))
		print('usual_problem_path: ', '.'.join(usual_problem_path))
	except:
		usual_problem_typedesc = None
	common_for_tournament_problem_path = [
		"problem-types",
		f"{relative_tournament_version}_problems",
		"common_types",
		problem_type,
	]
	try:
		common_for_tournament_problem_typedesc = import_module('.'.join(common_for_tournament_problem_path))
		print('common_for_tournament_problem_path: ', '.'.join(common_for_tournament_problem_path))
	except:
		common_for_tournament_problem_typedesc = None
	common_problem_path = [
		"problem-types",
		"common_types",
		problem_type,
	]
	try:
		common_problem_typedesc = import_module('.'.join(common_problem_path))
		print('common_problem_path: ', common_problem_path)
	except:
		common_problem_typedesc = None
	typedesc = usual_problem_typedesc or common_for_tournament_problem_typedesc or common_problem_typedesc or None
	return typedesc


def convert_to_camel_case(name: str): 
	camel_version_of_name = ''.join(map(lambda str_path : str_path.capitalize(), name.split('_')))
	return camel_version_of_name[0].lower() + camel_version_of_name[1:]


def get_old_problem_input_type(typedesc):
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
			return 'HintOnlyInput'
		elif show_default_buttons and not(hybrid):
			return 'InteractiveTypeInput'
		else:
			return 'IntegerTypeInput'

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


def set_relative_tournament_num(db):
	global relative_tournament_version

	db.execute('select tournament from Kvantland.Season')
	tournaments = list(db.fetchall())
	relative_tournament_version = len(tournaments)
