import problem

def entry_form(data, kwargs):
	yield ''

def validate(data, answer):
	return str(answer) == str(data['correct'])

CUSTOM_BUTTONS = True
SAVE_PROGRESS = False
