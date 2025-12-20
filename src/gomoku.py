from game_board import GameBoard, Marker, Move
from gomoku_ai import GomokuAI
from pygame_ui import PygameUI, UserEvent
from helpers import log


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

                    if isinstance(move, UserEvent):
                        if move == UserEvent.RESET:
                            self._reset()
                            game_over = True
                        continue
                    else:
                        col, row = move
                        self.gameboard.move(col, row, Marker.PLAYER)

                else:
                    board_copy = self.gameboard.clone_board()
                    candidates_copy = self.candidates.copy()
                    col, row = self.ui.get_ai_move(board_copy, self.ai, candidates_copy)
                    self.gameboard.move(col, row, Marker.AI)

                if self.gameboard.win_state():
                    winner = Marker.PLAYER if self.players_turn else Marker.AI
                    event = self.ui.show_winner(self.gameboard, winner)

                    if event == UserEvent.RESET:
                        self._reset()
                        game_over = True
                        continue
                    else:
                        return

                self.gameboard.update_candidates(self.candidates, col, row)
                self.ui.display_board(self.gameboard)


                if not self.players_turn:
                    self.turn_log()

                self.players_turn = not self.players_turn

    def turn_log(self) -> None:
        """Outputs details of the previous player and AI turn."""
        ai_col, ai_row = self.gameboard.move_history[-1]
        log(f"candidates: {self.candidates}")
        log(f"\nAI chose: ({chr(ord('A') + ai_col)}, {ai_row})\n")
        log(self.gameboard)
        log(f"history: {self.gameboard.move_history}")

