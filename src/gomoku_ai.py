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

        winning_move = None
        if prev_best_move and prev_best_move in candidates:
            col, row = prev_best_move
            prev_best_value = gameboard.get_move_value(col, row, marker)
            if maximizing and prev_best_value >= gameboard.WIN_VALUE * 0.9:
                winning_move = (prev_best_move, prev_best_value)
            else:
                sorted_candidates.append((prev_best_move, prev_best_value, 0))

        if not winning_move:
            for move in candidates:
                if move == prev_best_move:
                    continue
                col, row = move
                mv_value = gameboard.get_move_value(col, row, marker)

                is_win = (mv_value >= gameboard.WIN_VALUE) if maximizing else \
                    (mv_value <= -gameboard.WIN_VALUE)
                if is_win:
                    return (parent_value + mv_value), move

                mv_distance = gameboard.get_distance_to_prev_move(col, row)
                sorted_candidates.append((move, mv_value, mv_distance))

        if winning_move:
            best_move = winning_move[0]
            value = parent_value + winning_move[1]
            self.visited[gameboard.zobrist_hash] = value, best_move, depth, self.TT_EXACT
            return value, best_move

        if maximizing:
            sorted_candidates.sort(key=lambda x: (x[1], -x[2]), reverse=True)
        else:
            sorted_candidates.sort(key=lambda x: (x[1], x[2]), reverse=False)

        if depth >= 3:
            max_branches = 18
        else:
            max_branches = 12
        if len(sorted_candidates) > max_branches:
            sorted_candidates = sorted_candidates[:max_branches]

        best_move = None
        best_value = float('-inf') if maximizing else float('inf')

        for move, move_value, _ in sorted_candidates:
            col, row = move
            new_value = parent_value + move_value

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

            if maximizing:
                if value > best_value:
                    best_value = value
                    best_move = move

                    if depth == root_depth:
                        self.best_move_before_timeout = best_move

                alpha = max(alpha, best_value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, best_value)

            if alpha >= beta:
                flag = self.TT_LOWER_BOUND if maximizing else self.TT_UPPER_BOUND
                self.visited[gameboard.zobrist_hash] = best_value, best_move, depth, flag
                break
        else:
            if best_value <= alpha_orig:
                flag = self.TT_UPPER_BOUND
            else:
                flag = self.TT_EXACT

            self.visited[gameboard.zobrist_hash] = best_value, best_move, depth, flag

        return best_value, best_move


class Timeout(Exception):
    pass
