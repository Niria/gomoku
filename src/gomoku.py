from game_board import GameBoard, Markers
import random


class Gomoku:
    def __init__(self, size=20):
        self.gameboard = GameBoard(size)
        self.players_turn = True
        self.current_value = 0
        self.valid_moves = []

    def run(self):
        while True:
            if self.players_turn:
                user_input = input("X Y: ")
                if user_input == "":
                    break

                col, row = [int(n) for n in user_input.split(" ")]
                valid_move = self.__player_move(col, row)

                if not valid_move:
                    print(f"Invalid input, X and Y must be between 0 and {self.gameboard.size - 1}")
                    continue

            else:
                col, row = random.choice(self.valid_moves)
                self.__ai_move(col, row)

            if self.gameboard.win_state():
                if self.players_turn:
                    print("Player won!")
                else:
                    print("AI won!")
                print(self.gameboard)
                break

            self.__update_valid_moves(col, row)
            if not self.players_turn:
                print(self.gameboard)
            self.players_turn = not self.players_turn

    def __update_valid_moves(self, col, row):
        if (col, row) in self.valid_moves:
            self.valid_moves.remove((col, row))

        for x in range (col-2, col+3):
            for y in range (row-2, row+3):
                if x == col and y == row:
                    continue
                if self.gameboard.valid_coordinate(x, y) and self.gameboard.empty_space(x, y):
                    self.valid_moves.append((x, y))

    def __player_move(self, col, row):
        return self.gameboard.move(col, row, Markers.PLAYER)

    def __ai_move(self, col, row):
        return self.gameboard.move(col, row, Markers.AI)


