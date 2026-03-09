import numpy as np

def solve_sudoku(board):

    def is_valid(row, col, num):
        # check row
        # : means "all columns in this row"
        # num in board[row, :] checks if num is in that row
        if num in board[row, :]:
            return False

        # check column
        # : means "all rows in this column"
        # num in board[:, col] checks if num is in that column
        if num in board[:, col]:
            return False

        # check 3x3 box
        # row // 3 gives the index of the box row (0, 1, or 2)
        # because it counts how many times 3 fits fully into the row index
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        if num in board[start_row:start_row+3, start_col:start_col+3]:
            return False

        return True

    # both lists and arrays support indexing with [row][col]
    # but arrays also support [row, col] which is more concise
    def backtrack():
        for row in range(9):
            for col in range(9):
                if board[row, col] == 0:

                    for num in range(1, 10):
                        if is_valid(row, col, num):

                            board[row, col] = num

                            if backtrack():
                                return True

                            board[row, col] = 0

                    return False

        return True


    if backtrack():
        return board
    return None

import numpy as np

puzzle = np.array([
[5,3,0,0,7,0,0,0,0],
[6,0,0,1,9,5,0,0,0],
[0,9,8,0,0,0,0,6,0],
[8,0,0,0,6,0,0,0,3],
[4,0,0,8,0,3,0,0,1],
[7,0,0,0,2,0,0,0,6],
[0,6,0,0,0,0,2,8,0],
[0,0,0,4,1,9,0,0,5],
[0,0,0,0,8,0,0,7,9]
])

solution = solve_sudoku(puzzle)

print(solution)