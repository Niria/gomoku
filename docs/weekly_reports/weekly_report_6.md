# Weekly Report 6

### This week

This week I tried my best to implement the changes we discussed during the zoom session last Monday.

I removed the static branch pruning I had implemented last week. 
The candidate list keeps expanding throughout the game, which means the branching factor can become very high later on in the game.

I refactored minimax to once again have be split into max and min paths.
I still need to work on further extracting logic out of minimax into helper methods to make it easier to follow.

I believe I may have finally managed to fix the transposition table logic when minimizing by adding the lower bound flag when value is higher than beta_orig instead of beta.


One of the biggest changes I made this week is to move ordering.
Prior to the changes, the shallow move values of all candidate moves were calculated before creating the move ordering.
Move ordering no longer depends on move value, but the following 3 things:
1. Best move from previous search
2. History heuristic value [1, 2]
3. Chebyshev distance from the most recent move

Moves that cause alpha-beta prunes are stored and given a historical heuristic value that increases the more cutoffs it caused.
In essence this gives moves that proved to be good before a higher priority.
It seems my algorithm is at least a little more efficient now, but the search depth did not increase quite as much as I thought it would.
The algorithm used for computing the heuristic value of moves is simply too heavy, and would probably require a full overhaul in order to increase search depth.

I also added null window search to minimax when maximizing.
Null window searches start at depth >=4 from the second branch onwards.
If the search runs into a cutoff in any given branch, the branch is examined with a full search.

I wrote some new tests for the AI:
- Minimax maximizes in max
- Minimax minimizes in min
- AI is able to find move sequence for win from depth of 5
- AI does not play moves outside board
- AI blocks players blocked 4 from becoming 5 in a row

I also added a new graphical UI for the game using pygame and worked on the project documentation.

References: 

[1] https://ieeexplore.ieee.org/document/42858

[2] https://www.chessprogramming.org/History_Heuristic.


### What I learned

This week I learned about the history heuristic which can be used to create a better move order.
I also spent some time getting familiar with the concept of null window searching while implementing it into my minimax algorithm.


### Questions

Are the currently implemented tests for minimax representative enough and do they cover the course requirements?
Is there a test that is either missing or that I've misunderstood?

If there's any glaring issues, I'll gladly take any advice and be in touch if necessary.


### Next week

Next week I'll probably focus on refactoring to improve code quality, increasing test coverage and project documentation.
I'll also try to figure out a good way I can present the project at the demo event.

Hours spent this week: 24

