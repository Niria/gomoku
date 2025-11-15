# Weekly Report 3

### This week
This week I started implementing the alpha-beta pruning algorithm for the game.
Branching at each depth of minimax is limited to a candidate list that is updated as moves are played and explored.
Initially I added candidates that were within 2 spaces of the previous move, i.e. a 5x5 square of 24 up to 24 moves.
Based on feedback, I changed this so that only the candidates that are on the same row as the previous move are added.
The immediate effect of this is that the branching factor will not grow as fast as before.

Although the alpha-beta pruning seemingly works correctly, I'd still like to improve it quite a bit somehow.
At first, I simply prepended the candidates that are 2 spaces and then 1 space away from the previous move.
This guaranteed that the algorithm would iterate through the moves closest to the recent moves first.
I wasn't super happy with how it performed, so I decided to try value based ordering instead.
The candidate list is built just as before, but before minimax iterates through them, they are sorted based on the value of the move.
This seemed to reduce the number of minimax calls, but I'm ready to change back to the location based ordering if necessary.
During the first search there's usually around 60 0000 minimax calls and beyond that it varies between 50 000 and 200 000.
This is far from the optimal $\sqrt n$ calls, but I guess getting close to that number isn't realistic for such a short-term project.

While trying to improve the pruning, I learned about transposition tables and tried to implement them in this project.
I wasn't seeing impressive results, which realistically was probably due to a faulty implementation.
I came across transposition tables while trying to figure out how to prevent duplicate computation from identical board states.
Most of the transposition table features are now gone, but I still keep track of explored game board states with the help of zobrist hashing.
If the algorithm has explored the same game board state before through a different move sequence, it can just use the previously computed value. 

I also spent some time trying to clean up the code at least a tiny bit, but there's still work to be done. 

### Questions

What search depth should I set as my target for the algorithm?
I feel like currently the depth 5 search takes too long and the tends to balloon too much later in the game.

Do the values I have used for row patterns (GameBoard.PATTERN_VALUES) make sense and could they be improved?

Should I use location or move value based ordering?
As I mentioned before, although the values are only based on a shallow lookup, I found the move value based sorting improved the pruning.

I am tempted to try iterative deepening, but is that too much work for a project of this scale?

### Next week

The plan for next week is to focus on improving the tests and documentation as well as getting the project ready for peer review.


Hours spent this week: 25

