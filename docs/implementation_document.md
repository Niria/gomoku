# Implementation Document

## Structure

Details to come.

## Time complexity

Details to come.

## Possible improvements

My string pattern matching method for computing the move value heuristic is very slow which makes it difficult perform deep searches.
A better way would be to count the amount of markers on a row by row basis and compute the heuristic based on that.

Pattern matching can also be done entirely by using binary representations of the board state.

## AI usage

I have used Google Gemini Pro 2.5 and 3 for learning about concepts such as
- Alpha-beta pruning
- Transposition tables
- Iterative deepening

I have also used it for troubleshooting and trying to understand why the AI behaved the way it did during the execution of my program.
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
https://en.wikipedia.org/wiki/Negamax
<br>
https://ieeexplore.ieee.org/document/42858
<br>
https://www.chessprogramming.org/History_Heuristic
<br>
https://people.csail.mit.edu/plaat/mtdf.html#abmem

