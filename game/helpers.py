from copy import deepcopy as deep

class AttackPowers:
    chain_powers = []
    def __init__(self):
        # load the list of attack powers
        
        try:
            file = open('resource/attack_powers.txt', 'r')
            self.chain_powers = file.readlines()
            self.chain_powers = [int(x) for x in self.chain_powers] # converts the values from str -> int

        finally:
            file.close()

class Stack:
    def __init__(self):
        self.data = []

    '''
    Adds data to the top of the stack.
    '''
    def push(self,data):
        self.data.append(data)

    def length(self):
        return len(self.data)

    '''
    Removes (and returns) the top of the stack.
    '''
    def pop(self):
        return self.data.pop()


# could likely optimize based on whether or not scarce boards are common
def place(board,color,column):
    '''
    if not (board[0][column] == ' '):
        return False # the move is invalid
    '''
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
        elif (i == len(b) -1):
            b[i][column] = color # update the board
    return b # return the board with the placed color

def projected_score(board, chain_powers):
    # repeat until no chains left
        # add to score based on chain
        # increment discrete-chain counter
        # remove blocks in chains
        # apply gravity, repeat until no chains remain

    # initialize some variables
    chain = 0 # the current chain length
    chain_size = 0 # the number of puyos in the current chain
    colors_in_chain = set() # the size of this will let us determine a bonus
    chain_group_sizes = [] # the size of each group in a chain
    
    b = deep(board)
    # for some reason, b is false?
    chained_puyos, chain_size = drop(b, chain_size, colors_in_chain, chain_group_sizes)
    while len(chained_puyos) > 0:
        remove_puyos(b, chained_puyos)
        # apply gravity 
        correct_board(b)
        chained_puyos, chain_size = drop(b, chain_size, colors_in_chain, chain_group_sizes)
        chain +=1
    # return the score added from the move
    #print('chain',chain)
    #print('chain size',chain_size)
    #print('colors in chain',colors_in_chain)
    #print('chain group sizes',chain_group_sizes)

    return b, get_score(chain -1,chain_powers,chain_size,colors_in_chain,chain_group_sizes)

'''
Repairs a board after a chain is removed by dropping down all pieces 
such that no vertical gaps among puyos exist
'''
def apply_gravity(board):
    for c in range(len(board[0])):
        for r in range(len(board)-1):
            # if there is an empty space below the puyo, shift it down
            if board[r+1][c] == ' ' and not board[r][c] == ' ':
                board[r+1][c] = board[r][c]
                board[r][c] = ' '


def is_board_correct(board):
    correct = True
    for c in range(len(board[0])):
        for r in range(len(board)-1):
            if board[r+1][c] == ' ' and not board[r][c] == ' ':
                correct = False
    return correct

def correct_board(board):
    while not is_board_correct(board):
        apply_gravity(board)

# DEPRECATED
def decode_move(move, piece, board_width):

    if piece[0] == piece[1]:
        # if the colors are identical, we need only consider rotations 1 and 2
        # columns are pretty easy too

        # 0... w-1 are the vertical moves
        # w...2w-2 are the horizontal moves (-1 for zero indexing, -1 for horizontal)

        # so, 
        if move < board_width:
            # it is a vertical move
            return move, 1 # return the column (= move), and the orientation (upright)
        else: 
            # it is a horizontal move
            # conventionally, the 'column' returned
            # will be where the leftmost part of the puyo starts
            return move - board_width, 2 # return column (for ex. move 6 when board_width = 6 is the first horizontal move, but this should be in the 0th column: subtract board width!), always horizontal
    
    else: # direction of the piece is important!!!!!

        if move < board_width: # "upwards" orientation
            return move, 1
        elif move < 2 * board_width: # "downwards" orientation
            return move - board_width, 3

        elif move < 3 * board_width:
            return move - 2 * board_width, 2 # "left-to-right"
        
        else:
            return move - 3 * board_width, 4 # "right-to-left"
'''
Detects a set of chained puyos to remove, returning a set of puyos to be removed
'''
def drop(board, chain_size, colors_in_chain, chain_group_sizes):
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
                    puyo_to_remove = puyo_to_remove.union(chained)
                    chain_size += len(chained) 
                    colors_in_chain.add(color)
                    chain_group_sizes.append(len(chained))
    return puyo_to_remove, chain_size

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

'''
Given a puyo board and a set of puyos to remove (tuples of row,col), 
this function removes all such puyos - modifying the board and clearing the set afterwards.
'''
def remove_puyos(board, puyos):
    # removes the puyos
    for x in puyos:
        board[x[0]][x[1]] = ' '
    puyos.clear() # clear the set

def get_score( chain, chain_powers, chain_size,colors_in_chain, chain_group_sizes):
    # https://puyonexus.com/wiki/Scoring
    #print(get_chain_power(chain, chain_powers))
    return (10 * chain_size) * max(1,min( ( get_chain_power(chain, chain_powers) + get_color_bonus(len(colors_in_chain)) + get_group_bonus(chain_group_sizes) ), 999))
    

# Default file uses Arle in Puyo Puyo Chronicle (Normal)
# https://puyonexus.com/wiki/List_of_attack_powers
def get_chain_power(chain, powers):
    if (chain < len(powers)):
        # then return the indexed value
        return powers[chain]
    else: 
        # otherwise, return the largest value
        return powers[len(powers)-1] 

#  https://puyonexus.com/wiki/Scoring#Color_Bonus
'''
Returns the color bonus for a chain
'''
def get_color_bonus(num_colors):
    if  num_colors == 1:
        return 0
    elif num_colors == 2:
        return 3
    elif num_colors ==3:
        return 6
    elif num_colors == 4:
        return 12
    elif num_colors == 5:
        return 24

    return 0

# https://puyonexus.com/wiki/Scoring#Group_Bonus
def get_group_bonus(groups):
    local_sum = 0
    for i in groups:
        if (i == 4):
            local_sum += 0 
        elif (i <= 10):
            local_sum += i-3
        else: 
            local_sum += 10

    return local_sum


def print_board(board):
    print()
    for x in board:
        print(x)
    print()


def get_code(col1,row1,col2,row2):
    # first, calculate the column:
    col = min(col1,col2)
    if col1 == col2:
        if row1 < row2:
            return col,1
        else:
            return col, 3
    elif row1 == row2:
        if col1 > col2:
            return col, 2
        else: 
            return col, 4