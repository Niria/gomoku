# Requirements Specification


[Gomoku](https://en.wikipedia.org/wiki/Gomoku) is a zero-sum game between two participants that is traditionally played on a 15x15 board.
The participants take turns placing their markers with the goal of having five of them in a row on the board.
If the board runs out of space before either player has managed to reach the win state, the game ends in a draw.

This project will implement gomoku on a 20x20 board with an artificially intelligent (AI) opponent for the user to play against.
The program will be written in python and its dependencies will be managed with poetry. 


Since the main focus will be the performance of the algorithms behind the AI, the game will have a fairly basic graphical user interface.
At the bare minimum, the game board state will be printed in a terminal where the user can input the coordinates of their next move as a tuple.
Each move made by the user updates the board state and prompts the computation of the next optimal move for the AI.

The opponent's AI will be based on the minimax algorithm with alpha-beta pruning.
Without alpha-beta pruning the time complexity of minimax is $O(b^d)$, where $b$ is the branching factor and $d$ is the depth of turns examined.
Gomoku has a very high branching factor, which is why alpha-beta pruning and other optimizations are necessary.
With alpha-beta pruning, the time complexities of minimax are $O(\sqrt{b^d})$ and $O(b^d)$ for best and worse case scenarios respectively.

Depending on the turn order, the algorithm will try to either minimize or maximize the value of the game state.
The list of possible moves is updated and passed around in the recursive minimax to avoid redundant computation.
Since the amount of possible marker placements is quite large on a 20x20 board, the algorithm will only examine a subset of all possible moves to maintain efficiency.
The order in which game state branches are examined will follow a heuristic to maximize the benefits of alpha-beta pruning.

Degree programme: Bachelor's in Computer Science (TKT)
<br>
Documentation language: English
<br>
Proficient in: Python, C++

## References

I have briefly skimmed through the following sources while getting familiar with the topic. It is quite likely that I'll be using at least some of them while working on this project.

https://en.wikipedia.org/wiki/Gomoku
<br>
https://en.wikipedia.org/wiki/Minimax
<br>
https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning 
<br>
https://gomocup.org/
<br>
https://www.researchgate.net/publication/385905340_Design_of_a_Gomoku_AI_Based_on_the_Alpha-Beta_Pruning_Search_Algorithm

