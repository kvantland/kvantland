import sys


def steps(step_num, params, data):
    print(params, data, sep='\n', file=sys.stderr)
    try:
        if data['weightings_amount'] <= 0:
            return {'answer': "Out of limit"}
        data['weightings_amount'] -= 1
        weights = [(100 + i) for i in range(1, 11)]
        changed = data['correct']
        left_weight = 0
        right_weight = 0
        for weight in params['left']:
            if weight == changed[0]:
                left_weight += weights[changed[1]]
            elif weight == changed[1]:
                left_weight += weights[changed[0]]
            else:
                left_weight += weights[weight]
        print('left_weight: ', left_weight, file=sys.stderr)
        for weight in params['right']:
            if weight == changed[0]:
                right_weight += weights[changed[1]]
            elif weight == changed[1]:
                right_weight += weights[changed[0]]
            else:
                right_weight += weights[weight]
        print('right_weight: ', right_weight, file=sys.stderr)
        if not ('history' in data.keys()):
            data['history'] = []
        left_str_weights = ', '.join(list(map(str, params['left'])))
        right_str_weights = ', '.join(list(map(str, params['right'])))
        if (right_weight > left_weight):
            history_item = f"({left_str_weights}) < ({right_str_weights})"
            data['history'].append(history_item)
            return {'answer': "right", 'data_update': data}
        elif (right_weight < left_weight):
            data['history'].append(f"({left_str_weights}) > ({right_str_weights})")
            return {'answer': "left", 'data_update': data}
        else:
            data['history'].append(f"({left_str_weights}) = ({right_str_weights})")
            return {'answer': "equal", 'data_update': data}
    except:
        return {'answer', "Unknown error"}

def validate(data, answer):
    try:
        return set(data['correct']) == set(answer)
    except:
        return False