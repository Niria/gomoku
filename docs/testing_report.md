# Testing Report


## Test coverage

![Test coverage final](/docs/images/coverage_final.png)

## Testing methodology

All tests have been implemented using the unittest python library.

### GameBoard
All the methods related to game state logic have tests. 
They focus on making sure that the game state altering methods function as they are expected in both typical use cases and edge cases.
Majority of the tests are fairly simple unit tests, but the test for verifying the dynamically computed board heuristic is slightly more involved.

#### move
The `GameBoard.move` method is tested by verifying that a valid move updates the board state and move history.

#### undo
The `GameBoard.undo` method is tested by verifying that the latest move is removed from the game board and move history.

#### win_state
The `GameBoard.win_state` method is tested by verifying that it returns `True` when a win condition exists and `False` otherwise.

#### get_move_value
The `GameBoard.get_move_value` method is tested by verifying that it returns the correct heuristic value delta for the following game state:
```
  4 5 6 7 8 9
2 . . . . . .
3 . X X X o .
4 . . . O O .
5 . . . . . .
```
Where `X` is the player, `O` the AI, and `o` is the next AI move for which the delta is being calculated for.

The second test for `GameBoard.get_move_value` increments the overall game state heuristic value across 400 random moves (with a seed of 42) using the delta value returned by the method. 
The test asserts that the dynamically computed heuristical value matches the boards true heuristic value which is computed with the help of the full board heuristic evaluation method: `calculate_static_board_heuristic_value`. 
This proves that dynamically computing the heuristic value works as it should while being much faster than a full heuristic evaluation.

#### get_row_value
The test for `GameBoard.get_row_value` verifies that the method returns the correct heuristic value for an open three pattern.

#### valid_move
The first test for this method checks that it returns `True` for a valid move (0,0) when the space is empty. The second test verifies that a move that is valid, but already contains another piece returns `False`.

#### valid_coordinate
There's two different tests for this method. The first one checks that all the following moves are outside the board and return `False`:
```
moves = [(-1, 0), (0, -1), (20, 0), (0, 20), (20, 20)]
```
The second test verifies that the valid move (0, 0) returns `True`.

#### get_rows_that_contain_move
The test for this method checks that it returns the four correct rows that contain the move (8,3) when the board state is the following prior to the move:
```
  4 5 6 7 8 9
2 . . . . . .
3 . X X X . .
4 . . . O O .
5 . . . . . .
```

#### update_candidates
This method has two different tests. The first one checks that the method returns the correct candidate list when the board has one player marker at (5,5) and the AI plays a move to (4,5). Candidates update visualized:
```
Before move     After move
  2 3 4 5 6 7     2 3 4 5 6 7
3 . . . . . .   3 c . c . c .
4 . . . . . .   4 . c c c . .
5 . . c X . .   5 c c O X c .
6 . . . . . .   6 . c c c . .
7 . . . . . .   7 c . c . c .
```

The second test for the method verifies a similar thing using a corner move to make sure that the method does not return illegal moves.

#### clone_board
The test for this method verifies that the clone is an exact copy of the original gameboard instance.

#### Zobrist hash
The tests for the boards unique zobrist hash identifier verify that the hash is reverted to the previous hash after a move is undone. Another test is used to verify that two different board states have distinct hashes.


### GomokuAI

The AI tests include various game state scenarios where the goal is to verify that the AI behaves as expected. 
This includes simple scenarios such as making sure the AI plays the winning move and that it blocks the players winning moves.
These tests are repeated for each cardinal direction to make sure the AI is working symmetrically.
There's also a couple tests that verify that the AI does not attempt to pick moves that are illegal.

During development, I came across a scenario where the AI decided to create a blocked three and open two over blocking the players blocked three and open two that would turn into a blocked four and open three (a certain win). 
I fixed this behaviour and added a regression test that makes sure it does not reappear later on.

The most complicated test verifies that the AI detects a win with a search depth of 5. The initial board state and the final winning state are as follows:
```
 Initial board state:     AI win board state:
   2 3 4 5 6 7 8 9 10       2 3 4 5 6 7 8 9 10
 3 . . . . . . . . .      3 . . . . . . . . .
 4 . . . . . O X . .      4 . . . . . O X . .
 5 . . X O O O . . .      5 . . X O O O O X .
 6 . . . X X X O . .      6 . . . X X X O . .
 7 . . X X . X O . .      7 . . X X . X O . .
 8 . X . O O O . X .      8 . X O O O O O X .
 9 . . . . . . . . .      9 . . . . . . X . .
10 . . . . . . X . .     10 . . . . . . X . .
11 . . . . . . . . .     11 . . . . . . . . .
```
The test asserts that the AI plays the correct sequence of three moves that ensure a victory. 

The minimax algorithm is also tested to verify that it is always trying to maximise the value when `maximizing=True` and minimising otherwise.

#### List of GomokuAI tests
- AI plays move in the center of the board if starting
- AI detects available win (horizontal/vertical/diagonal/reverse diagonal)
- AI blocks player blocked four
- AI blocks player open and split three
- AI picks winning move over blocking players winning move
- AI prioritises blocking player open three over creating its own
- AI creates open four instead of blocked four
- AI blocks threatening intersection (regression test)
- AI does not play moves outside board
- AI is able to find move sequence for win from depth of 5
- Minimax maximizes when `maximizing=True`
- Minimax minimizes when `maximizing=False`


## Running the tests
You can run the tests with the command
```
poetry run pytest
```
and check test coverage with the commands
```
poetry run coverage run --branch -m pytest
poetry run coverage report -m
```