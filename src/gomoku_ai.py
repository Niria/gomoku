from game_board import Markers
from helpers import function_call_counter, generate_zobrist_table


class GomokuAI:
    EXACT = 'exact'
    LOWER_BOUND = 'lower_bound'
    UPPER_BOUND = 'upper_bound'

    def __init__(self, size):
        self.zobrist_table = generate_zobrist_table(size)
        self.transposition_table = {}
        self.current_hash = 0

        self.heatmap = None
        self.tt_lookups = 0
        self.tt_hits = 0

    def update_hash(self, col, row, marker):
        self.current_hash ^= self.zobrist_table[col][row][marker]

    def find_ai_move(self, gameboard, valid_moves, current_value, depth=5):
        print(self.current_hash)
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
            print(self.current_hash)
            minimax_value = self.minimax(gameboard, alpha, beta, False, child_valid_moves, child_value, depth - 1)

            gameboard.undo_move()
            self.update_hash(col, row, Markers.AI)
            print(self.current_hash)
            print()

            if minimax_value > highest_value:
                highest_value = minimax_value
                best_move = move

            alpha = max(alpha, highest_value)



        print(f"Total calls: {GomokuAI.minimax.calls}")
        board = ""
        for r in self.heatmap:
            for c in r:
                board += f"{c:5}"
            board += "\n"
        print(board)
        # print(self.transposition_table)
        print(f"tt_hits: {self.tt_hits} lookups: {self.tt_lookups}")
        return best_move

    @function_call_counter
    def minimax(self, gameboard, alpha, beta, maximizing, valid_moves, parent_value, depth):
        orig_alpha, orig_beta = alpha, beta
        # print(f"depth: {depth}, candidates: {len(valid_moves)}")

        self.tt_lookups += 1
        if self.current_hash in self.transposition_table:
            self.tt_hits += 1
            state = self.transposition_table[self.current_hash]
            if state['depth'] >= depth:
                match state['flag']:
                    case self.EXACT:
                        # print("found exact")
                        return state['value']
                    case self.LOWER_BOUND:
                        # print("updated alpha")
                        alpha = max(alpha, state['value'])
                    case self.UPPER_BOUND:
                        # print("updated beta")
                        beta = min(beta, state['value'])


                if alpha >= beta:
                    # print(f"pruned depth: {depth} alpha: {alpha} beta: {beta}")
                    return state['value']

        if depth == 0 or gameboard.win_state():
            return parent_value

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

                alpha = max(alpha, value)

                if alpha >= beta:
                    # print(f"pruned in max, depth: {depth} alpha: {alpha} beta: {beta}")
                    break


            if value <= orig_alpha:
                flag = self.UPPER_BOUND
            elif value >= orig_beta:
                flag = self.LOWER_BOUND
            else:
                flag = self.EXACT
            self.transposition_table[self.current_hash] = {'depth': depth, 'flag': flag, 'value': value}


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

                beta = min(beta, value)

                if alpha >= beta:
                    # print(f"pruned in min, depth: {depth} alpha: {alpha} beta: {beta}")
                    break


            if value <= orig_alpha:
                flag = self.UPPER_BOUND
            elif value >= orig_beta:
                flag = self.LOWER_BOUND
            else:
                flag = self.EXACT

            # print(self.current_hash)
            self.transposition_table[self.current_hash] = {'depth': depth, 'flag': flag, 'value': value}

            return value


