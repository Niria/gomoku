# Weekly Report 2

This week I worked on creating a barebones version of gomoku.
At this stage the player can place markers on the 20x20 board and the AI responds by placing a marker randomly within 2 tiles of previously placed markers.
Win condition checking should work, but it is only done for player moves right now.

Now that the most fundamental parts of the game are in place, I can start working on the minimax algorithm next week.
Aside from that, I will also work on adding tests to the project.

### Currently functional features
- Game board state handled by the GameBoard class
- Gameplay loop with player and AI taking turns
- Player can place marker on empty spaces on the board
- AI places a marker randomly on a space within 2 spaces of previous moves
- Win condition check

### Coming up next
- Game board value heuristic for minimax
- Minimax with alpha-beta pruning
- Testing

Hours spent this week: 9

