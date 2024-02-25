/**
 * Checks the Tic-Tac-Toe board to determine if there is a winner.
 * The board is represented as a flat array of 9 elements, where each element can be 'X', 'O', or an empty slot.
 * The function iterates through rows, columns, and diagonals to find if any line contains the same player's marks.
 * 
 * @param {Array} grid - The Tic-Tac-Toe board represented as a flat array of 9 elements.
 * @returns {(string|null)} - Returns the winning player's mark ('X' or 'O') if there is a winner, or null if there is no winner yet.
 */
export function getWinner(grid) {
  // check rows
  for (let i = 0; i < 9; i += 3) {
    if (grid[i] === grid[i + 1] && grid[i] === grid[i + 2]) {
      return grid[i];
    }
  }
  // check columns
  for (let i = 0; i < 3; i++) {
    if (grid[i] === grid[i + 3] && grid[i] === grid[i + 6]) {
      return grid[i];
    }
  }
  // check diagonals
  if (grid[0] === grid[4] && grid[0] === grid[8]) {
    return grid[0];
  }
  if (grid[2] === grid[4] && grid[2] === grid[6]) {
    return grid[2];
  }

  return null;
}