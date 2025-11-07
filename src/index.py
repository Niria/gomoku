from game_board import GameBoard
import random


def run_game():
    gameboard = GameBoard()

    while True:
        user_input = input("X Y: ")
        if user_input == "":
            break
        x, y = [int(n) for n in user_input.split(" ")]
        try:
            gameboard.move(x, y, 1)
            if gameboard.is_win_state():
                print("Player won!")
                break
            else:
                ai_x, ai_y = random.choice(gameboard.valid_moves)
                gameboard.move(ai_x, ai_y, 2)
                print(f"Player placed X to ({x}, {y}), AI placed O to ({ai_x}, {ai_y})")
        except ValueError:
            print(f"Invalid input, X and Y must be between 0 and {gameboard.SIZE-1}")
        finally:
            print(gameboard)


def main():
    run_game()


if __name__ == "__main__":
    main()