from bottle import route, request
import json
from login import check_token


def get_param(url, param):
	parsed_url = url.split('/')
	for ind in range(0, len(parsed_url)):
		if parsed_url[ind] == param:
			if ind + 1 < len(parsed_url):
				return parsed_url[ind + 1]
			return ''
	return None


def construct_all_crumbs(url, db):
	possible_params = ['land', 'town', 'problem']
	crumbs = []
	current_param_index = None

	for param_index in range(len(possible_params)):
		param_value = get_param(url, possible_params[param_index])
		if param_value != None:
			current_param_index = param_index 
			break
	
	if current_param_index == None: return None
	class_value = get_param(url, 'class')
	if class_value == None:
		return None
	
	if current_param_index != possible_params.index('land'):
		crumbs.append({'name': 'Квантландия', 'link': f'/class/{class_value}/land'})
	else:
		crumbs.append({'name': 'Квантландия', 'link': '/'})

	if current_param_index == possible_params.index('town'):
		town_num = get_param(url, 'town')
		db.execute('''select Kvantland.Town.name
				from Kvantland.Town where town = %s''', (town_num,))
		(town_name, ), = db.fetchall()
		crumbs.append({'name': f'{town_name}', 'link': f'/class/{class_value}/town/{town_num}'})

	if current_param_index == possible_params.index('problem'):
		variant = get_param(url, 'problem')
		db.execute('''select town,  Kvantland.Town.name
				from Kvantland.Problem join Kvantland.Variant using (problem) join 
				Kvantland.Town using (town) where variant = %s''', (variant,))
		(town_num, town_name, ), = db.fetchall()
		crumbs.append({'name': f'{town_name}', 'link': f'/class/{class_value}/town/{town_num}'})
	
	return crumbs


@route('/api/breadcrumbs', method='POST')
def get_breadcrumbs(db):
	resp = {
		'status': False,
		'breadcrumbs': [],
	}
	try:
		url = json.loads(request.body.read())['url']
	except:
		return json.dumps(resp)
	
	token_status = check_token(request)
	if token_status['error']:
		return json.dumps(resp)
	
	print(construct_all_crumbs(url, db))
	try:
		resp['breadcrumbs'] = construct_all_crumbs(url, db)
		resp['status'] = True
		print(resp)
		return json.dumps(resp)
	except:
		return json.dumps(resp)
	