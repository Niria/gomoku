import unittest
from game_board import GameBoard, Marker
from gomoku_ai import GomokuAI


class TestGomokuAi(unittest.TestCase):
    def setUp(self):
        self.gameboard = GameBoard(size=20)
        self.ai = GomokuAI()
        self.candidates = set()

    def setup_board(self, moves: list[tuple[int, int, Marker]]) -> None:
        for col, row, marker in moves:
            self.gameboard.move(col, row, marker)
            self.gameboard.update_candidates(self.candidates, col, row)

    def test_AI_detects_horizontal_win(self):
        moves = [(5,5, Marker.AI), (6,5,Marker.AI), (7,5,Marker.AI), (8,5,Marker.AI)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 2)
        self.assertIn(move, [(4,5), (9,5)])

    def test_AI_detects_vertical_win(self):
        moves = [(5,5,Marker.AI), (5,6,Marker.AI), (5,7,Marker.AI), (5,8,Marker.AI)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 2)
        self.assertIn(move, [(5,4), (5,9)])

    def test_AI_detects_diagonal_win(self):
        moves = [(5,5,Marker.AI), (6,6,Marker.AI), (7,7,Marker.AI), (8,8,Marker.AI)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 2)
        self.assertIn(move, [(4,4), (9,9)])

    def test_AI_detects_reverse_diagonal_win(self):
        moves = [(5,5,Marker.AI), (4,6,Marker.AI), (3,7,Marker.AI), (2,8,Marker.AI)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 2)
        self.assertIn(move, [(6,4), (1,9)])

    def test_AI_blocks_player_open_three(self):
        moves = [(5,5,Marker.PLAYER), (6,5,Marker.PLAYER), (7,5,Marker.PLAYER)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 1)
        self.assertIn(move, [(4,5), (8,5)])

    def test_AI_blocks_player_split_three(self):
        moves = [(5,5,Marker.PLAYER), (6,5,Marker.PLAYER), (8,5,Marker.PLAYER)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 1)
        self.assertIn(move, [(4,5), (7,5), (9,5)])

    def test_AI_picks_win_over_block(self):
        moves = [(5,5,Marker.PLAYER), (6,5,Marker.PLAYER), (7,5,Marker.PLAYER), (8,5,Marker.PLAYER),
                 (5,7,Marker.AI), (6,7,Marker.AI), (7,7,Marker.AI), (8,7,Marker.AI)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 2)
        self.assertIn(move, [(4,7), (9,7)])

    def test_AI_blocks_open_three_over_making_own(self):
        moves = [(5,5,Marker.PLAYER), (6,5,Marker.PLAYER), (7,5,Marker.PLAYER),
                 (5,7,Marker.AI), (6,7,Marker.AI)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 2)
        self.assertIn(move, [(4,5), (8,5)])

    def test_AI_makes_open_four_over_blocked_four(self):
        moves = [(5,5,Marker.AI), (6,5,Marker.AI), (7,5,Marker.AI), (8,5,Marker.PLAYER),
                 (5,7,Marker.AI), (6,7,Marker.AI), (7,7,Marker.AI)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 2)
        self.assertIn(move, [(4,7), (8,7)])