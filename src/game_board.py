from enum import IntEnum
from helpers import generate_zobrist_table


type Move = tuple[int, int]

class Marker(IntEnum):
    EMPTY = 0
    PLAYER = 1
    AI = 2


class GameBoard:
    PATTERN_VALUES = {
        "11111": 10000000,
        "011110": 1000000,
        "011112": 100000,
        "211110": 100000,
        "01111": 100000,
        "10111": 100000,
        "11011": 100000,
        "11101": 100000,
        "11110": 100000,
        "01110": 50000,
        "010110": 50000,
        "011010": 50000,
        "21110": 10000,
        "01112": 10000,
        "010112": 1000,
        "211010": 1000,
        "11000": 200,
        "00011": 200,
        "01100": 200,
        "00110": 200,
        "01010": 200,
        "10100": 200,
        "00101": 200,
        "00112": 50,
        "21100": 50,
        "00100": 10,
        "1": 1
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
        self.board[row][col] = marker
        self.move_history.append((col, row))
        self.update_hash(col, row, marker)

    def undo_move(self) -> None:
        if self.move_history:
            col, row = self.move_history[-1]
            marker = self.board[row][col]
            self.move_history.pop()
            self.update_hash(col, row, marker)
            self.board[row][col] = Marker.EMPTY

    def win_state(self) -> bool:
        if not self.move_history:
            return False
        col, row = self.move_history[-1]
        rows = self.get_rows_containing_move(col, row)

        for row in rows:
            if abs(self.get_row_value(row)) == self.PATTERN_VALUES["11111"]:
                return True
        return False

    def get_move_value(self, col: int, row: int, marker: Marker) -> int:
        rows = self.get_rows_containing_move(col, row)
        current_value = sum(self.get_row_value(r) for r in rows)

        self.board[row][col] = marker
        rows = self.get_rows_containing_move(col, row)
        new_value = sum(self.get_row_value(r) for r in rows)
        self.board[row][col] = Marker.EMPTY
        # print(f"move: ({col}, {row}) move_value: {new_value - current_value}")
        return new_value - current_value

    def get_rows_containing_move(self, col: int, row: int) -> list[list[int]]:
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        rows = []
        move_col, move_row = col, row

        for dx, dy in directions:
            current_row = []
            for i in range(-4, 5):
                col = move_col + i*dx
                row = move_row + i*dy
                if not self.valid_coordinate(col, row):
                    continue
                current_row.append(self.board[row][col])
            rows.append(current_row)
        return rows

    def get_row_value(self, row: list[int]) -> int:
        row = "".join(str(n) for n in row)
        flip = {"0": "0", "1": "2", "2": "1"}
        player_value = 0
        ai_value = 0
        flipped_row = "".join([flip[c] for c in row])
        for pattern, value in self.PATTERN_VALUES.items():
            if pattern in row:
                player_value = value
                break

        for pattern, value in self.PATTERN_VALUES.items():
            if pattern in flipped_row:
                ai_value = value
                break
        # print(f"row: {row} value: {ai_value-player_value}")
        return ai_value - player_value

    def valid_move(self, col: int, row: int) -> bool:
        return self.valid_coordinate(col, row) and self.empty_space(col, row)

    def valid_coordinate(self, col: int, row: int) -> bool:
        if col < 0 or col >= self.size or row < 0 or row >= self.size:
            return False
        return True

    def empty_space(self, col: int, row: int) -> bool:
        return self.board[row][col] == Marker.EMPTY

    # Old spatial move ordering based on previous move
    def get_candidates(self, curr_candidates: list[Move], col, row) -> list[Move]:
        candidates = curr_candidates.copy()
        new_candidates = []

        if (col, row) in curr_candidates:
            candidates.remove((col, row))

        for dx, dy in GameBoard.CANDIDATE_POSITIONS:
            mv_col = col + dx
            mv_row = row + dy

            if not self.valid_coordinate(mv_col, mv_row) or not self.empty_space(mv_col, mv_row):
                continue

            if (mv_col, mv_row) in candidates:
                candidates.remove((mv_col, mv_row))
            new_candidates.append((mv_col, mv_row))

        return new_candidates + candidates

    # New value based move ordering
    def get_candidates_set(self, candidates: set[Move], col: int, row: int) -> set[Move]:
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


    def update_hash(self, col: int, row: int, marker: Marker):
        self.zobrist_hash ^= self.zobrist_table[row][col][marker]
