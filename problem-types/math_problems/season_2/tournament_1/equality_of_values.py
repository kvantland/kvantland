def validate(data, answer):
    try:
        return calculate_equality(data['variant'],answer['signs'])
    except:
        return False


 


def calculate_equality(data, ops):
    # Проверка на наличие недопустимого ввода
    if None in ops or ops[:3] == ops[3:]:
        return False

    # Вычисляем результаты для обеих частей
    left_result = calculate_expression(data, ops[:3])
    right_result = calculate_expression(data, ops[3:])
    print(left_result,right_result)
    return left_result == right_result

def calculate_expression(data, ops):
    results = [data[0]]  # Начинаем с первого числа
    # Сначала обрабатываем операции с более высоким приоритетом (умножение)
    for i in range(1, len(data)):
        if ops[i - 1] == "*":
            results[-1] *= data[i]  # Выполняем умножение немедленно
        else:
            results.append(ops[i - 1])  # Добавляем операцию
            results.append(data[i])  # Добавляем следующее число

    # Теперь обрабатываем операции с низким приоритетом (сложение и вычитание)
    final_result = results[0]
    for i in range(1, len(results), 2):
        operator = results[i]
        next_number = results[i + 1]

        if operator == "-":
            final_result -= next_number
        elif operator == "+":
            final_result += next_number

    return final_result
    
