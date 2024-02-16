
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
