from typing import Optional
import pygame
from pygame import gfxdraw
import threading
import sys
from game_board import GameBoard, Marker, Move
from gomoku_ai import GomokuAI


class PygameUI:
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)

    def __init__(self, size=20):
        pygame.init()
        self.board_size = size
        self.grid_width = 40
        self.board_padding = 40
        self.board_width = size * self.grid_width
        self.board_height = size * self.grid_width
        self.display_width = self.board_width + 2*self.board_padding
        self.display_height = self.board_height + 2*self.board_padding
        self.marker_size = 36
        self.background_colour = (190, 150, 105)
        self.marker_colours = {}

        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Gomoku")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

    def _draw_board(self, gameboard: GameBoard) -> None:
        """
        Draws the board background, gridlines and player markers.
        :param gameboard: Instance of GameBoard
        :return:
        """
        self.display.fill(self.background_colour)
        self._draw_grid()
        self._draw_markers(gameboard)


    def _draw_grid(self) -> None:
        """
        Draws the gridlines.
        :return:
        """
        for i in range(self.board_size):
            pos = i * self.grid_width
            offset = self.grid_width // 2 + self.board_padding
            pygame.draw.line(self.display, (0,0,0), (offset, pos+offset), (self.display_width-offset, pos+offset), 2)
            pygame.draw.line(self.display, (0,0,0), (pos+offset, offset), (pos+offset, self.display_height-offset), 2)

    def _draw_markers(self, gameboard: GameBoard) -> None:
        """
        Draws the player markers.
        :param gameboard: Instance of GameBoard
        :return:
        """
        for row in range(self.board_size):
            for col in range(self.board_size):
                marker = gameboard.board[row][col]
                if marker != Marker.EMPTY:
                    x = col * self.grid_width + self.grid_width // 2 + self.board_padding
                    y = row * self.grid_width + self.grid_width // 2 + self.board_padding

                    if (col, row) == gameboard.move_history[-1]:
                        gfxdraw.aacircle(self.display, x, y, self.marker_size//2+3, (200, 0, 0))
                        gfxdraw.filled_circle(self.display, x, y, self.marker_size//2+3, (200, 0, 0))

                    # color = self.COLORS[marker]
                    color = self.marker_colours[marker]
                    gfxdraw.aacircle(self.display, x, y, self.marker_size//2, color)
                    gfxdraw.filled_circle(self.display, x, y, self.marker_size//2, color)

    def display_board(self, gameboard: GameBoard) -> None:
        """
        Displays the gameboard in the pygame window.
        :param gameboard: Instance of GameBoard
        :return:
        """
        self._event_loop()
        self._draw_board(gameboard)
        pygame.display.flip()

    def get_player_move(self, gameboard: GameBoard) -> Move:
        """
        Gets the player's next move. Returns the move the player clicks a valid empty space on the board.
        :param gameboard: Instance of GameBoard
        :return: Player's next move
        """
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    col = (x - self.board_padding) // self.grid_width
                    row = (y - self.board_padding) // self.grid_width

                    if gameboard.valid_move(col, row):
                        return col, row
                    else:
                        print(f"Invalid move! {col}, {row}")

    def get_ai_move(self, gameboard: GameBoard, ai: GomokuAI, candidates: set[Move]) -> Move:
        """
        Gets the AI's next move. Starts a new thread for running the AI to
        prevent pygame from freezing.
        :param gameboard: Instance of GameBoard
        :param ai: Instance of GomokuAI
        :param candidates: Set of candidate moves
        :return: AI's next move
        """
        ai_move = []
        thread = threading.Thread(target=self._ai_thread, args=(gameboard, ai, candidates, ai_move))
        thread.daemon = True
        thread.start()

        while thread.is_alive():
            self._event_loop()
            self.clock.tick(60)

        return ai_move[0]

    def _ai_thread(self, gameboard: GameBoard, ai: GomokuAI, candidates: set[Move], move: list[Move]) -> None:
        """
        Helper method for running find_ai_move in a thread.
        :param gameboard: Instance of GameBoard
        :param ai: Instance of GomokuAI
        :param candidates: Set of candidate moves
        :param move: Mutable list for storing the result
        """
        move.append(ai.find_ai_move(gameboard, candidates))

    def show_winner(self, gameboard: GameBoard, winner: Marker) -> Optional[bool]:
        """
        Displays the winner of the game in the pygame window.
        :param gameboard: Instance of GameBoard
        :param winner: The winner of the game
        :return: Returns True if player decides to restart game.
        """
        self.display_board(gameboard)
        restart_st = " Press R to restart, Q to quit"
        player_st = "Player won!" if winner == Marker.PLAYER else "AI won!"
        game_over_text = self.font.render(player_st+restart_st, True, (0,0,0))
        self.display.blit(game_over_text, (self.board_padding, self.board_padding//2))
        pygame.display.flip()

        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit(0)

    def set_starting_player(self, player_starts: bool) -> None:
        """
        Initializes the marker colours based on who starts the game.
        """
        if player_starts:
            self.marker_colours = {
                Marker.PLAYER: self.COLOR_BLACK,
                Marker.AI: self.COLOR_WHITE
            }
        else :
            self.marker_colours = {
                Marker.PLAYER: self.COLOR_WHITE,
                Marker.AI: self.COLOR_BLACK
            }


    def _event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
