from copy import deepcopy as deep



# could likely optimize based on whether or not scarce boards are common
def place(board,color,column):
    if not (board[0][column] == ' '):
        return False # the move is invalid
    # copy the board
    b = deep(board)
    # place the color at the heighest possible place of the specified column
    for i in range(len(b)):
        # iterate through the column, from top to bottom
        # until a color is reached
        if not (b[i][column] == ' '):
            row = i - 1 # this is the value of the row that the block should be placed in 
            b[row][column] = color # update the board
            break # terminate the loop
    return b # return the board with the placed color

def projected_score(board):
    # repeat until no chains left
        # add to score based on chain
        # vertically shift all blocks until no more gaps, repeat until no chains
    print('change in score: ')


'''
Detects a set of chained puyos to remove, returning a set of puyos to be removed as well as the number of chains
'''
def drop(board):
    chains = 0
    h = len(board) # find the height
    w = len(board[0]) # find the width
    puyo_to_remove = set()
    for col in range(h):
        for row in range(w):
            if (col, row) in puyo_to_remove:
                continue
            color = board[col][row]
            chained = [(col, row)]

            if color != ' ':
                chained = scan(board, col, row, chained, color)

                if len(chained) >= 4:
                    chains+=1
                    puyo_to_remove = puyo_to_remove.union(chained)
    return puyo_to_remove, chains

'''
Scans for a chain
'''
def scan(board, col, row, chained, color):
    h = len(board) # find the height
    w = len(board[0]) # find the width
    if row < w - 1:
        chained = check_neighbor(board, col, row + 1, chained, color)
    if col < h - 1:
        chained = check_neighbor(board, col + 1, row, chained, color)
    if row > 0:
        chained = check_neighbor(board, col, row - 1, chained, color)
    if col > 0:
        chained = check_neighbor(board, col - 1, row, chained, color)
    return chained


'''
Recursively checks neighbours in a chain to find the largest chain in a region
'''
def check_neighbor(board, col, row, chained, color):
    ar_color = board[col][row]
    if color == ar_color:
        if (col, row) in chained:
            return chained
        chained.append((col, row))
        chained = scan(board,col, row, chained, color)
    return chained