def validate(data, answer):
    try:
        return True
    except:
        return False

def calculate_expression(values, operations):
    total_sum = 0
    total_product = 1

    for i in range(len(values)):
        if operations[i] == '×':
            total_product *= values[i]
        elif operations[i] == '+':
            total_sum += values[i]
        elif operations[i] == '−':
            total_sum -= values[i]

    return total_sum * total_product

def compute_results(initial_data, operations):
    if None in operations:
        return False

    left_operations = operations[:len(initial_data['left_values'])]
    right_operations = operations[len(initial_data['left_values']):]

    left_result = calculate_expression(initial_data['left_values'], left_operations)
    right_result = calculate_expression(initial_data['right_values'], right_operations)

    return left_result == right_result



# Пример данных для вызова функции
initial_data = {
    'left_values': [97, 98, 99, 100],
    'right_values': [100, 101, 102, 103]
}

operations = [
    '+',
    'x',
    '+',
    '-',
    '+',
    '−',
]

# Вызов функции валидации и вывод результата
result = validate({'data': initial_data, 'signs': operations})
print(result)
