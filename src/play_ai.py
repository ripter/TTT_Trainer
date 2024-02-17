from pathlib import Path
from mlx_lm import load, generate

from consts import *
from file_utils import get_unique_filename 
from GameState import GameState
from input_utils import input_for_move, input_review_ai_reponse, convert_ai_response_to_move


def play_ai(model_path: Path, LoRA_path: Path = None):
  """
  Play's the model AI aganist a human player.
  The AI is trained to play as the "O" player.
  Game ends when the AI wins, loses, draws, or outputs an invalid move. 

  Args:
    model_path (Path): The path to load the model from.

  Returns:
    FileNotFoundError: If the weight files (.safetensors) are not found.
    str: The game log.
  """
  model, tokenizer = load(model_path, adapter_file=LoRA_path)
  game_state = GameState()
  result = INSTRUCTION +  str(game_state) 
  print(game_state)

  max_tokens = 35
  temp = 0

  while game_state.is_running:
    print("----")
    if game_state.player == "X":
      # Get the user's move and play it.
      (was_successful, user_move) = input_for_move()
      if not was_successful:
        game_state.error_message = user_move
        game_state.is_running = False
        break

      game_state.play(user_move)
      result += str(game_state)
    elif game_state.player == "O":
      # Give the AI the entire game log as the prompt.
      ai_response = generate(model, tokenizer, result, temp, max_tokens)
      (was_successful, ai_move) = convert_ai_response_to_move(ai_response)

      if not was_successful:
        game_state.error_message = ai_move
        game_state.is_running = False
        break
      game_state.play(ai_move)
      result += str(game_state)

    print(game_state)

  print("\n=========\nGame Log:\n")
  print(result)
  return result



if __name__ == "__main__":
  from os import path

  result = play_ai(PATH_MODEL)

  # # Combine the AI instructions with the gameplay log.
  # result = INSTRUCTION + play_random_ai()
  # write result out to /output
  file_path = path.join(DIR_OUTPUT, "TTT_AI_log.txt")
  file_name = get_unique_filename(file_path)
  with open(file_name, "w") as file:
    file.write(result)
