# Testing Report


## Coverage

![Test coverage week 5](/docs/images/coverage_week5.png)

The GameBoard class is currently tested with 93% coverage and GomokuAI with 87%.

## Testing

All tests are done using the unittest library. 

### GameBoard
In GameBoard all methods apart from str() are tested.

### GomokuAI
- Can AI detect available win (horizontal/vertical/diagonal/reverse diagonal)
- AI blocks player open and split three
- AI prioritises blocking player open three over creating its own
- AI creates open four instead of blocked four

