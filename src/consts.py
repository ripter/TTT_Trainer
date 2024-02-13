from os import path, makedirs
from pathlib import Path


PATH_MODEL = Path("./models/Mistral-7B-v0.1/")

DIR_OUTPUT = "data"
makedirs(DIR_OUTPUT, exist_ok=True)


INSTRUCTION = ("3TBot is playing Tic Tak Toe with User.\n"
    + "3TBot is playing as O. User is playing as X.\n"
    + "Only play when it is your turn.\n"
    + "Stop playing when someone wins.\n")
    # + "When it is your turn, make a valid move or declare the winner.\n"

GAME_OVER = ("Game Over\n")