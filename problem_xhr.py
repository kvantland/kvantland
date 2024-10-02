from copy import deepcopy
from bottle import request, route
from config import config
from login import check_token
from problem import get_problem_typedesc
import json
import sys


class ProblemResponse():
	def __init__(self, params: dict = {
				'user_answer': None, 
				'answer': '', 
				'solution': None, 
				'data_update': None, 
				'extra_points': 0, 
				'points_update': None, 
				'answer_correct': None
				}):
		self.answer = params.get('answer')
		self.user_answer = params.get('user_answer')
		self.answer_correct = params.get('answer_correct')
		self.solution = params.get('solution')
		self.data_update = params.get('data_update') # обновление текущих параметров задачи
		self.extra_points = params.get('extra_points') # добавление баллов к текущему счёту пользователя без изменения стоимости задачи
		self.points_update = params.get('points_update') # задание новой стоимости задачи
	
	def __str__(self):
		return '\n'.join([
			f'answer: {self.answer}', 
			f'user_answer: {self.user_answer[:40] if self.user_answer != None else None}...', 
			f'solution: {self.solution[0:40] if self.solution != None else None}...', 
			f'answer_coorect: {self.answer_correct}',
			f'data_update: {self.data_update}',
			f'extra points: {self.extra_points}',
			f'points_update: {self.points_update}'])
	

@route('/api/xhr', method='POST')
def get_xhr_request(db):
	print()
	print('===============================')
	print('xhr_request', file=sys.stderr)
	resp = {
		'status': False,
		'xhr_answer': None,
	}
	try:
		var_id = request.forms.get('variant')
		solution = request.forms.get('solution')
		params = json.loads(request.forms.get('xhr_params'))
		files = request.files
		params['files'] = files
		params['solution'] = solution
	except:
		return json.dumps(resp)
	
	token_status = check_token(request)
	if token_status['error']:
		return json.dumps(resp)
	user_id = token_status['user_id']
	
	print('var_id: ', var_id, file=sys.stderr)
	print('params: ', params)
	#print(xhr_request(db, user_id, var_id, params), file=sys.stderr)
	resp['xhr_answer'] = xhr_request(db, user_id, var_id, params)
	print(resp['xhr_answer'], file=sys.stderr)
	resp['status'] = True
	return json.dumps(resp)


def xhr_request(db, user_id, var_id, params):
	db.execute('update Kvantland.AvailableProblem set xhr_amount = xhr_amount + 1 where variant = %s and student = %s returning xhr_amount', (var_id, user_id))
	(xhr_amount, ), = db.fetchall()
	if (xhr_amount >= config['xhr']['dead_step']):
		raise Exception("Слишком много запросов!")
	db.execute('select Kvantland.Type_.code from Kvantland.Problem join Kvantland.Variant using (problem) join Kvantland.Type_ using (type_) where variant = %s', (var_id,))
	(type_, ), = db.fetchall()
	db.execute('select content from Kvantland.Variant where variant = %s', (var_id,))
	(start_cont, ), = db.fetchall()
	db.execute('select curr, curr_points from Kvantland.AvailableProblem where variant = %s and student = %s', (var_id, user_id))
	(curr, points, ), = db.fetchall()
	if curr:
		cont = deepcopy(curr)
		cont['default'] = start_cont
		cont['points'] = points
	else:
		cont = deepcopy(start_cont)
		cont['default'] = start_cont
		cont['points'] = points
	typedesc = get_problem_typedesc(type_)
	print()
	print('===========================')
	print('after xhr request')
	print()
	print('xhr_amount: ', xhr_amount)
	print('cont: ', cont)
	resp = typedesc.steps(xhr_amount, params, cont)
	resp = ProblemResponse(resp) if type(resp) == dict else resp
	print('resp: ', resp)
	try:
		if resp.points_update != None:
			db.execute('select curr_points from Kvantland.AvailableProblem where variant = %s and student= %s', (var_id, user_id))
			(current_points, ), = db.fetchall()
			print('points before update: ', current_points)
			new_points = current_points + resp.points_update
			if new_points > 0:
				db.execute('update Kvantland.AvailableProblem set curr_points = %s where variant = %s and student= %s', (new_points, var_id, user_id))
			else:
				resp.answer = {'message': "Невозможно совершить действие", 'display': True}
				return resp.answer
	except:
		pass

	try:
		if resp.extra_points:
			db.execute('update Kvantland.Student set score=score + %s where student = %s', (resp.extra_points, user_id))
			db.execute('update Kvantland.Score set score=score + %s where student = %s and tournament = %s', (resp.extra_points, user_id, config["tournament"]["version"]))
	except:
		pass

	if resp.data_update:
		db.execute('update Kvantland.AvailableProblem set curr = %s where variant = %s and student= %s', (json.dumps(resp.data_update), var_id, user_id))

	if resp.answer_correct != None:
		db.execute('update Kvantland.AvailableProblem set solution=%s where variant = %s and student = %s', (resp.solution, var_id, user_id))
		db.execute('update Kvantland.AvailableProblem set answer_true=%s, answer=%s where variant = %s and student = %s', (resp.answer_correct, resp.user_answer, var_id, user_id))
		partial_solution = 'partial_score' in cont.keys()
		print('partial solution given: ', partial_solution)
		if not partial_solution:
			db.execute('update Kvantland.Student set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) * %s where student = %s', (var_id, int(resp.answer_correct), user_id))
			db.execute('update Kvantland.Score set score=score + (select points from Kvantland.Variant join Kvantland.Problem using (problem) where variant = %s) where student = %s and tournament = %s', (var_id, user_id, config["tournament"]["version"]))
	
	return resp.answer

