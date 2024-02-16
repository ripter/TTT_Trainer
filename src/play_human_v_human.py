##
## Human vs Human, battle is logged to file.
## Run file to generate a log of a game of Tic Tac Toe.
##

from GameState import GameState
from file_utils import get_unique_filename
from consts import *
from input_utils import input_for_move

def play_human_vs_human():
    ## Both players are human.
    game_state = GameState()
    result = str(game_state) 
    print(result)

    while game_state.is_running:
        print("----")
        # Get the user's move.
        (should_play_move, user_move) = input_for_move()

        # Check if the user moved or forfeited.
        if should_play_move:
          game_state.play(user_move)
        else:
          game_state.is_running = False
          game_state.error_message = user_move


        print(game_state)
        result += str(game_state)

    print("Game Over")
    return result


if __name__ == "__main__":
    from os import path, makedirs
    makedirs(DIR_OUTPUT, exist_ok=True)

    # Combine the gameplay instructions with the gameplay log.
    result = INSTRUCTION + play_human_vs_human()
    # Write result out to /output
    file_path = path.join(DIR_OUTPUT, "TTT_game_log.txt")
    file_name = get_unique_filename(file_path)
    with open(file_name, "w") as file:
        file.write(result)
