import numpy as np

def solve(variation, answer):
    for n in range(32):
        res = np.array([[0, 0], [0, 0]])
        mask = n
        i = 0
        lst = []
        while mask > 0:
            flag = mask % 2
            if flag:
                res += variation[i]
                lst.append(i + 1)
            mask //= 2
            i += 1
        flag = True
        for i in range(2):
            for j in range(2):
                res[i, j] %= 2
                flag &= res[i, j]
        if flag:
            answer.append(lst)
    return

variations = [
    [[[0, 1], [1, 1]], [[0, 1], [1, 0]], [[0, 0], [1, 1]], [[1, 1], [0, 1]], [[1, 0], [1, 1]]],
    [[[1, 1], [1, 0]], [[0, 1], [1, 0]], [[1, 1], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [1, 1]]],
    [[[0, 1], [1, 0]], [[1, 1], [1, 0]], [[1, 0], [1, 1]], [[1, 1], [0, 1]], [[1, 1], [0, 0]]],
    [[[0, 1], [1, 0]], [[0, 1], [1, 1]], [[1, 0], [1, 1]], [[1, 1], [0, 1]], [[0, 0], [1, 1]]]
]

variations = [[np.array(elem) for elem in variation] for variation in variations]

answers = [[] for i in range(4)]

for i in range(4):
    solve(variations[i], answers[i])

print(answers)
