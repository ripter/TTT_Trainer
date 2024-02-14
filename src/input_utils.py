
def input_for_move():
  """
  Get input from the user for a move.

  Returns:
    int: The move the user wants to make.
  """
  while True:  # Keep asking until a valid input is received
    try:
      user_input = input("Player Move (0-8): ")
      user_move = int(user_input)
      if -1 <= user_move <= 8:  # Check if the number is within the valid range
        return user_move
      else:
        print("Invalid input. Please enter a number between 0 and 8.")
    except ValueError:
      print("Invalid input. Please enter a number between 0 and 8.")


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
