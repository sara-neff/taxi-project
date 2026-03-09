# this code solves a Sudoku puzzle using backtracking. 
# The `solve_sudoku` function takes a 9x9 board as input, 
# where empty cells are represented by 0. 
# It uses a helper function `is_valid` to check if placing a number 
# in a specific cell is valid according to Sudoku rules. 
# The `backtrack` function recursively tries to fill the board and returns True 
# if a solution is found, or False if it needs to backtrack. 
# Finally, the code includes an example Sudoku puzzle and prints the solved board.
def solve_sudoku(board):
    def is_valid(row, col, num):
        # check row
        for c in range(9):
            if board[row][c] == num:
                return False

        # check column
        for r in range(9):
            if board[r][col] == num:
                return False

        # check 3x3 box
        # row // 3 gives the index of the box row (0, 1, or 2)
        # because it counts how many times 3 fits fully into the row index,
        # ignoring any remainder. Multiplying by 3 gives the starting row index of that box.
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if board[r][c] == num:
                    return False

        # if we passed all checks, it's valid
        return True

    # the key idea is that each recursive call is responsible for one placement
    # and if something fails later, the program returns to the correct earlier level
    # and changes the number there
    def backtrack():
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:  # empty cell
                    for num in range(1, 10):
                        # if placing num in (row, col) is valid, place it and continue
                        if is_valid(row, col, num):
                            board[row][col] = num

                            # recursively try to fill the rest of the board
                            # if it leads to a solution, return True
                            if backtrack():
                                return True

                            # otherwise undo the move and try the next number
                            board[row][col] = 0  # undo move

                    # if no number 1-9 is valid in this cell, this board
                    # configuration is not solvable, so return False
                    return False
        # if we filled all cells without conflicts, we found a solution
        return True

    if backtrack():
        return board
    return None

puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solution = solve_sudoku(puzzle)

for row in solution:
    print(row)