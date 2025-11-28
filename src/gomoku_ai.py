import time

from game_board import GameBoard, Marker, Move
from helpers import function_call_counter


class GomokuAI:
    def __init__(self):
        self.visited = {}

    def find_ai_move(self, gameboard: GameBoard, candidates: set[Move],
                     current_value: int, turn_time_limit=10.0) -> Move:
        """
        Initiates the minimax with alpha-beta pruning
        :param gameboard: Instance of GameBoard
        :param candidates: Set of candidate moves
        :param current_value: The heuristic value of the current game state
        :param turn_time_limit: Time limit for the AI's turn
        :return: The best move for the AI
        """
        self.visited = {}
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        start_time = time.time()
        candidates_copy = candidates.copy()

        for depth in range (1,50):
            try:
                GomokuAI.minimax.calls = 0

                value, move = self.minimax(gameboard, alpha, beta, True, candidates_copy,
                                           current_value, depth, start_time, turn_time_limit)

                best_move = move
                print(f"Depth: {depth} done, best move: {best_move}, minimax calls: {GomokuAI.minimax.calls}")

                if value >= gameboard.OPEN_FOUR * 0.8:
                    print(f"Open four found, value: {value} move: {best_move}")
                    break

            except Timeout:
                print(f"Depth: {depth} timeout")
                break

        return best_move

    @function_call_counter
    def minimax(self, gameboard: GameBoard, alpha: float, beta: float, maximizing: bool,
                candidates: set[Move], parent_value: int, depth: int, start_time: float,
                turn_time_limit: float) -> tuple[int, Move | None]:
        """
        Minimax algorithm
        :param gameboard: Instance of GameBoard
        :param alpha: The alpha value used in alpha-beta pruning
        :param beta: The beta value used in alpha-beta pruning
        :param maximizing: Boolean toggle for minimax's max_value and min_value computation
        :param candidates: List of candidate moves
        :param parent_value: Heuristic value of the game state prior to trying the candidate moves
        :param depth: The depth remaining in the minimax search
        :param start_time: Starting time for the search
        :param turn_time_limit: Maximum time that the AI can take to determine the best move
        :return:
        """
        if time.time() - start_time >= turn_time_limit:
            raise Timeout()

        prev_best_move = None

        if gameboard.zobrist_hash in self.visited:
            prev_value, prev_move, prev_depth = self.visited[gameboard.zobrist_hash]
            if prev_depth >= depth:
                return prev_value, prev_move
            prev_best_move = prev_move

        if depth == 0 or gameboard.win_state():
            return parent_value, None

        marker = Marker.AI if maximizing else Marker.PLAYER

        prev_best = []
        if prev_best_move in candidates:
            col, row = prev_best_move
            prev_best_value = gameboard.get_move_value(col, row, marker)
            prev_best_distance = gameboard.get_distance_to_prev_move(col, row)
            prev_best = [(prev_best_move, prev_best_value, prev_best_distance)]

        sorted_candidates = []
        winning_move = None
        for move in candidates:
            if move == prev_best_move:
                continue
            col, row = move
            mv_value = gameboard.get_move_value(col, row, marker)

            if mv_value >= GameBoard.OPEN_FOUR * 0.8:
                winning_move = (move, mv_value)
                break

            mv_distance = gameboard.get_distance_to_prev_move(col, row)
            sorted_candidates.append((move, mv_value, mv_distance))

        if winning_move:
            best_move = winning_move[0]
            value = parent_value + winning_move[1]

            self.visited[gameboard.zobrist_hash] = value, best_move, depth
            return value, best_move

        if maximizing:
            sorted_candidates.sort(key=lambda x: (x[1], -x[2]), reverse=True)
        else:
            sorted_candidates.sort(key=lambda x: (x[1], x[2]), reverse=False)
        sorted_candidates = prev_best + sorted_candidates

        best_move = None
        if maximizing:
            max_value = float('-inf')

            for move, move_value, _ in sorted_candidates:
                col, row = move
                new_value = parent_value + move_value

                new_candidates = gameboard.update_candidates(candidates, col, row)
                gameboard.move(col, row, marker)

                try:
                    value, _ = self.minimax(gameboard, alpha, beta, False, candidates,
                                            new_value, depth - 1, start_time, turn_time_limit)
                finally:
                    gameboard.undo_move()
                    for new_candidate in new_candidates:
                        candidates.remove(new_candidate)
                    candidates.add(move)
                if value > max_value:
                    max_value = value
                    best_move = move

                alpha = max(alpha, value)

                if alpha >= beta:
                    self.visited[gameboard.zobrist_hash] = max_value, best_move, depth
                    break

            self.visited[gameboard.zobrist_hash] = max_value, best_move, depth

            return max_value, best_move
        else:
            min_value = float('inf')

            for move, move_value, _ in sorted_candidates:
                col, row = move
                new_value = parent_value + move_value

                new_candidates = gameboard.update_candidates(candidates, col, row)
                gameboard.move(col, row, marker)
                try:
                    value, _ = self.minimax(gameboard, alpha, beta, True, candidates,
                                            new_value, depth - 1, start_time, turn_time_limit)
                finally:
                    gameboard.undo_move()
                    for new_candidate in new_candidates:
                        candidates.remove(new_candidate)
                    candidates.add(move)

                if value < min_value:
                    min_value = value
                    best_move = move

                beta = min(beta, value)

                if alpha >= beta:
                    self.visited[gameboard.zobrist_hash] = min_value, best_move, depth
                    break
            self.visited[gameboard.zobrist_hash] = min_value, best_move, depth

            return min_value, best_move


class Timeout(Exception):
    pass
