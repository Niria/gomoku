import unittest
from game_board import GameBoard, Marker
from gomoku_ai import GomokuAI
import time


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

    def test_AI_blocks_player_blocked_four(self):
        moves = [(5,5,Marker.PLAYER), (6,5,Marker.PLAYER), (7,5,Marker.PLAYER), (8,5,Marker.PLAYER),
                 (9,5,Marker.AI)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 2)
        self.assertEqual(move, (4,5))

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

    def test_AI_does_not_pick_winning_move_outside_board(self):
        moves = [(0,5,Marker.AI), (1,5,Marker.AI), (2,5,Marker.AI), (3,5,Marker.AI)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 2)
        self.assertEqual(move, (4,5))

    def test_AI_does_not_pick_blocking_move_outside_board(self):
        moves = [(0,0,Marker.PLAYER), (1,1,Marker.PLAYER), (2,2,Marker.PLAYER), (3,3,Marker.PLAYER)]
        self.setup_board(moves)
        move = self.ai.find_ai_move(self.gameboard, self.candidates, 2)
        self.assertEqual(move, (4,4))

    def test_AI_finds_win_at_depth_5(self):
        """
        Checks that the AI is able to notice a sequence of moves that guarantees win 5 turns later.
        The initial board state actually has two possible win sequences for the AI, but since the
        move ordering is in this test case based only on distance from last move the AI picks (8,5)
        first over (8,8).
        """

        # Initial board state:     AI win board state:
        #   2 3 4 5 6 7 8 9 10       2 3 4 5 6 7 8 9 10
        # 3 . . . . . . . . .      3 . . . . . . . . .
        # 4 . . . . . O X . .      4 . . . . . O X . .
        # 5 . . X O O O . . .      5 . . X O O O O X .
        # 6 . . . X X X O . .      6 . . . X X X O . .
        # 7 . . X X . X O . .      7 . . X X . X O . .
        # 8 . X . O O O . X .      8 . X O O O O O X .
        # 9 . . . . . . . . .      9 . . . . . . X . .
        #10 . . . . . . X . .     10 . . . . . . X . .
        #11 . . . . . . . . .     11 . . . . . . . . .

        # AI win sequence:
        # 1. AI (8,5) creates blocked 4 (row 5) and blocked 3 (col 8)
        # 2. Player (9,5) stops AI blocked 4 (row 5)
        # 3. AI (8,8) creates blocked 4 (col 8)
        # 4. Player (8,9) stops AI blocked 4 (col 8)
        # 5. AI (4,8) creates 5 in a row and wins (row 8)


        moves = [(7,4,Marker.AI), (5,5,Marker.AI), (6,5,Marker.AI),
                 (7,5,Marker.AI), (8,6,Marker.AI), (8,7,Marker.AI),
                 (5,8,Marker.AI), (6,8,Marker.AI), (7,8,Marker.AI),
                 (9,8,Marker.PLAYER), (4,5,Marker.PLAYER), (5,6,Marker.PLAYER),
                 (6,6,Marker.PLAYER), (7,6,Marker.PLAYER), (4,7,Marker.PLAYER),
                 (8,10,Marker.PLAYER), (7,7,Marker.PLAYER), (3,8,Marker.PLAYER),
                 (8,4,Marker.PLAYER)]
        self.setup_board(moves)

        mv1 = self.ai.find_ai_move(self.gameboard, self.candidates, 10.0)
        self.assertEqual(mv1, (8,5))

        self.setup_board([(8,5,Marker.AI), (9,5,Marker.PLAYER)])

        mv2 = self.ai.find_ai_move(self.gameboard, self.candidates, 10.0)
        self.assertEqual(mv2, (8,8))

        self.setup_board([(8,8,Marker.AI), (8,9,Marker.PLAYER)])

        mv3 = self.ai.find_ai_move(self.gameboard, self.candidates, 10.0)
        self.assertEqual(mv3, (4,8))

        self.setup_board([(4,8,Marker.AI)])
        self.assertTrue(self.gameboard.win_state())

    def test_minimax_maximizes_in_max(self):
        current_state_value = 0
        alpha = float('-inf')
        beta = float('inf')
        moves = [(3,3,Marker.AI), (4,3,Marker.AI), (5,3,Marker.AI)]
        self.setup_board(moves)

        value, move = self.ai.minimax(self.gameboard, alpha, beta, True, self.candidates,
                                   current_state_value, 5, time.time(), 10.0, 5)
        self.assertGreater(value, 0)
        self.assertIn(move, [(2,3), (6,3)])

    def test_minimax_minimizes_in_min(self):
        current_state_value = 0
        alpha = float('-inf')
        beta = float('inf')
        moves = [(3,3,Marker.PLAYER), (4,3,Marker.PLAYER), (5,3,Marker.PLAYER)]
        self.setup_board(moves)

        value, move = self.ai.minimax(self.gameboard, alpha, beta, False, self.candidates,
                                   current_state_value, 5, time.time(), 10.0, 5)
        self.assertLess(value, 0)
        self.assertIn(move, [(2,3), (6,3)])
