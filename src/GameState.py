import json

def value_to_str(value):
    if value is None:
        return " "
    return value

class GameState:
    def __init__(self):
        self.grid = [None, None, None, None, None, None, None, None, None]
        self.player = "X"
        self.last_move = (None, None)
        self.error_message = ""
        self.is_running = True

    def turn_end(self):
        # Switch players
        if self.player == "X":
            self.player = "O"
        else:
            self.player = "X"

        # Check if the game is over
        if self.get_winner() is not None:
            self.is_running = False

        if self.has_open_moves() is False:
            self.error_message = "The game is a draw."
            self.is_running = False


    def play(self, move):
        if move < 0 or move > 8:
            self.error_message = f'{self.player} played an invalid move location. "{move}"'
            return
        if not self.can_move_at(move):
            self.error_message = f'{self.player} attempted to move into occupied space at position {move}'
            return

        self.grid[move] = self.player # Update State
        self.last_move = (self.player, move) # Log the move
        self.error_message = "" # Clear any error messages
        self.turn_end()


    def get_winner(self):
        # check rows
        for i in range(0, 9, 3):
            if self.grid[i] == self.grid[i + 1] == self.grid[i + 2]:
                return self.grid[i]
                
        # check columns
        for i in range(3):
            if self.grid[i] == self.grid[i + 3] == self.grid[i + 6]:
                return self.grid[i]
                
        # check diagonals
        if self.grid[0] == self.grid[4] == self.grid[8]:
            return self.grid[0]
        if self.grid[2] == self.grid[4] == self.grid[6]:
            return self.grid[2]
        return None
    

    def can_move_at(self, move):
        """Return True if the move is valid."""
        return self.grid[move] is None


    def has_open_moves(self):
        """Return True if there is an open space in the grid."""
        return any([x is None for x in self.grid])

    
    def __str__(self):
        """Return a string representation of the game state."""
        return (
            self._str_status() + 
            self._str_grid() +
            f'\n{self.error_message}'
        )

    
    def _str_grid(self):
        """Return a string representation of the game grid."""
        return (" " + value_to_str(self.grid[0]) + " | " + value_to_str(self.grid[1]) + " | " + value_to_str(self.grid[2]) + " \n" 
            + " " + value_to_str(self.grid[3]) + " | " + value_to_str(self.grid[4]) + " | " + value_to_str(self.grid[5]) + " \n"
            + " " + value_to_str(self.grid[6]) + " | " + value_to_str(self.grid[7]) + " | " + value_to_str(self.grid[8]) + " \n"
        )
        
    def _str_status(self):
        """Return a string representation of the game status."""
        winner = self.get_winner()
        message = "\n"

        if self.is_running:
            message += f'Next Play: {self.player} \n'

        if winner is not None:
            message += f'Winner: {winner} \n'
        elif self.has_open_moves() is False:
            message += "The game is a draw. \n"

        message += f'Last Play: {self.last_move[0]}, {self.last_move[1]} \n'
        
        return message
        

    def to_json(self):
        """Return a JSON representation of the game state."""
        return json.dumps({
            "player": self.player,
            "lastMove": self.last_move,
            "errorMessage": self.error_message,
            "winner": self.get_winner(),
            "grid": [
                [self.grid[0], self.grid[1], self.grid[2]],
                [self.grid[3], self.grid[4], self.grid[5]],
                [self.grid[6], self.grid[7], self.grid[8]],
            ],
        })
    
