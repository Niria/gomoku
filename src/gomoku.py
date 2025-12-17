from game_board import GameBoard, Marker, Move
from gomoku_ai import GomokuAI
from pygame_ui import PygameUI

from stored_gamestates import GAME_STATES

class Gomoku:
    def __init__(self, size: int=20, player_starts: bool=True):
        self.size = size
        self.ui = PygameUI(size)
        self.player_starts = player_starts
        self._reset()

    def _reset(self) -> None:
        """
        Resets the game board state to its initial state.
        """
        self.gameboard = GameBoard(self.size)
        self.ai = GomokuAI()
        self.candidates: set[Move] = set()
        self.players_turn = self.player_starts
        self.ui.set_starting_player(self.player_starts)

    def run(self) -> None:
        """
        Runs the gomoku gameplay loop.
        """
        running = True
        while running:
            game_over = False
            self.ui.display_board(self.gameboard)

            ai_match = False

            while not game_over:
                if self.players_turn and not ai_match:
                    move = self.ui.get_player_move(self.gameboard)
                    if isinstance(move, str):
                        if move == "reset":
                            self._reset()
                            game_over = True
                            continue
                        elif move == "AI_match":
                            ai_match = True
                        elif move.startswith("game_"):
                            key = move.split("_")[1]
                            self.load_game(key)
                        continue

                    col, row = move
                    self.gameboard.move(col, row, Marker.PLAYER)

                else:
                    board_copy = self.gameboard.clone_board()
                    candidates_copy = self.candidates.copy()
                    curr_marker = Marker.PLAYER if self.players_turn else Marker.AI
                    col, row = self.ui.get_ai_move(board_copy, self.ai, candidates_copy, curr_marker)
                    self.gameboard.move(col, row, curr_marker)

                if self.gameboard.win_state():
                    winner = Marker.PLAYER if self.players_turn else Marker.AI
                    restart_game = self.ui.show_winner(self.gameboard, winner)

                    if restart_game:
                        self._reset()
                        game_over = True
                        continue
                    else:
                        return

                self.gameboard.update_candidates(self.candidates, col, row)
                self.ui.display_board(self.gameboard)

                print(f"candidates: {self.candidates} move: ({col}, {row})")

                if not self.players_turn:
                    print()
                    ai_col, ai_row = self.gameboard.move_history[-1]
                    print(f"AI chose: ({chr(ord("A")+ai_col)}, {ai_row})\n")
                    print(self.gameboard)
                self.players_turn = not self.players_turn
                print(f"history: {self.gameboard.move_history}")

    def load_game(self, state_key: str) -> None:
        """
        Loads a game state from stored_gamestates.py.
        :param state_key:
        :return:
        """
        if state_key not in GAME_STATES:
            return

        self._reset()
        moves = GAME_STATES[state_key]["moves"]

        print(moves[0])
        for col, row, marker in moves:
            self.gameboard.move(col, row, marker)
            self.gameboard.update_candidates(self.candidates, col, row)

        self.players_turn = GAME_STATES[state_key]["turn"] == Marker.PLAYER
        self.ui.display_board(self.gameboard)
