from enum import IntEnum


class Markers(IntEnum):
    EMPTY = 0
    PLAYER = 1
    AI = 2


class GameBoard:
    SYMBOLS = {
        Markers.EMPTY: ".",
        Markers.PLAYER: "X",
        Markers.AI: "O"
    }

    WIN_VALUE = 100

    VALUES = {
        "11111": 100,
        "011110": 80,
        "011112": 40,
        "211110": 40,
        "10111": 40,
        "11011": 40,
        "11101": 40,
        "01110": 25,
        "01011": 25,
        "01101": 25,
        "01010": 10,
        "01100": 10,
        "00110": 10
    }

    def __init__(self, size):
        self.size = size
        self.board = [[Markers.EMPTY for _ in range(size)] for _ in range(size)]
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
            self.board[row][col] = Markers.EMPTY

    def win_state(self):
        rows = self.get_rows_containing_move(*self.move_history[-1])

        for row in rows:
            if abs(self.get_row_value(row)) == self.WIN_VALUE:
                return True
        return False

    def get_rows_containing_move(self, col, row):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        rows = []
        move_col, move_row = col, row

        for dx, dy in directions:
            current_row = ""
            for i in range(-4, 5):
                col = move_col + i*dx
                row = move_row + i*dy
                if not self.valid_coordinate(col, row):
                    continue
                current_row += str(self.board[row][col])
            rows.append(current_row)
        return rows

    def get_children(self):
        pass

    def get_move_value(self, col, row, marker):
        rows = self.get_rows_containing_move(col, row)
        current_value = sum(self.get_row_value(row) for row in rows)

        self.board[row][col] = marker
        new_value = sum(self.get_row_value(row) for row in rows)
        self.board[row][col] = Markers.EMPTY

        return new_value - current_value

    def get_row_value(self, row):
        flip = {"0": "0", "1": "2", "2": "1"}
        human_value = 0
        ai_value = 0
        flipped_row = "".join([flip[c] for c in row])

        for pattern, value in self.VALUES.items():
            if pattern in row:
                human_value = -value
                break
            if pattern in flipped_row:
                ai_value = value
                break

        return ai_value - human_value


    def valid_coordinate(self, col, row):
        if col < 0 or col >= self.size or row < 0 or row >= self.size:
            return False
        return True

    def empty_space(self, col, row):
        return self.board[row][col] == 0

