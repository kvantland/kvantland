import problem

def entry_form(data, kwargs):
	yield ''

def validate(data, answer):
	answer = int(answer)
	return answer == data['correct']

CUSTOM_BUTTONS = True
SAVE_PROGRESS = False
