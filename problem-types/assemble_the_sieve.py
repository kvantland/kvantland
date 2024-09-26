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