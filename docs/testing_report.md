# Testing Report


## Coverage

![Test coverage week 6](/docs/images/coverage_week6.png)

The GameBoard class is currently tested with 90% coverage and GomokuAI with 98%.

## Testing

All tests are done using the unittest library. More details to come.

### GameBoard
In GameBoard almost all methods are tested.

### GomokuAI
- Can AI detect available win (horizontal/vertical/diagonal/reverse diagonal)
- AI blocks player open and split three
- AI prioritises blocking player open three over creating its own
- AI creates open four instead of blocked four
- Minimax maximizes in max
- Minimax minimizes in min
- AI is able to find move sequence for win from depth of 5
- AI does not play moves outside board
- AI blocks players blocked 4 from becoming 5 in a row
