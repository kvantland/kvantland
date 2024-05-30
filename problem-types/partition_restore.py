import sys

def replace(arr, prev_value, new_value):
    for arr_row in range(len(arr)):
        for arr_item in range(len(arr[arr_row])):
            if arr[arr_row][arr_item] == prev_value:
                arr[arr_row][arr_item] = new_value
    return arr


def validate(data, answer):
    # print(replace(data['correct'][0], 1, 'c3'), file=sys.stderr)
    print('answer: ', answer, file=sys.stderr)
    try:
        if len(answer) != len(data['correct'][0]):
            return False
        for row_ind in range(len(answer)):
            if len(answer[row_ind]) != len(data['correct'][0][row_ind]):
                return False
            for column_ind in range(len(answer[row_ind])):
                if not str(answer[row_ind][column_ind]) in [str(i) for i in range(10)]:
                    return False
                answer[row_ind][column_ind] = 'c' + str(answer[row_ind][column_ind])
                prev_value = data['correct'][0][row_ind][column_ind]
                if not 'c' in str(prev_value):
                    data['correct'][0] = replace(data['correct'][0], prev_value, answer[row_ind][column_ind])
                print(data['correct'][0])
        print('final_data: ', data['correct'][0], file=sys.stderr)
        print('final_answer: ', answer, file=sys.stderr)
        return data['correct'][0] == answer
    except:
        return False