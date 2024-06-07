import sys

def validate(data, answer):
    print('lock_code answer: ', answer, file=sys.stderr)
    return data['correct'] == answer