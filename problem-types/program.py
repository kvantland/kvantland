from config import config
import urllib.request as urllib2
import urllib.parse
import certifi
from urllib.error import HTTPError, URLError
import json

token = config['ejudge']['token']
apiUrl = config['ejudge']['apiUrl']
print(token)

def steps(step_num, params, data):
	global token, apiUrl
	try:
		params['data'] = json.loads(params['data'])
		if params['type'] == 'send':
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
			print('succccces')
			try:
				cont = urllib2.urlopen(request)
				print('here')
			except HTTPError as e:
				print(f"HTTP Error: {e.code}")
				print(e)
			except URLError as e:
				print(f"URL Error: {e.reason}")
				print(e)
			except Exception as ex:
				print(ex)
				print(ex.args)
			print(cont.read())
			'''
			run_id = response['result']['run_id']
			if 'run_list' in data.keys():
				data['run_list'] = []
			data['run_list'].append({'id': run_id, 'status': get_status(run_id)})
			pass'''
		elif params['type'] == 'update':
			pass
	except:
		return {'answer': {'message': "Неизвестная ошибка"}}
	

def get_status(run_id):
	global token, apiUrl
	request_params = {
		'contest_id': config['ejudge']['contest_id'],
		'run_id': run_id,
	}
	updateUrl = apiUrl + '/run-status-json'
	try:
		request = urllib2.Request(url=updateUrl, data=urllib.parse.urlencode(request_params).encode('utf-8'), 
						   headers={f'Authorization: Bearer AQAA{token}'}, method='POST')
		cont = urllib2.urlopen(request, cafile=certifi.where())
		response = json.loads(cont.read())
		print('updat status', 'id=', run_id, response)
		return response
	except:
		return {}