from random import getrandbits

def function_call_counter(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


def generate_zobrist_table(size):
    table = [[[0 for _ in range(3)] for _ in range(size)] for _ in range(size)]

    for row in range(size):
        for col in range(size):
            for marker in range(1,3):
                table[col][row][marker] = getrandbits(64)

    return table