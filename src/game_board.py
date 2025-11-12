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

    VALUES = {
        "11111": 100000,
        "011110": 50000,
        "011112": 5000,
        "211110": 5000,
        "10111": 1000,
        "11011": 1000,
        "11101": 1000,
        "01110": 200,
        "01011": 200,
        "01101": 200,
        "21110": 100,
        "01112": 100,
        "01010": 50,
        "01100": 50,
        "00110": 50,
        "00100": 20,
        "01": 10,
        "10": 10
    }

    VALID_MOVE_POSITIONS = [(-1,-1), (1,-1), (-1,1), (1,1), (0,-1), (-1,0), (1,0), (0,1),
                            (-2,-2), (2,-2), (-2,2), (2,2), (0,-2), (-2,0), (2,0), (0,2)]

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
        self.board[row][col] = marker
        self.move_history.append((col, row))

    def undo_move(self):
        if self.move_history:
            col, row = self.move_history.pop()
            self.board[row][col] = Markers.EMPTY

    def win_state(self):
        rows = self.get_rows_containing_move(*self.move_history[-1])

        for row in rows:
            if abs(self.get_row_value(row)) == self.VALUES["11111"]:
                return True
        return False

    def get_move_value(self, col, row, marker):
        rows = self.get_rows_containing_move(col, row)
        current_value = sum(self.get_row_value(r) for r in rows)

        self.board[row][col] = marker
        rows = self.get_rows_containing_move(col, row)
        new_value = sum(self.get_row_value(r) for r in rows)
        self.board[row][col] = Markers.EMPTY

        # print(f"Move value: {new_value-current_value} for {marker}")
        return new_value - current_value

    def get_rows_containing_move(self, col, row):
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

    def get_row_value(self, row):
        row = "".join(str(n) for n in row)
        flip = {"0": "0", "1": "2", "2": "1"}
        player_value = 0
        ai_value = 0
        flipped_row = "".join([flip[c] for c in row])
        for pattern, value in self.VALUES.items():
            if pattern in row:
                player_value = value
                break

        for pattern, value in self.VALUES.items():
            if pattern in flipped_row:
                ai_value = value
                break
        return ai_value - player_value

    def valid_move(self, col, row):
        return self.valid_coordinate(col, row) and self.empty_space(col, row)

    def valid_coordinate(self, col, row):
        if col < 0 or col >= self.size or row < 0 or row >= self.size:
            return False
        return True

    def empty_space(self, col, row):
        return self.board[row][col] == Markers.EMPTY

    def get_valid_moves(self, curr_valid_moves, col, row):
        valid_moves = curr_valid_moves.copy()
        new_moves = []

        if (col, row) in curr_valid_moves:
            valid_moves.remove((col, row))

        for dx, dy in GameBoard.VALID_MOVE_POSITIONS:
            move_col = col + dx
            move_row = row + dy

            if not self.valid_coordinate(move_col, move_row) or not self.empty_space(move_col, move_row):
                continue

            if (move_col, move_row) in valid_moves:
                valid_moves.remove((move_col, move_row))
            new_moves.append((move_col, move_row))

        return new_moves + valid_moves



    # def get_valid_moves(self, curr_valid_moves, col, row):
    #     valid_moves = curr_valid_moves.copy()
    #     if (col, row) in valid_moves:
    #         valid_moves.remove((col, row))
    #     for x in range (col-2, col+3):
    #         for y in range (row-2, row+3):
    #             if x == col and y == row:
    #                 continue
    #             if self.valid_coordinate(x, y) and self.empty_space(x, y) and (x, y) not in valid_moves:
    #                 valid_moves.append((x, y))
    #     return valid_moves