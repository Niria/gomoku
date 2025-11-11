def find_ai_move(gameboard, valid_moves, current_value, depth=3):
    best_move = None
    highest_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in valid_moves:
        col, row = move
        child_value = current_value + gameboard.get_move_value(col, row, False)
        child_valid_moves = gameboard.get_valid_moves(valid_moves, col, row)

        gameboard.move(col, row, False)
        minimax_value = minimax(gameboard, alpha, beta, True, child_valid_moves, child_value, depth - 1)
        gameboard.undo_move()

        if minimax_value > highest_value:
            highest_value = minimax_value
            best_move = move

        alpha = max(alpha, highest_value)

    return best_move

def minimax(gameboard, alpha, beta, maximizing_player, valid_moves, parent_value, depth):
    if depth == 0 or gameboard.win_state():
        return parent_value
    if maximizing_player:
        value = float('-inf')
        for move in valid_moves:
            col, row = move
            child_value = parent_value + gameboard.get_move_value(col, row, maximizing_player)
            child_valid_moves = gameboard.get_valid_moves(valid_moves, col, row)

            gameboard.move(col, row, False)
            value = max(value, minimax(gameboard, alpha, beta, False, child_valid_moves, child_value, depth - 1))
            gameboard.undo_move()

            if value >= beta:
                break

            alpha = max(alpha, value)
        return value
    else:
        value = float('inf')
        for move in valid_moves:
            col, row = move
            child_value = parent_value + gameboard.get_move_value(col, row, maximizing_player)
            child_valid_moves = gameboard.get_valid_moves(valid_moves, col, row)

            gameboard.move(col, row, True)
            value = min(value, minimax(gameboard, alpha, beta, True, child_valid_moves, child_value, depth - 1))
            gameboard.undo_move()

            if value <= alpha:
                break

            beta = min(beta, value)
        return value
