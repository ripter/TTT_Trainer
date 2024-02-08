def value_to_str(value):
    if value is None:
        return " "
    return value

class GameState:
    def __init__(self):
        self.grid = [None, None, None, None, None, None, None, None, None]
        self.player = "X"
        self.is_running = True

    def turn_end(self):
        if self.player == "X":
            self.player = "O"
        else:
            self.player = "X"

    def play(self, move):
        self.grid[move] = self.player
        self.turn_end()

        if self.get_winner() is not None:
            self.is_running = False

        if self.has_open_moves() is False:
            self.is_running = False

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
    
    def has_open_moves(self):
        # Return true if there is an open space in the grid.
        return any([x is None for x in self.grid])

    
    def __str__(self):
        return (self._str_status() + self._str_grid())

    
    def _str_grid(self):
        return (" " + value_to_str(self.grid[0]) + " | " + value_to_str(self.grid[1]) + " | " + value_to_str(self.grid[2]) + " \n" 
            + " " + value_to_str(self.grid[3]) + " | " + value_to_str(self.grid[4]) + " | " + value_to_str(self.grid[5]) + " \n"
            + " " + value_to_str(self.grid[6]) + " | " + value_to_str(self.grid[7]) + " | " + value_to_str(self.grid[8]) + " \n"
        )
        
    def _str_status(self):
        winner = self.get_winner()
        if winner is None:
            return f'\n Next Play: {self.player} \n'
        return f'\n Winner: {winner} \n'
        

    def to_json(self):
        return {
            "player": self.player,
            "winner": self.get_winner(),
            "grid": [
                [self.grid[0], self.grid[1], self.grid[2]],
                [self.grid[3], self.grid[4], self.grid[5]],
                [self.grid[6], self.grid[7], self.grid[8]],
            ],
        }
    
