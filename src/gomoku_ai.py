import time

from game_board import GameBoard, Marker, Move
from helpers import function_call_counter


class GomokuAI:
    TT_EXACT = 0
    TT_LOWER_BOUND = 1
    TT_UPPER_BOUND = 2

    def __init__(self):
        self.visited = {}
        self.best_move_before_timeout = None
        self.history_table = {}

    def find_ai_move(self, gameboard: GameBoard, candidates: set[Move],
                     turn_time_limit=10.0) -> Move:
        """
        Initiates the minimax with alpha-beta pruning
        :param gameboard: Instance of GameBoard
        :param candidates: Set of candidate moves
        :param turn_time_limit: Time limit for the AI's turn
        :return: The best move for the AI
        """
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        start_time = time.time()
        candidates_copy = candidates.copy()
        self.history_table = {}

        for depth in range (1,50):
            try:
                GomokuAI.minimax.calls = 0
                self.best_move_before_timeout = None

                value, move = self.minimax(gameboard, alpha, beta, True, candidates_copy,
                                           0, depth, start_time, turn_time_limit,
                                           depth)

                best_move = move
                print(f"Depth: {depth} done, best move: {best_move}, minimax calls: {GomokuAI.minimax.calls}")

                if value >= gameboard.OPEN_FOUR * 0.8:
                    print(f"Open four found, value: {value} move: {best_move}")
                    break

            except Timeout:
                if self.best_move_before_timeout:
                    best_move = self.best_move_before_timeout
                print(f"Depth {depth} timed out, best move: {best_move}, minimax calls: {GomokuAI.minimax.calls}")
                break

        return best_move

    @function_call_counter
    def minimax(self, gameboard: GameBoard, alpha: float, beta: float, maximizing: bool,
                candidates: set[Move], parent_value: int, depth: int, start_time: float,
                turn_time_limit: float, root_depth: int | None=None) -> tuple[int, Move | None]:
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
        :param root_depth: The depth the search was initially started with
        :return:
        """
        if time.time() - start_time >= turn_time_limit:
            raise Timeout()

        alpha_orig = alpha
        beta_orig = beta

        tt_entry = self.visited.get(gameboard.zobrist_hash)
        if tt_entry:
            prev_value, prev_move, prev_depth, flag = tt_entry
            if prev_depth >= depth:
                if flag == self.TT_EXACT:
                    return prev_value, prev_move
                elif flag == self.TT_LOWER_BOUND:
                    alpha = max(alpha, prev_value)
                elif flag == self.TT_UPPER_BOUND:
                    beta = min(beta, prev_value)

                if alpha >= beta:
                    return prev_value, prev_move

        prev_best_move = tt_entry[1] if tt_entry else None

        if gameboard.win_state():
            return (-gameboard.WIN_VALUE if maximizing else gameboard.WIN_VALUE), None

        if depth == 0:
            return parent_value, None

        marker = Marker.AI if maximizing else Marker.PLAYER
        sorted_candidates = []

        for move in candidates:
            col, row = move
            is_prev_best = move == prev_best_move
            mv_historical_value = self.history_table.get(move, 0)
            mv_distance = gameboard.get_distance_to_prev_move(col, row)
            sorted_candidates.append((move, is_prev_best, mv_historical_value, mv_distance))

        sorted_candidates.sort(key=lambda x: (x[1], x[2], -x[3]), reverse=True)

        best_move = None
        if maximizing:
            best_value = float('-inf')
            for i, (move, _, _, _) in enumerate(sorted_candidates):
                col, row = move
                value_delta = gameboard.get_move_value(col, row, marker)
                new_value = parent_value + value_delta

                new_candidates = gameboard.update_candidates(candidates, col, row)
                gameboard.move(col, row, marker)

                try:
                    if i == 0 or depth < 4:
                        value, _ = self.minimax(gameboard, alpha, beta, not maximizing, candidates,
                                            new_value, depth - 1, start_time, turn_time_limit,
                                            root_depth)
                    else:
                        value, _ = self.minimax(gameboard, alpha, alpha+1, not maximizing, candidates,
                                                new_value, depth - 1, start_time, turn_time_limit,
                                                root_depth)

                        if alpha < value < beta:
                            value, _ = self.minimax(gameboard, alpha, beta, not maximizing,
                                                    candidates, new_value, depth - 1, start_time,
                                                    turn_time_limit, root_depth)

                finally:
                    gameboard.undo_move()
                    for new_candidate in new_candidates:
                        candidates.remove(new_candidate)
                    candidates.add(move)

                if value > best_value:
                    best_value = value
                    best_move = move

                    if depth == root_depth:
                        self.best_move_before_timeout = best_move

                alpha = max(alpha, best_value)

                if alpha >= beta:
                    self.history_table[best_move] = self.history_table.get(best_move, 0) + 2**depth
                    break

        else:
            best_value = float('inf')
            for move, _, _, _ in sorted_candidates:
                col, row = move
                value_delta = gameboard.get_move_value(col, row, marker)
                new_value = parent_value + value_delta

                new_candidates = gameboard.update_candidates(candidates, col, row)
                gameboard.move(col, row, marker)

                try:
                    value, _ = self.minimax(gameboard, alpha, beta, not maximizing, candidates,
                                            new_value, depth - 1, start_time, turn_time_limit,
                                            root_depth)
                finally:
                    gameboard.undo_move()
                    for new_candidate in new_candidates:
                        candidates.remove(new_candidate)
                    candidates.add(move)

                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)

                if alpha >= beta:
                    self.history_table[best_move] = self.history_table.get(best_move, 0) + 2**depth
                    break

        if best_value <= alpha_orig:
            tt_flag = self.TT_UPPER_BOUND
        elif best_value >= beta_orig:
            tt_flag = self.TT_LOWER_BOUND
        else:
            tt_flag = self.TT_EXACT

        self.visited[gameboard.zobrist_hash] = best_value, best_move, depth, tt_flag

        return best_value, best_move


class Timeout(Exception):
    pass
