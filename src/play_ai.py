from pathlib import Path
from mlx_lm import load, generate

from GameState import GameState
from input_utils import input_for_move
from consts import * 


def play_ai(model_path: Path):
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
  model, tokenizer = load(model_path)
  game_state = GameState()
  result = INSTRUCTION +  str(game_state) 
  print(game_state)

  temperatures = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5]
  max_tokens = 25

  while game_state.is_running:
    print("----")
    if game_state.player == "X":
      user_move = input_for_move()
      game_state.play(user_move)
      print(game_state)
    elif game_state.player == "O":
      print("Prompting AI")
      print("====")
      print(result)
      print("====")

      for temp in temperatures:
          print(f"AI Response at temperature {temp}")
          print("====")
          ai_response = generate(model, tokenizer, result, temp, max_tokens)
          print(ai_response)
          print("====")

      # ai_move = get_move_from_llm(ai_input)
      # game_state.play(ai_input)
      # print(game_state)
      game_state.is_running = False
    result += str(game_state)

  # # The Player moves first, so we need to get the player's move before we can generate the first prompt.
  # user_move = input_for_move()
  # game_state.play(user_move)
  # result += str(game_state)
  # print(game_state)




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
