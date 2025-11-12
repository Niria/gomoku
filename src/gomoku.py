from game_board import GameBoard, Markers
from gomoku_ai import GomokuAI
from helpers import generate_zobrist_table


class Gomoku:
    def __init__(self, size=20):
        self.gameboard = GameBoard(size)
        self.ai = GomokuAI(size)
        self.players_turn = True
        self.current_value = 0
        self.valid_moves = []

        self.zobrist_table = generate_zobrist_table(size)
        self.gameboard_values = {}

    def run(self):
        while True:
            if self.players_turn:
                user_input = input("X Y: ")
                if user_input == "":
                    break

                col, row = [int(n) for n in user_input.split(" ")]

                if not self.gameboard.valid_move(col, row):
                    print(f"Invalid input, X and Y must be between 0 and {self.gameboard.size - 1}")
                    continue

                self.current_value += self.gameboard.get_move_value(col, row, Markers.PLAYER)

                print(f"curr value: {self.current_value}")

                self.gameboard.move(col, row, Markers.PLAYER)
                self.ai.update_hash(col, row, Markers.PLAYER)

            else:
                # col, row = random.choice(self.valid_moves)
                col, row = self.ai.find_ai_move(self.gameboard, self.valid_moves, self.current_value)
                self.current_value += self.gameboard.get_move_value(col, row, Markers.AI)
                self.gameboard.move(col, row, Markers.AI)
                self.ai.update_hash(col, row, Markers.AI)

            if self.gameboard.win_state():
                if self.players_turn:
                    print("Player won!")
                else:
                    print("AI won!")
                print(self.gameboard)
                break

            self.valid_moves = self.gameboard.get_valid_moves(self.valid_moves, col, row)

            if not self.players_turn:
                print(self.gameboard)
            self.players_turn = not self.players_turn
            print(self.gameboard.move_history)
