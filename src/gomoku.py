from game_board import GameBoard, Marker, Move
from gomoku_ai import GomokuAI
from helpers import char_to_number


class Gomoku:
    def __init__(self, size=20):
        self.gameboard = GameBoard(size)
        self.ai = GomokuAI()
        self.players_turn = True
        self.current_value = 0
        self.candidates: set[Move] = set()


    def run(self) -> None:
        """
        Runs the gomoku gameplay loop.
        :return:
        """
        print(self.gameboard)
        print()

        while True:
            if self.players_turn:
                user_input = input("X Y: ")
                if user_input == "":
                    break

                try:
                    col, row = user_input.split(" ")
                    col = char_to_number(col)
                    row = int(row)
                except ValueError:
                    print("Invalid input, X and Y must be between 0 and {self.gameboard.size - 1}")
                    break

                if not self.gameboard.valid_move(col, row):
                    print(f"Invalid input, X and Y must be between 0 and {self.gameboard.size - 1}")
                    continue
                print(f"value before player: {self.current_value}")
                self.current_value += self.gameboard.get_move_value(col, row, Marker.PLAYER)
                print(f"value after player: {self.current_value}")
                # print(f"curr value: {self.current_value}")

                self.gameboard.move(col, row, Marker.PLAYER)

            else:
                col, row = self.ai.find_ai_move(self.gameboard, self.candidates, self.current_value)
                print(f"value before AI: {self.current_value}")
                self.current_value += self.gameboard.get_move_value(col, row, Marker.AI)
                print(f"value after AI: {self.current_value}")
                self.gameboard.move(col, row, Marker.AI)

            if self.gameboard.win_state():
                if self.players_turn:
                    print("Player won!")
                else:
                    print("AI won!")
                print(self.gameboard)
                break

            self.candidates = self.gameboard.get_candidates_set(self.candidates, col, row)

            if not self.players_turn:
                print()
                ai_col, ai_row = self.gameboard.move_history[-1]
                print(f"AI chose: ({chr(ord("A")+ai_col)}, {ai_row})\n")
                print(self.gameboard)
            self.players_turn = not self.players_turn
            print(f"history: {self.gameboard.move_history}")
