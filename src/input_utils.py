
def input_for_move():
  """
  Get input from the user for a move.

  Returns:
    int: The move the user wants to make.
  """
  while True:  # Keep asking until a valid input is received
    try:
      user_input = input("0-8: ")
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
  print("AI Response:")
  print(ai_response)
  print("Where did the AI move? (-1 for invalid response)")
  user_response = input_for_move()

  if user_response == -1:
    print("Invalid AI response. Ending Game.")
    raise ValueError("Invalid AI response.")

  return user_response