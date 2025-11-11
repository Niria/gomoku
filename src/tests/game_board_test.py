import unittest
from game_board import GameBoard, Markers


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.gameboard = GameBoard(20)

    def test_move_out_of_bounds_fails(self):
        moves = [
            (-1, 0),
            (0, -1),
            (-1, -1),
            (self.gameboard.size, 0),
            (0, self.gameboard.size),
            (self.gameboard.size, self.gameboard.size ),
        ]
        for x, y in moves:
            self.assertFalse(self.gameboard.move(x, y, Markers.PLAYER))

    def test_move_stored_to_history(self):
        self.gameboard.move(0, 0, Markers.PLAYER)
        self.assertEqual((0, 0), self.gameboard.move_history[-1])

    def test_undo_removes_from_history(self):
        self.gameboard.move(0, 0, Markers.PLAYER)
        self.gameboard.undo_move()
        self.assertListEqual([], self.gameboard.move_history)

    def test_win_state_returns_true(self):
        pass

    def test_win_state_returns_false(self):
        pass

    def test_valid_coordinate_returns_true(self):
        self.assertTrue(self.gameboard.valid_coordinate(0, 0))

    def test_valid_coordinate_returns_false(self):
        self.assertFalse(self.gameboard.valid_coordinate(-1, 0))