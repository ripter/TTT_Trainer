
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
      if 0 <= user_move <= 8:  # Check if the number is within the valid range
        return user_move
      else:
        print("Invalid input. Please enter a number between 0 and 8.")
    except ValueError:
      print("Invalid input. Please enter a number between 0 and 8.")
