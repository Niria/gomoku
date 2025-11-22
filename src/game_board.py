from enum import IntEnum
from helpers import generate_zobrist_table


type Move = tuple[int, int]

class Marker(IntEnum):
    EMPTY = 0
    PLAYER = 1
    AI = 2


class GameBoard:
    WIN_VALUE = 10000000
    OPEN_FOUR = 1000000
    OPEN_THREE = 50000

    PATTERN_VALUES = {
        "11111": WIN_VALUE,
        "011110": OPEN_FOUR,
        "011112": 100000,
        "211110": 100000,
        "01111": 100000,
        "11110": 100000,
        "10111": 75000,
        "11011": 75000,
        "11101": 75000,
        "01110": OPEN_THREE,
        "0101010": 50000,
        "010110": 50000,
        "011010": 50000,
        "211100": 10000,
        "001112": 10000,
        "21110": 5000,
        "01112": 5000,
        "010112": 1000,
        "211010": 1000,
        "11000": 200,
        "00011": 200,
        "01100": 200,
        "00110": 200,
        "01010": 200,
        "10100": 200,
        "00101": 200,
        "000112": 50,
        "211000": 50,
        "211112": 40,
        "21112": 30,
        "00100": 10
    }
    SYMBOLS = {
        Marker.EMPTY: ".",
        Marker.PLAYER: "X",
        Marker.AI: "O",
    }


    CANDIDATE_POSITIONS = [(-1,-1), (1,-1), (-1,1), (1,1), (0,-1), (-1,0), (1,0), (0,1),
                            (-2,-2), (2,-2), (-2,2), (2,2), (0,-2), (-2,0), (2,0), (0,2)]

    def __init__(self, size: int):
        self.size = size
        self.board: list[list[Marker]] = [[Marker.EMPTY for _ in range(size)] for _ in range(size)]
        self.move_history: list[Move] = []
        self.zobrist_hash = 0
        self.zobrist_table: list[list[list[int]]] = generate_zobrist_table(size)
        self.player_patterns = self.precompute_player_patterns()
        self.ai_patterns = self.precompute_ai_patterns()

    def __str__(self) -> str:
        board = "    "
        board += " ".join([chr(n) for n in range(65,85)])
        board += "\n"
        for i,row in enumerate(self.board):
            board += f"{i:3} "
            for pos in row:
                board += self.SYMBOLS[pos] + " "
            board += "\n"
        return board

    def move(self, col: int, row: int, marker: Marker) -> None:
        """
        Places the given marker on the board at (col, row)
        :param col: Column of the board
        :param row: Row of the board
        :param marker: Player or AI marker
        :return: None
        """
        self.board[row][col] = marker
        self.move_history.append((col, row))
        self.update_hash(col, row, marker)

    def undo_move(self) -> None:
        """
        Undoes the latest move
        :return: None
        """
        if self.move_history:
            col, row = self.move_history[-1]
            marker = self.board[row][col]
            self.move_history.pop()
            self.update_hash(col, row, marker)
            self.board[row][col] = Marker.EMPTY

    def win_state(self) -> bool:
        """
        Checks if the latest move created a winning row
        :return: Bool
        """
        if not self.move_history:
            return False
        col, row = self.move_history[-1]
        rows = self.get_rows_containing_move(col, row)

        for row, _ in rows:
            if abs(self.get_row_value(row)) == self.WIN_VALUE:
                return True
        return False

    def get_move_value(self, col: int, row: int, marker: Marker) -> int:
        """
        Computes the value of placing a marker at location (col, row). This is done by
        calculating the initial value of the rows that contain the move without the marker.
        The same is repeated for all the rows, but this time with the marker placed at (col, row).
        The end result is the value with the marker placed subtracted by the value without it.
        :param col: Column of the board
        :param row: Row of the board
        :param marker: Player or AI marker
        :return: Heuristic value of the move
        """
        rows = self.get_rows_containing_move(col, row)

        current_value = 0
        for r, _ in rows:
            current_value += self.get_row_value(r)

        new_value = 0
        marker = int(marker)
        for r, idx in rows:
            r[idx] = marker
            new_value += self.get_row_value(r)

        return new_value - current_value

    def get_rows_containing_move(self, col: int, row: int) -> list[tuple[list[int], int]]:
        """
        Generates a list of rows that contain the move (col, row) and its index within the row.
        :param col: Column of the board
        :param row: Row of the board
        :return: List of rows and the index of the move
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        rows = []

        for dx, dy in directions:
            current_row = []
            mv_index = 0

            for i in range(-6, 7):
                if i == 0:
                    mv_index = len(current_row)
                c = col + i*dx
                r = row + i*dy
                if not self.valid_coordinate(c, r):
                    continue
                current_row.append(self.board[r][c])
            rows.append((current_row, mv_index))
        return rows

    def get_row_value(self, row: list[int]) -> int:
        """
        Computes the value of the given row
        :param row: List of empty, player and AI markers
        :return: Heuristic value of the given row
        """
        row = "".join(str(n) for n in row)
        player_value = 0
        ai_value = 0

        for pattern, value in self.player_patterns:
            if pattern in row:
                player_value = value
                break

        for pattern, value in self.ai_patterns:
            if pattern in row:
                ai_value = value
                break

        if player_value >= self.OPEN_THREE:
            return ai_value - int(player_value*4)
        else:
            return ai_value - int(player_value*1.2)

    def valid_move(self, col: int, row: int) -> bool:
        """
        Checks if the given move is within the board and the space is empty
        :param col: Column of the board
        :param row: Row of the board
        :return: Bool
        """
        return self.valid_coordinate(col, row) and self.empty_space(col, row)

    def valid_coordinate(self, col: int, row: int) -> bool:
        """
        Checks if the given coordinate is within the board
        :param col: Column of the board
        :param row: Row of the board
        :return: Bool
        """
        if col < 0 or col >= self.size or row < 0 or row >= self.size:
            return False
        return True

    def empty_space(self, col: int, row: int) -> bool:
        """
        Checks if the given coordinate is empty
        :param col: Column of the board
        :param row: Row of the board
        :return: Bool
        """
        return self.board[row][col] == Marker.EMPTY

    def get_candidates_set(self, candidates: set[Move], col: int, row: int) -> set[Move]:
        """
        Updates a list of candidate moves with new possible moves that are within 1 and 2 spaces
        of the latest move. A maximum of 16 moves are added to the candidate list, since only
        candidates that are on the same rows as the move are considered.
        :param candidates: List of candidate moves
        :param col: Column of the board
        :param row: Row of the board
        :return: List of candidate moves
        """
        new_candidates = candidates.copy()
        if (col, row) in new_candidates:
            new_candidates.remove((col, row))

        for dx, dy in GameBoard.CANDIDATE_POSITIONS:
            mv_col = col + dx
            mv_row = row + dy

            if not self.valid_coordinate(mv_col, mv_row) or not self.empty_space(mv_col, mv_row):
                continue
            new_candidates.add((mv_col, mv_row))

        return new_candidates

    def get_distance_to_prev_move(self, col: int, row: int) -> int:
        """
        Computes the Chebyshev distance between the latest move and a given move
        :param col: Column of the board
        :param row: Row of the board
        :return: Distance between the latest move and a given move
        """
        prev_col, prev_row = self.move_history[-1]
        distance = max(abs(prev_col - col), abs(prev_row - row))
        return distance

    def update_hash(self, col: int, row: int, marker: Marker) -> None:
        """
        Updates the zobrist_hash of the gameboard. The hash is a unique identifier for the game
        state.
        :param col: Column of the board
        :param row: Row of the board
        :param marker: Player or AI marker
        :return: None
        """
        self.zobrist_hash ^= self.zobrist_table[row][col][marker]

    def precompute_player_patterns(self) -> list[tuple[str, int]]:
        """
        Precomputes the patterns for identifying useful row states for the player.
        :return: List of (pattern, value) tuples
        """
        patterns = []
        for p, v in self.PATTERN_VALUES.items():
            patterns.append((p,v))
        patterns.sort(key=lambda x: x[1], reverse=True)

        return patterns

    def precompute_ai_patterns(self) -> list[tuple[str, int]]:
        """
        Precomputes the patterns for identifying useful row states for the AI.
        :return: List of (pattern, value) tuples
        """
        flip = {"0": "0", "1": "2", "2": "1"}
        patterns = []
        for p, v in self.PATTERN_VALUES.items():
            flipped_pattern = "".join([flip[c] for c in p])
            patterns.append((flipped_pattern, v))
        patterns.sort(key=lambda x: x[1], reverse=True)

        return patterns
