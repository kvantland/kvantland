def solve(variation, ans):
    # operations: + - *
    ops = ['+', '-', '*']
    for n in range(3 ** 6):
        mask = n
        left_expr = ""
        right_expr = ""
        ops_list = []
        for i in range(8):
            if i < 3:
                left_expr += str(variation[i])
                left_expr += ops[mask % 3]
                ops_list.append(ops[mask % 3])
                mask //= 3
            elif i == 3:
                left_expr += str(variation[i])
            elif i < 7:
                right_expr += str(variation[i - 4])
                right_expr += ops[mask % 3]
                ops_list.append(ops[mask % 3])
                mask //= 3
            else:
                right_expr += str(variation[i - 4])
        if eval(left_expr) == eval(right_expr) and left_expr != right_expr:
            # appending the whole expression:
            # ans.append(left_expr + "=" + right_expr)
            ans.append(ops_list)
    return

variations = [
    [i for i in range(97, 101)],
    [i for i in range(98, 102)],
    [i for i in range(99, 103)],
    [i for i in range(100, 104)]
]

answers = [[] for i in range(4)]

for i in range(4):
    solve(variations[i], answers[i])

print(variations)
print(answers)