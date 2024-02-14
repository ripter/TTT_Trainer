from os import path, makedirs
from pathlib import Path


PATH_MODEL = Path("./models/Mistral-7B-v0.1/")

DIR_OUTPUT = "data"
makedirs(DIR_OUTPUT, exist_ok=True)


BOT_NAME = "3TBot"
PLAYER_NAME = "User"
INSTRUCTION = (f'{BOT_NAME} is playing Tic Tak Toe with {PLAYER_NAME}.\n'
    + f'{BOT_NAME} is playing as O. {PLAYER_NAME} is playing as X.\n'
    + "Only play when it is your turn.\n"
    + "Update the gameboard with your move.\n"
    + "Stop playing when someone wins.\n"
    )

GAME_OVER = ("Game Over\n")