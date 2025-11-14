from game_board import Markers, GameBoard
from helpers import function_call_counter


class GomokuAI:

    def __init__(self):
        self.current_hash = 0
        self.visited = {}

        self.heatmap = None
        self.duplicates = 0
        self.value_map = None
        self.prunes = 0


    def find_ai_move(self, gameboard, valid_moves, current_value, depth=5):
        self.visited = {}
        best_move = None
        highest_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        self.heatmap = [[0 for _ in range(20)] for _ in range(20)]
        self.value_map = [[0 for _ in range(20)] for _ in range(20)]
        GomokuAI.minimax.calls = 0

        sorted_moves = sorted(valid_moves, key=lambda x: gameboard.get_move_value(x[0], x[1], Markers.AI), reverse=True)
        print(sorted_moves)
        print(valid_moves)

        for move in sorted_moves:
            col, row = move
            self.heatmap[row][col] += 1
            child_value = current_value + gameboard.get_move_value(col, row, Markers.AI)
            child_valid_moves = gameboard.get_valid_moves_set(valid_moves, col, row)

            gameboard.move(col, row, Markers.AI)
            minimax_value = self.minimax(gameboard, alpha, beta, False, child_valid_moves, child_value, depth - 1)
            gameboard.undo_move()

            if minimax_value > highest_value:
                highest_value = minimax_value
                best_move = move
                self.value_map[row][col] = highest_value

            if not self.value_map[row][col] and minimax_value == highest_value:
                self.value_map[row][col] = -1
            else:
                self.value_map[row][col] = minimax_value


            alpha = max(alpha, highest_value)

        board = ""
        for r in self.heatmap:
            for c in r:
                board += f"{c:5}"
            board += "\n"
        print(board)
        board = ""
        for r in self.value_map:
            for c in r:
                board += f"{c:5}"
            board += "\n"
        print(board)

        print(f"Total minimax calls: {GomokuAI.minimax.calls}, estimated prunes: {self.prunes}, duplicate boards: {self.duplicates}")
        print(f"AI chose: {best_move}")

        return best_move

    @function_call_counter
    def minimax(self, gameboard, alpha, beta, maximizing, valid_moves, parent_value, depth):
        if gameboard.zobrist_hash in self.visited:
            self.duplicates += 1
            return self.visited[gameboard.zobrist_hash]

        if depth == 0 or gameboard.win_state():
            return parent_value

        marker = Markers.AI if maximizing else Markers.PLAYER


        if maximizing:
            value = float('-inf')
            sorted_moves = sorted(valid_moves,
                                  key=lambda x: gameboard.get_move_value(x[0], x[1], marker),
                                  reverse=True)

            for move in sorted_moves:
                col, row = move
                self.heatmap[row][col] += 1
                child_value = parent_value + gameboard.get_move_value(col, row, marker)
                child_valid_moves = gameboard.get_valid_moves_set(valid_moves, col, row)

                gameboard.move(col, row, marker)
                value = max(value, self.minimax(gameboard, alpha, beta, False, child_valid_moves, child_value, depth - 1))
                gameboard.undo_move()

                alpha = max(alpha, value)

                if alpha >= beta:
                    self.prunes += len(valid_moves)**(depth-1)
                    # print(f"pruned in max, depth: {depth} alpha: {alpha} beta: {beta}")
                    break

            self.visited[gameboard.zobrist_hash] = value

            return value
        else:
            value = float('inf')
            sorted_moves = sorted(valid_moves, key=lambda x: gameboard.get_move_value(x[0], x[1], marker))

            for move in sorted_moves:
                col, row = move
                self.heatmap[row][col] += 1
                child_value = parent_value + gameboard.get_move_value(col, row, marker)
                child_valid_moves = gameboard.get_valid_moves_set(valid_moves, col, row)

                gameboard.move(col, row, marker)
                value = min(value, self.minimax(gameboard, alpha, beta, True, child_valid_moves, child_value, depth - 1))
                gameboard.undo_move()

                beta = min(beta, value)

                if alpha >= beta:
                    self.prunes += len(valid_moves)**(depth-1)
                    # print(f"pruned in min, depth: {depth} alpha: {alpha} beta: {beta}")
                    break

            self.visited[gameboard.zobrist_hash] = value

            return value


