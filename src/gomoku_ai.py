from game_board import Markers
from helpers import function_call_counter, generate_zobrist_table


class GomokuAI:
    def __init__(self, size):
        self.zobrist_table = generate_zobrist_table(size)
        self.transposition_table = {}
        self.current_hash = 0

        self.heatmap = None

    def update_hash(self, col, row, marker):
        self.current_hash ^= self.zobrist_table[col][row][marker]

    def find_ai_move(self, gameboard, valid_moves, current_value, depth=5):
        self.heatmap = [[0 for _ in range(20)] for _ in range(20)]
        GomokuAI.minimax.calls = 0
        best_move = None
        highest_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in valid_moves:
            self.heatmap[move[1]][move[0]] += 1
            col, row = move
            child_value = current_value + gameboard.get_move_value(col, row, Markers.AI)
            child_valid_moves = gameboard.get_valid_moves(valid_moves, col, row)

            gameboard.move(col, row, Markers.AI)
            self.update_hash(col, row, Markers.AI)
            minimax_value = self.minimax(gameboard, alpha, beta, False, child_valid_moves, child_value, depth - 1)

            gameboard.undo_move()
            self.update_hash(col, row, Markers.AI)

            if minimax_value > highest_value:
                highest_value = minimax_value
                best_move = move

            alpha = max(alpha, highest_value)

        self.transposition_table[self.current_hash] = (highest_value, depth)

        print(f"Total calls: {GomokuAI.minimax.calls}")
        board = ""
        for r in self.heatmap:
            for c in r:
                board += f"{c:5}"
            board += "\n"
        print(board)
        return best_move

    @function_call_counter
    def minimax(self, gameboard, alpha, beta, maximizing, valid_moves, parent_value, depth):
        if depth == 0 or gameboard.win_state():
            return parent_value

        if self.current_hash in self.transposition_table and self.transposition_table[self.current_hash][1] >= depth:
            return self.transposition_table[self.current_hash][0]

        marker = Markers.AI if maximizing else Markers.PLAYER

        if maximizing:
            value = float('-inf')
            for move in valid_moves:
                self.heatmap[move[1]][move[0]] += 1
                col, row = move
                child_value = parent_value + gameboard.get_move_value(col, row, marker)
                child_valid_moves = gameboard.get_valid_moves(valid_moves, col, row)

                gameboard.move(col, row, marker)
                self.update_hash(col, row, marker)
                value = max(value, self.minimax(gameboard, alpha, beta, False, child_valid_moves, child_value, depth - 1))

                gameboard.undo_move()
                self.update_hash(col, row, marker)

                if value >= beta:
                    # print("beta")
                    break

                alpha = max(alpha, value)

            self.transposition_table[self.current_hash] = (value, depth)

            return value
        else:
            value = float('inf')
            for move in valid_moves:
                self.heatmap[move[1]][move[0]] += 1
                col, row = move
                child_value = parent_value + gameboard.get_move_value(col, row, marker)
                child_valid_moves = gameboard.get_valid_moves(valid_moves, col, row)

                gameboard.move(col, row, marker)
                self.update_hash(col, row, marker)
                value = min(value, self.minimax(gameboard, alpha, beta, True, child_valid_moves, child_value, depth - 1))

                gameboard.undo_move()
                self.update_hash(col, row, marker)

                if value <= alpha:
                    # print("alpha")
                    break

                beta = min(beta, value)

            self.transposition_table[self.current_hash] = (value, depth)


            return value



