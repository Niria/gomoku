# Implementation Document

## Program structure

The program logic is split into four main components:

- `gomoku.py` manages the game loop and calls methods of `GameBoard` and `PygameUI` to control the state of the game and UI. 
- `game_board.py` contains the game state and all the logic required for updating it.
- `gomoku_ai.py` contains the minimax algorithm that is used to look for the most optimal next move for the AI.
- `pygame_ui.py` draws the UI, handles user input and game events.

Additionally, there's tests in `src/tests` that verify the correctness of game state and AI logic.


## Time complexity and optimisation

The minimax algorithm has a time complexity of $O(b^d)$, where $b$ is the branching factor and $d$ is the search depth.
In a 20x20 gomoku game the branching factor is very large, because the candidate list can potentially have up to 400 moves.
To mitigate this, in this project the candidates are limited to all moves that are within a Chebyshev distance of 2 from a previous move.
This limits the branching factor to roughly 20-30 in the early game, but this number keeps growing throughout the game since no branch pruning is done.

Alpha-beta pruning has a best case time complexity of $O(\sqrt{b^d}$ which requires optimal move ordering.
The move ordering implemented in this project is based on three things:
1. Best move from previous search
2. History heuristic. Moves that cause a lot of alpha-beta prunes are worth exploring first.
3. Chebyshev distance from the previous move.

To further optimise the search algorith, several other optimisations have been used:
- Heuristic evaluation is done dynamically by calculating the delta heuristic value of moves, instead of performing a full heuristic evaluation of the board. If for example a move is very beneficial for the AI, this means the delta is a large positive number which is then added to the overall heuristic value of the board.
- Transposition table with zobrist hashing. Different move sequences may lead to the exact same board state. To reduce unnecessary computation, cached exact, lower and upper bound values stored in the transposition table can be used instead. Zobrist hashing is used to give every distinct game board state a unique hash identifier.
- Null window search when minimax is maximizing. Null window searching is used after the first full branch search beyond depth 4. The goal is to check whether a given branch increases the alpha value by setting the search window size to 1. If it does, a full search is done to determine the true value of alpha and beta within that particular branch.

## Limitations and possible improvements

The candidate list keeps going as the game progresses and currently no pruning is done to remove older candidates that may or may not be very relevant during later stages of the game. The major downside is that it can limit search depth quite a bit.

The string pattern matching method for computing the move value heuristic is quite slow, which makes it difficult to increase search depth.
A better way would be to count the amount of markers on a row by row basis and compute the heuristic based on that.

The game board can be stored is a bitboard instead of a 2d list. This enables much faster pattern matching through bit manipulation. For example to match five in a row you can simply bitshift a row to the right by one five times while performing a bitwise AND on the original row.

## AI usage

I have used Google Gemini Pro 2.5 and 3 for learning about concepts related to algorithm, such as:
- Alpha-beta pruning
- Transposition tables
- Iterative deepening

I have also used it for troubleshooting, and examining the AI behaviour during the execution of my program by analysing debug logs.
I have not used AI written code.

## Sources
https://en.wikipedia.org/wiki/Gomoku
<br>
https://en.wikipedia.org/wiki/Minimax
<br>
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning 
<br>
https://xinhhd.github.io/GomokuReport_11610320.pdf
<br>
https://en.wikipedia.org/wiki/Transposition_table
<br>
https://en.wikipedia.org/wiki/Zobrist_hashing
<br>
https://en.wikipedia.org/wiki/Negamax
<br>
https://ieeexplore.ieee.org/document/42858
<br>
https://www.chessprogramming.org/History_Heuristic
<br>
https://people.csail.mit.edu/plaat/mtdf.html#abmem

