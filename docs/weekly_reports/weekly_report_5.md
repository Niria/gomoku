# Weekly Report 5

### This week

I spent quite a bit of time trying to improve the way the heuristic value of moves is calculated.
Instead of using string pattern matching, I experimented with calculating consecutive markers on the board.
While it was faster than the string matching, I had a very difficult time coming up with useful heuristic values.
So after a full day of experimentation I decided to revert back to string pattern matching.

Based on feedback I tried my best to implement transposition tables so that cached values are actually useful.
This time around there's an extra flag which denotes if the value was the result of an exact evaluation or an alpha/beta prune.
I also changed find_ai_move so that it keeps track of the best move that has been found so far in the current search. 
When the search eventually times out, the algorithm returns the best move it found during the timed out search.

Since I am basing move order on values first and location second, I added branch pruning which limits the number of branches examined.
At depth 3 or higher minimax examines 18 highest value branches and 12 below depth 3 respectively.
I think this should work okay, but I may need to tinker with the numbers a little.


I finally refactored win_state to be independent of heuristic values.
Now it just checks if it can find 5 markers in a row.
I also refactored minimax so there's at least a little less duplicate code.

I fixed the game_board tests that I broke last week and added a few tests for gomoku_ai.
The new tests mainly test simple things such as checking if the AI can detect wins, open threes and so on.


### What I learned

This week I learned more about transposition tables and how to implement them correctly.
I also came across other methods for creating move value heuristics.
The gomoku project that I peer-reviewed had a very different approach to this problem which I found very interesting.

### Questions

I would like to know if my implementation of the transposition table is at least somewhat correct.

Is it okay to use the best value that the deepest search found before it timed out?

### Next week

I think I'm basically done with the algorithm now, unless there's some major issue I've missed.
Next week I'll focus mostly on comprehensive AI testing, refactoring and documentation.
If I have spare time, I may try to improve the UI.

Hours spent this week: 20 (+7 peer review)

