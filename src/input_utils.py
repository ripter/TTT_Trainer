
def input_for_move():
  """
  Get input from the user for a move or a forfeit.

  Returns:
    tuple: (bool, int or str) A tuple where the first element indicates whether the operation was successful,
            and the second element is either the move as an integer or an error/forfeit message.
  """
  while True:
    user_input = input("Player Move (0-8) or 'f' to forfeit: ")
    if user_input.lower() == 'f':
      return (False, "The player has decided to forfeit the game.")
    try:
      user_move = int(user_input)
      if 0 <= user_move <= 8:
        return (True, user_move)
      else:
        print("Invalid input. Please enter a number between 0 and 8, or 'f' to forfeit.")
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 8, or 'f' to forfeit.")



def input_review_ai_reponse(ai_response: str):
  """
  Prompts the user to review the AI's response.

  Args:
    ai_response (str): The response from the AI.

  Returns:
    int: The AI's move.
  """
  error_msg = "Invalid input. Please enter a number between 0 and 8 or -1 for invalid response." 
  print("AI Response:")
  print(ai_response)
  print("Where did the AI move? (-1 for invalid response)")
  while True:
    try:
      ai_input = input("AI Move (-1 to 8): ")
      ai_move = int(ai_input)
      if -2 <= ai_move <= 8:  # Check if the number is within the valid range
        return ai_move
      else:
        print(error_msg)
    except ValueError:
      print(error_msg)




def parse_last_play(input_string):
  # Step 1 & 2: Split on the colon to separate the description from the values, then strip whitespace
  value_part = input_string.split(':')[1].strip()

  # Step 3: Split on the comma to separate the player and position
  value_parts = value_part.split(',')

  # Step 4: Strip whitespace from each part and prepare the values
  player = value_parts[0].strip()
  position = value_parts[1].strip()

  # Step 5: Convert position to an integer
  try:
    position = int(position)
  except ValueError:
    # If the position is not an integer, return None
    position = None

  # Return as a tuple
  return (player, position)



def convert_ai_response_to_move(ai_response: str):
  """
  Convert the AI's response to a move.

  Args:
    ai_response (str): The AI's response.

  Returns:
    tuple: (bool, int or str) A tuple where the first element indicates whether the operation was successful,
            and the second element is either the move as an integer or an error/forfeit message.
  """
  ai_response_list = ai_response.split("\n") # Split the response into lines
  # Find the line that contains the last play
  last_play_lines = [parse_last_play(line) for line in ai_response_list if line.strip().startswith("Last Play:")]
  if len(last_play_lines) == 0:
    return (False, "The AI's response did not contain a 'Last Play' line.")
  elif len(last_play_lines) > 1:
    return (False, "The AI's response contained multiple 'Last Play' lines.")

  [(marker, ai_move)] = last_play_lines
  if ai_move is None:
    return (False, "The AI's response was invalid.")

  if marker == "O":
    if 0 <= ai_move <= 8:
      return (True, ai_move)
    else:
      return (False, "The ML response was outside the range of 0-8.")

  return (False, "The ML response was not for the 'O' player.")

