import json
from turtle import position

def steps(step_num, params, data):
    try:
        try:
            if 'program' not in params.keys():
                if 'reload' in params.keys():
                    if data['action_allowed']:
                        return {'answer': {'message': "Перезапуск сейчас не требуется"}}
                    else:
                        data = data['default']
                        return {'answer': {'reload': True}, 'data_update': data}
                else:
                    if 'checkout' in params.keys():
                        print('checkout!')
                        if data['current_position'] == data['end_position']:
                            print('successful checkout!')
                            return {'answer': {}, 'answer_correct': True, 'user_answer': data['current_position'], 'solution': params['solution']}
                        else:
                            print('unsuccessful checkout!')
                            if data['points'] <= 0:
                                return {'answer': {}, 'answer_correct': False, 'user_answer': data['current_position'], 'solution': params['solution']}
                            else:
                                return {'answer': {'message': "Неверно. Робот не дошёл до нужной точки"}}
                    else:
                        return {'answer': {'message': "Неверный формат запроса"}}
        except:
            return {'asnwer': {'message': "Неверный формат запроса"}}
        program = json.loads(params['program'])

        def printt(matrix):
            for arr in matrix:
                for elem in arr:
                    if elem in [True, False]:
                        print(int(elem), end=' ')
                    else:
                        print(elem, end=' ')
                print()

        def command_amount(program):
            amount = 0
            for command in program:
                print(command)
                if 'children' in command.keys():
                      amount += command_amount(command['children'])
                amount += 1
            return amount

        def check(x, y, add):
            new_x, new_y = [x + add[0], y + add[1]]
            if not(new_x < board_side and new_x >= 0):
                return False
            if not(new_y < board_side and new_y >= 0):
                return False
            if new_x != x and vertical_walls[new_y][(x + new_x - 1) // 2]:
                print('vertical wall', x, new_x)
                return False
            if new_y != y and horizontal_walls[(new_y + y - 1) // 2][new_x]:
                print('horizontal wall', y, new_y)
                return False
            return True

        def execute_program(x, y, direction, program):
            for command in program:
                if (len(command_list) > 100):
                    return [x, y, direction]
                print(x, y, command['type'], command['text'], direction_array[direction], sep=' -- ')
                if command['type'] == 'usual':
                    text = command['text']
                    if text == 'Повернуть влево':
                        direction = (direction + 3) % 4
                    elif text == 'Повернуть вправо':
                        direction = (direction + 1) % 4
                    elif text == 'Пройти вперед на 1 клетку':
                        if check(x, y, position_transform[direction_array[direction]]):
                            x += position_transform[direction_array[direction]][0]
                            y += position_transform[direction_array[direction]][1]
                            command_list.append([y, x, direction_array[direction]])
                        else:
                            print('unsuccess')
                            return [x, y, direction]
                    else:
                        return {'answer': {'message': "Недопустимая команда"}}
                elif command['type'] == 'cycle':
                    if 'children' in command.keys():
                        while True:
                            if new_result := execute_program(x, y, direction, command['children']):
                                if [x, y] != [new_result[0], new_result[1]]:
                                    x, y, direction = new_result
                                else:
                                    break
                            else:
                                break
                else:
                    return {'answer': {'message': "Недопустимый тип блока"}}
            return [x, y, direction]
        
        def stripp(command_list):
            index = len(command_list) - 1
            if index < 0:
                return command_list
            last_position = [command_list[index][0], command_list[index][1]]
            index -= 1
            while index >= 0:
                if [command_list[index][0], command_list[index][1]] != last_position:
                    break
                index -= 1
            return command_list[0:index + 2]
        
        if not data['action_allowed']:
            return {'answer': {'message': "Необходимо сбросить положение робота. Цена - 1 квантик"}}
        
        if command_amount(program) > data['allowed_blocks_amount']:
            return {'answer': {'message': "Слишком много блоков использовано"}}
        
        direction_array = ['left', 'top', 'right', 'bottom']
        position_transform = {
            'left': [-1, 0],
            'right': [1, 0],
            'top': [0, -1],
            'bottom': [0, 1],
        }
        [current_y, current_x] = data['current_position']
        current_diraction = direction_array.index(data['current_direction'])
        board_side = len(data['maze']) - 1
    
        vertical_walls = []
        horizontal_walls = []
        row_num = 0

        for row in data['maze']:
            if row_num == 0:
                row_num += 1
                continue
            horizontal_walls_row = []
            vertical_walls_row = []
            symb_num = 0
            for symb in row:
                if symb == '|' and symb_num != 0 and symb_num + 1 < len(data['maze'][0]):
                    vertical_walls_row.append(True)
                elif symb == '.' and symb_num != 0 and symb_num + 1 < len(data['maze'][0]):
                    vertical_walls_row.append(False)
                elif symb == '_' and row_num + 1 < len(data['maze']):
                    horizontal_walls_row.append(True)
                elif symb == ' ' and row_num + 1 < len(data['maze']):
                    horizontal_walls_row.append(False)
                symb_num += 1
            vertical_walls.append(vertical_walls_row)
            horizontal_walls.append(horizontal_walls_row)
            row_num += 1

        try:
            command_list = []
            x, y, direction = execute_program(current_x, current_y, current_diraction, program)
            command_list = stripp(command_list)
            printt(command_list)
            data['current_direction'] = direction_array[direction]
            data['current_position'] = [y, x]
            data['action_allowed'] = False
            return {'answer': {'command_list': command_list}, 'data_update': data}
        except:
            return {'answer': {'message': "Unknown error"}}
        
    except:
        return {'answer': {'message': "Unknown error"}}
    

def validate(data, answer):
    return data['current_position'] == data['end_position']