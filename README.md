# Gomoku

Gomoku is a zero-sum game traditionally played on a 15x15 board using black and white pieces. 
This project implements the game on a 20x20 board along with an AI opponent.
At its core, the AI opponent is based on the minimax algorithm with alpha-beta pruning.
This project includes various optimization methods for the algorithm, such as a transposition table, history heuristic and null window search.

## Documentation
[Project documentation](https://github.com/Niria/gomoku/tree/main/docs)

[Weekly reports](https://github.com/Niria/gomoku/tree/main/docs/weekly_reports)

## Installation

Install dependencies
```
poetry install
```

Run the game
```
poetry run python3 src/index.py
```

Run tests
```
poetry run pytest src/
```