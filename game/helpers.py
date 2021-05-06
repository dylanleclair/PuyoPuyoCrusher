from copy import deepcopy



# could likely optimize based on whether or not scarce boards are common
def place(board,color,column):
    if not (board[0][column] == ' '):
        return False # the move is invalid
    # copy the board
    b = copy.deepcopy(board)
    # place the color at the heighest possible place of the specified column
    for i in range(len(b)):
        # iterate through the column, from top to bottom
        # until a color is reached
        if not (b[i][column] == ' '):
            row = i - 1 # this is the value of the row that the block should be placed in 
            b[row][column] = color # update the board
            break # terminate the loop
    return b # return the board with the placed color



