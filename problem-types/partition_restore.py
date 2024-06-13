import sys

def validate(data, answer):
    parents = dict()

    def make_set(v):
        parents[v] = v  

    def find_set(v):
        if v == parents[v]:
            return v
        return find_set(parents[v])

    def union_sets(a, b):
        a = find_set(a)
        b = find_set(b)
        if a != b:
            parents[a] = b

    def same_color_near_amount(color, row, column):
        amount = 0
        if (row > 0):
            if answer[row - 1][column] == color:
                amount += 1
                union_sets((row, column), (row - 1, column))
        if (column > 0):
            if  answer[row][column - 1] == color:
                amount += 1
                union_sets((row, column), (row, column - 1))
        return amount
    
    try:
        board_numbers = data['start_board']
        current_perimeters = dict()
        expected_perimeters = dict()
        component_colors = dict()
        board_side = len(data['start_board'])

        for row in range(board_side):
            for column in range(board_side):
                field_color = answer[row][column]
                make_set((row, column))
                if not field_color in current_perimeters.keys():
                    current_perimeters[field_color] = 4
                else:
                    amount = same_color_near_amount(field_color, row, column)
                    current_perimeters[field_color] += 4 - 2 * amount
                if expected_perimeter := board_numbers[row][column]:
                    if field_color in expected_perimeters.keys():
                        return False
                    expected_perimeters[field_color] = expected_perimeter

        for row in range(board_side):
            for column in range(board_side):
                head_row, head_column = find_set((row, column))
                component_color = answer[head_row][head_column]
                if component_color in component_colors.keys():
                    if component_colors[component_color] != (head_row, head_column):
                        return False
                component_colors[component_color] = (head_row, head_column)

        return expected_perimeters == current_perimeters
    except: 
        return False