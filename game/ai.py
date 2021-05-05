class Stack:
    def __init__(self):
        self.data = []

    '''
    Adds data to the top of the stack.
    '''
    def append(self,data):
        self.data.append(data)


    '''
    Removes (and returns) the top of the stack.
    '''
    def pop(self):
        return self.data.pop()

class AndNode:

    # constructs the problem 
    def __init__(self,board, moves):    
        self.board = board # the board representation at this state
        self.moves = moves # list of integers representing the possible moves    
        self.depth = 0 # keeps track of how 'deep' (ie: how many moves in the future) this node has computed        

    def advance(self,piece, move):
        # computes the desired orientation of the move and places the piece into the board accordingly. 
        print('advancing the search')

    def search(self): 
        # computes the search
        print('performing a search')


# need some code to simulate a 'move' on the board
# also need to calculate the score / update board once the move is completed

def search(board):
    # initialize the data structures for the search
    root = AndNode(board,[]) # creates the root of the and search tree being used
    leaves = Stack() # a stack that will contain the leaves of the tree that will need to be searched. 

    # perform the search
    # some constraints to keep in mind: 
    #   - items added to the stack need to be done so in the correct order (higher priority to more promising leaves)



