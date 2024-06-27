import sys
from copy import deepcopy

def steps(step_num, params, data):
    if params['type'] == "clear":
        transfusion_subject= params['transfusionSubject']
        print(transfusion_subject, file=sys.stderr)
        subject_num = transfusion_subject[1]
        subject_type = transfusion_subject[0]
        if subject_type != "pot":
            return {'answer': "wrong object type"}
        configuration = deepcopy(data['configuration'])
        configuration[subject_num]['water'] = 0
        configuration[subject_num]['nectar'] = 0
        if not 'default' in data.keys():
            data['default'] = {'configuration': deepcopy(data['configuration'])}
        data['configuration'] = configuration
        print(configuration, file=sys.stderr)
        return {'answer': "success", 'data_update': data}
    if params['type'] == "reload":
        if 'default' in data.keys():
            data['configuration'] = data['default']['configuration']
        return {'answer': "reload", 'data_update': data}
    try: # проверка формата данных ['object_name', 'object_num']
        transfusion_object = params['transfusionObject']
        transfusion_subject = params['transfusionSubject']
        if len(transfusion_object) != 2 or transfusion_object[0] != 'pot' or not(transfusion_object[1] in [0, 1, 2]):
            return {'answer': "not correct data"}
        if len(transfusion_subject) != 2 or not(transfusion_subject[0] in ['tap', 'pot']) or not(transfusion_object[1] in [0, 1, 2]):
            return {'answer': "not correct data"}
        if transfusion_subject[1] == 'tap' and transfusion_subject[1] != 0:
            return {'answer': "not correct data"}
    except:
        return {'answer': "not correct data"}
    volumes = data['volumes']
    configuration = data['configuration']
    if not 'default' in data.keys():
        data['default'] = {'configuration': deepcopy(data['configuration'])}
    
    object_num = transfusion_object[1]
    subject_num  = transfusion_subject[1]
    if transfusion_subject[0] == 'tap':
        configuration[object_num]['water'] = volumes[object_num] - configuration[object_num]['nectar']
    if transfusion_subject[0] == 'pot':
        object_liquid = configuration[object_num]['nectar'] + configuration[object_num]['water']
        subject_liquid = configuration[subject_num]['nectar'] + configuration[subject_num]['water']
        if subject_liquid == 0:
            return {'answer': "empty pot"}
        subject_concentration = configuration[subject_num]['nectar'] / subject_liquid
        transfusion_liquid_amount = min(subject_liquid, volumes[object_num] - object_liquid)
        transfusion_nectar_amount = transfusion_liquid_amount * subject_concentration
        transfusion_water_amount = transfusion_liquid_amount * (1 - subject_concentration)
        configuration[object_num]['water'] += transfusion_water_amount
        configuration[object_num]['nectar'] += transfusion_nectar_amount
        configuration[subject_num]['water'] -= transfusion_water_amount
        configuration[subject_num]['nectar'] -= transfusion_nectar_amount
    data['configuration'] = configuration
    print(data, file=sys.stderr)
    return {'answer': "success", 'data_update': data}

def validate(data, answer):
    for pot in data['configuration']:
        nectar = pot['nectar']
        water = pot['water']
        if (nectar / (nectar + water) - data['purpose']['nectar']) < 0.000001:
            return True
    return False
    
    
    