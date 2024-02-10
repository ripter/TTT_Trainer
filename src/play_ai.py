from pathlib import Path
from mlx_lm import load, generate
from GameState import GameState


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
  # model, tokenizer = load(model_path)
  game_state = GameState()

  # The Player moves first, so we need to get the player's move before we can generate the first prompt.
  print(game_state)




# def run_prompt(prompt):
#   response = generate(
#     model, 
#     tokenizer,
#     max_tokens=200,
#     temp=0.7,
#     prompt="In a hole in the ground there lived a hobbit.", 
#     verbose=True
# )