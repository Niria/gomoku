from random import getrandbits

DEBUG_MODE = False


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

def log(*args, **kwargs):
    """Wrapper for outputting debug information to terminal"""
    if DEBUG_MODE:
        print(*args, **kwargs)