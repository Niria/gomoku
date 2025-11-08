from game_board import GameBoard, Markers
import random


class Gomoku:
    def __init__(self, size=20):
        self.gameboard = GameBoard(size)
        self.valid_moves = []

    def run(self):
        while True:
            user_input = input("X Y: ")
            if user_input == "":
                break
            col, row = [int(n) for n in user_input.split(" ")]
            valid_move = self.gameboard.move(col, row, Markers.HUMAN)
            if not valid_move:
                print(f"Invalid input, X and Y must be between 0 and {self.gameboard.size - 1}")
                continue
            self.__update_valid_moves(col, row)
            if self.gameboard.win_state():
                print("Player won!")
                print(self.gameboard)
                break
            else:
                # Currently the AI just randomly picks a space
                ai_x, ai_y = random.choice(self.valid_moves)
                self.gameboard.move(ai_x, ai_y, Markers.AI)
                print(f"Player placed X to ({col}, {row}), AI placed O to ({ai_x}, {ai_y})")
            print(self.gameboard)

    def __update_valid_moves(self, col, row):
        if (col, row) in self.valid_moves:
            self.valid_moves.remove((col, row))

        for x in range (col-2, col+3):
            for y in range (row-2, row+3):
                if x == col and y == row:
                    continue
                if self.gameboard.valid_coordinate(x, y) and self.gameboard.empty_space(x, y):
                    self.valid_moves.append((x, y))







