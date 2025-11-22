from random import getrandbits

def function_call_counter(func):
    """
    Used for calculating the number of times a function has been called
    :param func: Function to be called
    :return: Wrapper function
    """
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


def generate_zobrist_table(size):
    """
    Generates a zobrist table for the unique combinations of moves and players
    :param size: Size of the board
    :return: 3d list of 64 bit values for each move and player combination
    """
    table = [[[0 for _ in range(3)] for _ in range(size)] for _ in range(size)]

    for row in range(size):
        for col in range(size):
            for marker in range(1,3):
                table[col][row][marker] = getrandbits(64)

    return table

def char_to_number(char):
    """
    Converts a character into an integer
    :param char: Character to be converted
    :return: Int
    """
    return ord(char.lower()) - ord('a')
