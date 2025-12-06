# User guide

## Installation

Clone the repository
```
git clone git@github.com:Niria/gomoku.git
```

Move to repository and install dependencies
```
cd gomoku
poetry install
```

Launch the game
```
poetry run python3 src/index.py
```

## Instructions

The program launches a gomoku game played on a 20x20 board. 
The goal of the game is to get five game markers in a row on a horizontal, vertical or diagonal line.
In gomoku the player that starts the game uses black markers and their opponent uses white ones.

### Gameplay

![Pygame GUI](/docs/images/pygame_gui.png)

Launching the game opens up the 20x20 board GUI in a pygame window.
In gomoku markers can only be placed on top of the gridlines.
To place a marker, simply click on top of a gridline. 
The most recent move is highlighted with a red outline.

By default, the player will start the game. 
After the player picks their move, the AI initiates an iteratively deepening minimax search. 
This search can last up to 10 seconds, but can be nearly instantaneous if the AI is able to find a move that leads to a win condition.

Currently, there's no way to adjust game settings in the GUI. 
If you want to let the AI start, you can edit the `player_starts` bool flag in `gomoku.py`.
If you want to increase or decrease the AI timer, you can do it manually by editing `turn_time_limit` in ``gomoku_ai.py``.

The game continues until either the player or the AI gets five in a row.
Once the game is over, you can press R to restart the game from a clean board or Q to quit the game.

### Tests

You can run the tests with the command
```
poetry run pytest src/
```
