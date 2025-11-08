from enum import IntEnum


class Markers(IntEnum):
    EMPTY = 0
    HUMAN = 1
    AI = 2


class GameBoard:
    SYMBOLS = {
        Markers.EMPTY: ".",
        Markers.HUMAN: "X",
        Markers.AI: "O"
    }

    def __init__(self, size):
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.move_history = []

    def __str__(self):
        board = ""
        for row in self.board:
            for pos in row:
                board += self.SYMBOLS[pos] + " "
            board += "\n"
        return board

    def move(self, col, row, marker):
        if self.valid_coordinate(col, row) and self.empty_space(col, row):
            self.board[row][col] = marker
            self.move_history.append((col, row))
            return True
        else:
            return False

    def undo_move(self):
        if self.move_history:
            col, row = self.move_history.pop()
            self.board[row][col] = 0

    def is_win_state(self):
        move_col, move_row = self.move_history[-1]
        marker = self.board[move_row][move_col]

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dx, dy in directions:
            marker_count = 1

            for i in range(1, 5):
                col = move_col + i*dx
                row = move_row + i*dy
                if not self.valid_coordinate(col, row) or self.board[row][col] != marker:
                    break
                marker_count += 1

            for i in range(1, 5):
                col = move_col - i*dx
                row = move_row - i*dy
                if not self.valid_coordinate(col, row) or self.board[row][col] != marker:
                    break
                marker_count += 1
            if marker_count >= 5:
                return True
        return False

    def get_children(self):
        pass

    def value(self):
        pass

    def valid_coordinate(self, col, row):
        if col < 0 or col >= self.size or row < 0 or row >= self.size:
            return False
        return True

    def empty_space(self, col, row):
        return self.board[row][col] == 0

