from enum import IntEnum
from helpers import generate_zobrist_table


type Move = tuple[int, int]

class Marker(IntEnum):
    EMPTY = 0
    PLAYER = 1
    AI = 2


class GameBoard:
    WIN_VALUE = 10000000
    OPEN_FOUR = 100000 * 2
    OPEN_THREE = 10000 * 2

    VALUES = {
        (5, 0): -10000000,
        (4, 0): -1000000,
        (3, 0): -100000,
        (2, 0): -1000,
        (1, 0): -10,
        (0, 5): 10000000,
        (0, 4): 100000,
        (0, 3): 1000,
        (0, 2): 100,
        (0, 1): 10
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
        marker = self.board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dx, dy in directions:
            count = 1

            c = col + dx
            r = row + dy
            while self.valid_coordinate(c, r) and self.board[r][c] == marker:
                count += 1
                c += dx
                r += dy

            c = col - dx
            r = row - dy
            while self.valid_coordinate(c, r) and self.board[r][c] == marker:
                count +=1
                c -= dx
                r -= dy

            if count >= 5:
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

            for i in range(-5, 6):
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
        Uses a sliding window algorithm to calculate the value of the given row.
        :param row: List of markers
        :return: Heuristic value of the row
        """
        row_value = 0
        row_len = len(row)
        if row_len < 5:
            return row_value

        player_count = 0
        ai_count = 0

        for i in range(5):
            if row[i] == Marker.PLAYER:
                player_count += 1
            elif row[i] == Marker.AI:
                ai_count += 1


        if (player_count > 0 and ai_count == 0) or (ai_count > 0 and player_count == 0):
            row_value += self.VALUES[(player_count, ai_count)]

        for i in range(5, row_len):
            removed_from_window = row[i-5]
            if removed_from_window == Marker.PLAYER:
                player_count -= 1
            elif removed_from_window == Marker.AI:
                ai_count -= 1

            added_to_window = row[i]
            if added_to_window == Marker.PLAYER:
                player_count += 1
            elif added_to_window == Marker.AI:
                ai_count += 1

            if player_count > 0 and ai_count > 0:
                continue

            row_value += self.VALUES.get((player_count, ai_count), 0)

        return row_value

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

    def update_candidates(self, candidates: set[Move], col: int, row: int) -> list[Move]:
        """
        Updates the candidates set by adding new candidates from the move (col, row).
        :param candidates: List of candidate moves
        :param col: Column of the board
        :param row: Row of the board
        :return: List of moves added to the candidates set
        """
        if (col, row) in candidates:
            candidates.remove((col, row))

        new_candidates = []

        for dx, dy in GameBoard.CANDIDATE_POSITIONS:
            mv_col = col + dx
            mv_row = row + dy

            if not self.valid_coordinate(mv_col, mv_row) or not self.empty_space(mv_col, mv_row):
                continue

            if (mv_col, mv_row) not in candidates:
                new_candidates.append((mv_col, mv_row))
                candidates.add((mv_col, mv_row))

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
