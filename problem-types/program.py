from urllib import response
from config import config
import urllib.request as urllib2
import urllib.parse
import datetime
import certifi
from urllib.error import HTTPError, URLError
import json

token = config['ejudge']['token']
apiUrl = config['ejudge']['apiUrl']
print(token)

def steps(step_num, params, data):
	global token, apiUrl
	try:
		if params['type'] == 'send':
			params['data'] = json.loads(params['data'])
			print(params['data'])
			try:
				request_params = {
					'sender_user_login': config['ejudge']['user'],
					'lang_id': params['data']['lang'],
					'contest_id': config['ejudge']['contest_id'],
					'problem': data['prob_id'],
					'file': params['data']['text_input'],
				}
			except:
				return {'answer': {'message': "Неверный формат данных"}}
			print(request_params)
			sendUrl = apiUrl + '/submit-run'
			print(sendUrl)
			request = urllib2.Request(url=sendUrl, data=urllib.parse.urlencode(request_params).encode('utf-8'), 
						   headers={'Authorization': f'Bearer AQAA{token}'}, method='POST')
			try:
				cont = urllib2.urlopen(request)
			except HTTPError as e:
				return{'answer': {'message': f"HTTP Error: {e.code}"}}
			except URLError as e:
				return{'answer': {'message': f"URL Error: {e.reason}"}}
			except Exception as ex:
				return{'answer': {'message': f"Unknown Error: {ex}"}}
			response = json.loads(cont.read().decode('utf8').replace("'", '"'))
			print('response:', response)
			
			run_id = response['result']['run_id']
			if 'run_list' not in data.keys():
				data['run_list'] = []
			data['run_list'].append({'id': run_id, 'data': get_status(run_id)})
			return {'answer': {'status': "successful request"}, 'data_update': data}
		elif params['type'] == 'update':
			try:
				if 'run_list' not in data.keys():
					return {'answer': {'message': "nothing to update"}}
				for elem_index in range(len(data['run_list'])):
					print(elem_index)
					run = data['run_list'][elem_index]
					print(run)
					if run['data']['status'] in ['RJ', 'AV', 'CG', 'CD', 'RU', '']:
						updated_run = get_status(run['id'])
						print('after update: ', updated_run)
						data['run_list'][elem_index]['data'] = updated_run
				return {'answer': {'message': "successful request"}, 'data_update': data}
			except Exception as ex:
				return {'answer': {'message': ex}}

	except:
		return {'answer': {'message': "Неизвестная ошибка"}}
	

def get_status(run_id):
	global token, apiUrl
	request_params = {
		'contest_id': config['ejudge']['contest_id'],
		'run_id': run_id,
	}
	updateUrl = apiUrl + '/run-status-json'
	testUrl = apiUrl + '/raw-report'
	print('url: ', updateUrl)
	try:
		request_1 = urllib2.Request(url=updateUrl, data=urllib.parse.urlencode(request_params).encode('utf-8'), 
						   headers={'Authorization': f'Bearer AQAA{token}'}, method='POST')
		print('test test test!!!')
		print(json.loads(urllib2.urlopen(request_1).read().decode('utf8').replace("'", '"')))
		request = urllib2.Request(url=updateUrl, data=urllib.parse.urlencode(request_params).encode('utf-8'), 
						   headers={'Authorization': f'Bearer AQAA{token}'}, method='POST')
		cont = urllib2.urlopen(request)
		full_response = json.loads(cont.read().decode('utf8').replace("'", '"'))
		print()
		print(full_response['result'])
		print(full_response['result']['run'])
		print()
		response = full_response['result']['run']
		print('update status', 'id=', run_id, response)
		try:
			status = response['status_str']
		except:
			status = ''
		try:
			duration = response['nsec'] // 10**6
		except:
			duration = ''
		try:
			size = response['size']
		except:
			size = ''
		try:
			tests_passed = response['saved_test']
		except:
			tests_passed = '???'
		try:
			submit_time =  response['run_time']
		except:
			submit_time = 0
		try:
			lang = response['lang_name']
		except:
			lang = 'Unknown'
		return {'status': status, 'duration': duration, 'size': size, 'tests_passed': tests_passed, 'submit_time': submit_time, 'lang': lang}
	except:
		return {'status': '', 'duration': '', 'size': '', 'tests_passed': '???', 'submit_time': 0, 'lang': 'Unknown'}