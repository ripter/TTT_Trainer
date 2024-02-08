##
## Human player vs AI, battle is logged to file.
## Run file to generate a log of a game of Tic Tac Toe.
##

import random
from GameState import GameState
from consts import INSTRUCTION
from file_utils import get_unique_filename

DIR_OUTPUT = "data"


def play_random_ai():
    ## Simple AI that makes a random move each turn.
    game_state = GameState()
    result = str(game_state) 
    print(result)

    while game_state.is_running:
        print("----")
        if game_state.player == "X":
            # TODO: loop until we have a valid play.
            user_input = input("0-8: ")
            # Convert to a number and update game state.
            game_state.play(int(user_input))
            print(game_state)
        elif game_state.player == "O":
            # Make a random valid play.
            while game_state.player == "O":
                ai_input = random.randint(0, 8)
                if game_state.grid[ai_input] == None:
                    game_state.play(ai_input)
            print(game_state)
        result += str(game_state)


    print("Game Over")
    return result


if __name__ == "__main__":
    from os import path, makedirs
    makedirs(DIR_OUTPUT, exist_ok=True)

    # Combine the AI instructions with the gameplay log.
    result = INSTRUCTION + play_random_ai()
    # write result out to /output
    file_path = path.join(DIR_OUTPUT, "TTT_game_log.txt")
    file_name = get_unique_filename(file_path)
    with open(file_name, "w") as file:
        file.write(result)
