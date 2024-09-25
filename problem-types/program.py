from re import T
from urllib import response
from config import config
import urllib.request as urllib2
import urllib.parse
import datetime
import certifi
from urllib.error import HTTPError, URLError
import json
from bottle import request

token = config['ejudge']['token']
pending_status_list = ['RJ', 'AV', 'CG', 'CD', 'RU', '']
status_translate_list = {
	'0': "OK",  '1': "CE",  '2': "RT", 
	'3': "TL",  '4': "PE",  '5': "WA", 
	'6': "CF",  '7': "PT",  '8': "AC", 
	'9': "IG",  '10':"DQ",  '11':"PD",
	'12':"ML",  '13':"SE",  '14':"SV",
	'15':"WT",  '16':"PR",  '17':"RJ",
	'18':"SK",  '19':"SY",  '23':"SM",
	'95': " ",  '96':"RU",  '97':"CD",
	'98':"CG",  '99':"AV",  '22':"EM",
	'20':"VS",  '21':"VT",
}
print(token)

def steps(step_num, params, data):
	global token, pending_status_list
	apiUrl = config['ejudge']['clientUrl']
	print()
	print('=========================')
	print("problem of type 'program'")
	try:
		if params['type'] == 'send':
			if data['available_tries'] <= 0:
				return {'answer': {'message': "Попытки вышли", 'display': True}}
			if params['data']['text_input']:
				content = params['data']['text_input']
			elif params['files']['file_input']:
				content = params['files']['file_input'].file.read()
			else:
				return {'answer': {'message': "Пустая посылка!", 'display': True}}
			try:
				request_params = {
					'sender_user_login': config['ejudge']['user'],
					'lang_id': params['data']['lang'],
					'contest_id': config['ejudge']['contest_id'],
					'prob_id': data['prob_id'],
					'file': content,
				}
			except:
				return {'answer': {'message': "Неверный формат данных"}}
			sendUrl = apiUrl + '/submit-run'
			request = urllib2.Request(url=sendUrl, data=urllib.parse.urlencode(request_params).encode('utf-8'), 
						   headers={'Authorization': f'Bearer AQAA{token}', 'Content-Type': 'multipart/form-data'}, method='POST')
			try:
				cont = urllib2.urlopen(request)
			except HTTPError as e:
				return{'answer': {'message': f"HTTP Error: {e.code}"}}
			except URLError as e:
				return{'answer': {'message': f"URL Error: {e.reason}"}}
			except Exception as ex:
				return{'answer': {'message': f"Unknown Error: {ex}"}}
			response = json.loads(cont.read().decode('utf8').replace("'", '"'))
			print('send url: ', sendUrl, 'response:', response)
			
			run_id = response['result']['run_id']
			if 'run_list' not in data.keys():
				data['run_list'] = []
			data['run_list'].append({'id': run_id, 'data': get_status(run_id)})
			data['available_tries'] -= 1
			return {'answer': {'status': "successful request"}, 'data_update': data}
		elif params['type'] == 'update':
			try:
				if 'run_list' not in data.keys():
					return {'answer': {'message': "nothing to update"}}
				for elem_index in range(len(data['run_list'])):
					run = data['run_list'][elem_index]
					if run['data']['status'] in pending_status_list:
						updated_run = get_status(run['id'])
						print('after update: ', updated_run)
						data['run_list'][elem_index]['data'] = updated_run
				return {'answer': {'message': "successful request"}, 'data_update': data}
			except Exception as ex:
				return {'answer': {'message': ex}}

	except:
		return {'answer': {'message': "Неизвестная ошибка"}}
	

def get_test_status(test_list):
	try:
		time = 0
		status = '0'

		for test in test_list:
			time = max(time, test['time_ms'])
			if str(test['status']) == str(0):
				continue
			status = test['status']
			break
		return {'status': status, 'time': time}

	except:
		return {'status': None, 'time': 0}
	

def get_status(run_id):
	global token, status_translate_list
	apiUrl = config['ejudge']['clientUrl']
	request_params = {
		'contest_id': config['ejudge']['contest_id'],
		'run_id': run_id,
	}
	updateUrl = apiUrl + '/run-status-json'
	try:
		request = urllib2.Request(url=updateUrl + '?' + urllib.parse.urlencode(request_params), 
						   headers={'Authorization': f'Bearer AQAA{token}'}, method='GET')
		cont = urllib2.urlopen(request)
		full_response = json.loads(cont.read().decode('utf8').replace("'", '"'))
		run_response = full_response['result']['run']
		try:
			if 'testing_report' in full_response['result'].keys():
				if 'tests' in full_response['result']['testing_report'].keys():
					test_status = get_test_status(full_response['result']['testing_report']['tests'])
				else:
					test_status = {'status': run_response['status'], 'time': 0}
			else:
				test_status = {'status': run_response['status'], 'time': 0}
			status = status_translate_list[str(test_status['status'])]
			duration = test_status['time']
		except:
			status = 'CF'
			duration = 0
		try:
			size = run_response['size']
		except:
			size = ''
		try:
			tests_passed = run_response['passed_tests']
		except:
			tests_passed = 0
		try:
			submit_time =  run_response['run_time']
		except:
			submit_time = 0
		try:
			lang = run_response['lang_id']
		except:
			lang = 'Unknown'
		return {'status': status, 'duration': duration, 'size': size, 'tests_passed': tests_passed, 'submit_time': submit_time, 'lang': lang}
	except Exception as e:
		print(e)
		return {'status': '', 'duration': '', 'size': '', 'tests_passed': '???', 'submit_time': 0, 'lang': 'Unknown'}