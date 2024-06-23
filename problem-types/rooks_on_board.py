def validate(data, answer):
    beaten_rooks_amount = None
    rooks_on_board = 0
    side = 8
    try:
        def beaten_rooks(row, column):
            beaten_rooks_amount = 0
            for other_row in range(side):
                if other_row == row:
                    continue
                if answer[other_row][column]['type'] == 'rook_b':
                    beaten_rooks_amount += 1
            for other_column in range(side):
                if other_column == column:
                    continue
                if answer[row][other_column]['type'] == 'rook_b':
                    beaten_rooks_amount += 1
            return beaten_rooks_amount      
        
        for row in range(side):
            for column in range(side):
                if answer[row][column]['type'] == 'rook_b':
                    rooks_on_board += 1
                if beaten_rooks_amount == None and answer[row][column]['type'] == 'rook_b':
                    beaten_rooks_amount = beaten_rooks(row, column)
                    print(row, column, beaten_rooks_amount)
                elif beaten_rooks_amount != None and answer[row][column]['type'] == 'rook_b':
                    current_beaten_rooks = beaten_rooks(row, column)
                    print(row, column, current_beaten_rooks)
                    if beaten_rooks_amount != current_beaten_rooks:
                        return False
        if rooks_on_board != data['rooks_amount']:
            return False
        return True
    except:
        return False