import unittest
from game_board import GameBoard, Marker


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.gameboard = GameBoard(20)

    def test_move_stored_to_history(self):
        self.gameboard.move(0, 0, Marker.PLAYER)
        self.assertEqual((0, 0), self.gameboard.move_history[-1])

    def test_undo_removes_from_history(self):
        self.gameboard.move(0, 0, Marker.PLAYER)
        self.gameboard.undo_move()
        self.assertListEqual([], self.gameboard.move_history)

    def test_win_state_win_returns_true(self):
        self.gameboard.board[5][5] = Marker.PLAYER
        self.gameboard.board[6][6] = Marker.PLAYER
        self.gameboard.board[7][7] = Marker.PLAYER
        self.gameboard.board[8][8] = Marker.PLAYER
        self.gameboard.board[9][9] = Marker.PLAYER

        self.gameboard.move_history.append((9, 9))

        self.assertTrue(self.gameboard.win_state())

    def test_win_state_no_win_returns_false(self):
        self.gameboard.board[5][5] = Marker.PLAYER
        self.gameboard.board[6][6] = Marker.PLAYER
        self.gameboard.board[7][7] = Marker.PLAYER
        self.gameboard.board[9][9] = Marker.PLAYER
        self.gameboard.board[10][10] = Marker.PLAYER

        self.gameboard.move_history.append((9, 9))

        self.assertFalse(self.gameboard.win_state())

    def test_win_state_empty_history_returns_false(self):
        self.assertFalse(self.gameboard.win_state())

    def test_move_value_returns_correct_value(self):
        self.gameboard.board[3][5] = Marker.PLAYER
        self.gameboard.board[3][6] = Marker.PLAYER
        self.gameboard.board[3][7] = Marker.PLAYER
        self.gameboard.board[4][7] = Marker.AI
        self.gameboard.board[4][8] = Marker.AI

        # Rows pre move:       post move:
        # [0,0,0,0,2,0,0,0]    [0,0,0,2,2,0,0,0]
        # [0,1,1,1,0,0,0,0,0]  [0,1,1,1,2,0,0,0,0]
        # [0,0,0,0,0,0,0,0]    [0,0,0,2,0,0,0,0]
        # [0,0,0,2,0,0,0,0]    [0,0,0,2,2,0,0,0]

        old_value = 2*GameBoard.PATTERN_VALUES["00100"] - GameBoard.PATTERN_VALUES["01110"]
        new_value = (2*GameBoard.PATTERN_VALUES["11000"] - GameBoard.PATTERN_VALUES["01112"]
                     + GameBoard.PATTERN_VALUES["1"] + GameBoard.PATTERN_VALUES["00100"])
        correct_value = new_value - old_value

        self.assertEqual(correct_value, self.gameboard.get_move_value(8, 3, Marker.AI))

    def test_get_rows_containing_move_returns_correct_rows(self):
        self.gameboard.board[3][5] = Marker.PLAYER
        self.gameboard.board[3][6] = Marker.PLAYER
        self.gameboard.board[3][7] = Marker.PLAYER
        self.gameboard.board[4][7] = Marker.AI
        self.gameboard.board[4][8] = Marker.AI

        correct_rows = [
            [0,0,0,0,2,0,0,0],
            [0,1,1,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,2,0,0,0,0]
        ]
        rows = self.gameboard.get_rows_containing_move(8, 3)
        for i,row in enumerate(rows):
            self.assertListEqual(correct_rows[i], [int(i) for i in row])

    def test_get_row_value_returns_correct_value(self):
        row = [0, 2, 2, 2, 0]
        self.assertEqual(GameBoard.PATTERN_VALUES["01110"], self.gameboard.get_row_value(row))

    def test_valid_move_returns_true(self):
        self.assertTrue(self.gameboard.valid_move(0, 0))

    def test_valid_move_space_not_empty_returns_false(self):
        self.gameboard.board[5][5] = Marker.PLAYER
        self.assertFalse(self.gameboard.valid_move(5, 5))

    def test_valid_coordinate_out_of_bounds_returns_false(self):
        moves = [
            (-1, 0),
            (0, -1),
            (-1, -1),
            (self.gameboard.size, 0),
            (0, self.gameboard.size),
            (self.gameboard.size, self.gameboard.size),
        ]
        for x, y in moves:
            self.assertFalse(self.gameboard.valid_coordinate(x, y))

    def test_valid_coordinate_in_bounds_returns_true(self):
        self.assertTrue(self.gameboard.valid_coordinate(0, 0))

    def test_get_candidates_returns_correct_list(self):
        self.gameboard.board[5][5] = Marker.PLAYER
        old_candidates = [(4,5), (10,10), (3,4)]
        real_candidates = [(3,4), (5,4), (3,6), (5,6), (4,4), (3,5), (4,6), (2,3), (6,3), (2,7), (6,7), (4,3), (2,5), (6,5), (4,7), (10,10)]
        self.assertListEqual(real_candidates, self.gameboard.get_candidates(old_candidates, 4, 5))

    def test_get_candidates_set_returns_correct_set(self):
        self.gameboard.board[5][5] = Marker.PLAYER
        old_candidates = {(5,5), (4,5)}
        real_candidates = {(3,4), (5,4), (3,6), (5,6), (4,4), (3,5), (4,6), (2,3), (6,3), (2,7), (6,7), (4,3), (2,5), (6,5), (4,7), (5,5)}
        self.assertSetEqual(real_candidates, self.gameboard.get_candidates_set(old_candidates, 4, 5))
