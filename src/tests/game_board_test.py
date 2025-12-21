import random
import unittest

from game_board import GameBoard, Marker

random.seed(42)


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.gameboard = GameBoard(20)

    def calculate_static_board_heuristic_value(self) -> int:
        """
        Helper method for calculating the static heuristic value of the entire board.
        """
        heuristic_value = 0
        size = self.gameboard.size

        for row in self.gameboard.board:
            heuristic_value += self.gameboard.get_row_value(row)

        for col in range(size):
            column = [self.gameboard.board[row][col] for row in range(size)]
            heuristic_value += self.gameboard.get_row_value(column)

        diag_starts = [(0, col) for col in range(size)] + \
                      [(row, 0) for row in range(1, size)]

        for start_row, start_col in diag_starts:
            line = []
            r, c = start_row, start_col
            while r < size and c < size:
                line.append(self.gameboard.board[r][c])
                r += 1
                c += 1
            heuristic_value += self.gameboard.get_row_value(line)

        reverse_diag_starts = [(0, col) for col in range(size)] + \
                              [(row, size - 1) for row in range(1, size)]

        for start_row, start_col in reverse_diag_starts:
            line = []
            r, c = start_row, start_col
            while r < size and c >= 0:
                line.append(self.gameboard.board[r][c])
                r += 1
                c -= 1
            heuristic_value += self.gameboard.get_row_value(line)

        return heuristic_value

    def test_move_updates_board_state(self):
        self.gameboard.move(0, 0, Marker.PLAYER)
        self.gameboard.move(8, 19, Marker.AI)

        self.assertEqual(self.gameboard.board[0][0], Marker.PLAYER)
        self.assertEqual(self.gameboard.board[19][8], Marker.AI)

    def test_undo_updates_board_state(self):
        self.gameboard.move(0, 0, Marker.PLAYER)
        self.gameboard.undo_move()

        self.assertEqual(self.gameboard.board[0][0], Marker.EMPTY)

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

        old_value = -GameBoard.PATTERN_VALUES["01110"] * 4
        new_value = (2 * GameBoard.PATTERN_VALUES["01100"] - GameBoard.PATTERN_VALUES["00111"] * 2)
        correct_value = new_value - old_value

        self.assertEqual(correct_value, self.gameboard.get_move_value(8, 3, Marker.AI))

    def test_incremental_move_value_heuristic_matches_static_board_heuristic(self):
        current_value = 0
        moves = [(c, r) for c in range(20) for r in range(20)]
        random.shuffle(moves)

        for i, move in enumerate(moves):
            col, row = move

            marker = Marker.PLAYER if i % 2 == 0 else Marker.AI
            delta = self.gameboard.get_move_value(col, row, marker)
            self.gameboard.move(col, row, marker)
            current_value += delta
            board_value = self.calculate_static_board_heuristic_value()

            self.assertEqual(current_value, board_value)

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

    def test_get_rows_that_contain_move_returns_correct_rows(self):
        self.gameboard.board[3][5] = Marker.PLAYER
        self.gameboard.board[3][6] = Marker.PLAYER
        self.gameboard.board[3][7] = Marker.PLAYER
        self.gameboard.board[4][7] = Marker.AI
        self.gameboard.board[4][8] = Marker.AI

        correct_rows = [
            [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        ]
        rows = self.gameboard.get_rows_that_contain_move(8, 3)
        for i, row in enumerate(rows):
            self.assertListEqual(correct_rows[i], [int(n) for n in row[0]])

    def test_update_candidates_returns_correct_list(self):
        self.gameboard.board[5][5] = Marker.PLAYER
        old_candidates = {(5, 5), (4, 5)}
        added_candidates = [(3, 4), (5, 4), (3, 6), (5, 6), (4, 4), (3, 5), (4, 6), (2, 3), (6, 3),
                            (2, 7), (6, 7), (4, 3), (2, 5), (6, 5), (4, 7)]
        self.assertListEqual(added_candidates,
                             self.gameboard.update_candidates(old_candidates, 4, 5))

    def test_update_candidates_returns_correct_list_with_corner_move(self):
        self.gameboard.board[1][0] = Marker.AI
        old_candidates = {(0, 0)}
        added_candidates = [(1, 1), (1, 0), (2, 2), (2, 0), (0, 2)]
        self.assertListEqual(added_candidates,
                             self.gameboard.update_candidates(old_candidates, 0, 0))

    def test_clone_board_returns_exact_clone(self):
        self.gameboard.move(5, 5, Marker.PLAYER)
        self.gameboard.move(0, 0, Marker.AI)
        self.gameboard.move(19, 19, Marker.PLAYER)

        copy = self.gameboard.clone_board()

        self.assertEqual(copy.size, self.gameboard.size)
        self.assertListEqual(copy.board, self.gameboard.board)
        self.assertListEqual(copy.move_history, self.gameboard.move_history)
        self.assertEqual(copy.zobrist_hash, self.gameboard.zobrist_hash)
        self.assertListEqual(copy.zobrist_table, self.gameboard.zobrist_table)
        self.assertListEqual(copy.player_patterns, self.gameboard.player_patterns)
        self.assertListEqual(copy.ai_patterns, self.gameboard.ai_patterns)

    def test_zobrist_hash_matches_after_undo(self):
        orig_hash = self.gameboard.zobrist_hash
        self.gameboard.move(10, 10, Marker.PLAYER)
        new_hash = self.gameboard.zobrist_hash

        self.assertNotEqual(orig_hash, new_hash)

        self.gameboard.undo_move()
        new_hash = self.gameboard.zobrist_hash

        self.assertEqual(orig_hash, new_hash)

    def test_zobrist_hash_is_distinct(self):
        self.gameboard.move(10, 10, Marker.PLAYER)
        hash1 = self.gameboard.zobrist_hash

        self.gameboard.undo_move()

        self.gameboard.move(11, 11, Marker.PLAYER)
        hash2 = self.gameboard.zobrist_hash

        self.assertNotEqual(hash1, hash2)
