import problem

def entry_form(data, kwargs):
	yield ''

def validate(data, answer):
	try:
		return str(answer) == str(data['correct'])
	except:
		return False

CUSTOM_BUTTONS = True
SAVE_PROGRESS = False
