def description(params):
    return '''
            Cоберите функцию, которая реализует алгоритм решета Эратосфена по поиску простых чисел
            среди первых n натуральных чисел. Создается список is_prime длины n + 1, заполненный единицами – 
            изначально мы считаем, что все числа от 0 до n являются простыми, положив is_prime[k] = 1 для 
            любого k от 0 до n. Далее мы инициализируем начальные значения: is_prime[0] = is_prime[1] = 0 – мы 
            знаем, что 0 и 1 не являются простыми числами. После этого перебираем k = 2, …, n. Если is_prime[k] = 0, 
            то мы пропускаем итерацию. Иначе is_prime[k] = 1 и k заведомо простое. Поэтому мы должны пометить числа 
            2k, 3k, … как достоверно не являющимися простыми (положив 0 = is_prime[2k]= is_prime[3k] = …). В самом 
            конце функция должна вернуть список is_prime. Перетаскивая блоки справа, расположите их в области слева 
            так, чтобы получилась корректно работающая программа, которая строит решето Эратосфена.'''


def validate(data, answer):
    try:
        print('user_answer: ', answer)
        answer_permutation = []
        try:
            if len(answer) > len(data['correct'][0]):
                return False
        except:
            return False
        for elem in answer:
            if not('num'in elem.keys()):
                return False
            answer_permutation.append(elem['num'])
        print('answer permutation: ', answer_permutation)
        for correct in data['correct']:
            if correct == answer_permutation:
                return True
        return False
    except:
        return False