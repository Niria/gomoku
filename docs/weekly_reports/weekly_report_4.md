# Weekly Report 4

### This week

I had very little time this week, so I didn't have as much time to work on the project as last week. 
After our meeting on friday I started working on implementing iterative deepening, and it seems to be working now.
The best move is now returned in minimax, and it is prioritized in later searches.
I added a check for open fours in the minimax to immediately return the move as it is lethal.
I also refactored the method for calculating the move value which seems to have improved performance a little. 
I added some docstrings for most of the methods.
That's all I had time for this week. 

### What I learned

I learned a lot about how important prioritizing active moves is for pruning. 
I think I also finally grasped why exactly two identical board states don't necessarily have the same value (that took a while).


### Questions

No questions this time around as I still have plenty of suggestions left to experiment with.

### Next week

I'll try to implement at least some of the things we talked about, such as prioritizing active moves, but at this stage I really need to get started with proper testing and documentation, so I'll have to focus on that.

Hours spent this week: 12

