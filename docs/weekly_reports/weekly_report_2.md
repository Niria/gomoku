# Weekly Report 2

This week I worked on creating a barebones version of gomoku.
At this stage the player can place markers on the 20x20 board and the AI responds by placing a marker randomly within 2 spaces of previously placed markers.
Win condition checking should work, but it is only done for player moves right now.
I implemented a few basic tests for GomokuBoard, but the test coverage is not ideal yet.
The project should have a fairly solid structure and separation of logic at this point, but we'll see how it holds up.

This week I learned about how to compute the win condition by only iterating through the rows containing the previous move.
I also spent some time researching how to efficiently compute the next valid moves and how to pass them to child nodes during minimax.

At this point I don't really have any questions regarding the project.

Now that the fundamental mechanics of the game are in place, I can start working on the minimax algorithm next week.
I'll also work on improving the test coverage.

### Currently functional features
- Game board state handled by the GameBoard class
- Gameplay loop with player and AI taking turns
- Player can place a marker on an empty space on the board
- AI places a marker randomly on a space within 2 spaces of previous moves
- Win condition check

### Coming up next
- Game board value heuristic for minimax
- Minimax with alpha-beta pruning
- Improved test coverage

Hours spent this week: 10

