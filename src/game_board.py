class GameBoard:
    SIZE = 20
    MARKERS = {
        0: ".",
        1: "X",
        2: "O"}

    def __init__(self):
        self.board = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.valid_moves = [(x, y) for x in range(self.SIZE) for y in range(self.SIZE)]
        self.move_history = []

    def __str__(self):
        board = ""
        for row in self.board:
            for cell in row:
                board += self.MARKERS[cell] + " "
            board += "\n"
        return board

    def move(self, x, y, marker):
        if self.__is_move_valid(x, y):
            self.board[y][x] = marker
            self.move_history.append((x, y))
            self.valid_moves.remove((x, y))
        else:
            raise ValueError("Invalid move")


    def is_win_state(self):
        move_col, move_row = self.move_history[-1]
        marker = self.board[move_row][move_col]

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dx, dy in directions:
            marker_count = 1

            for i in range(1, 5):
                col = move_col + i*dx
                row = move_row + i*dy
                if not self.__is_coordinate_valid(col, row) or self.board[row][col] != marker:
                    break
                marker_count += 1

            for i in range(1, 5):
                col = move_col - i*dx
                row = move_row - i*dy
                if not self.__is_coordinate_valid(col, row) or self.board[row][col] != marker:
                    break
                marker_count += 1

            if marker_count >= 5:
                return True

        return False

    def get_children(self):
        pass

    def value(self):
        pass

    def __is_move_valid(self, x, y):
        if not self.__is_coordinate_valid(x, y):
            return False
        if (x, y) not in self.valid_moves:
            return False
        return True

    def __is_coordinate_valid(self, x, y):
        if x < 0 or x >= self.SIZE or y < 0 or y >= self.SIZE:
            return False
        print(f"{x}, {y} is valid")
        return True
