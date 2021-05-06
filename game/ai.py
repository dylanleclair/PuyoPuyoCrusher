from . import helpers


class AndNode:

    # constructs the problem 
    def __init__(self,board,buffer, moves, score):    
        self.board = board # the board representation at this state
        self.buffer = buffer # the buffer of 'known' pieces
        self.moves = moves # list of integers representing the possible moves    
        self.depth = 0 # keeps track of how 'deep' (ie: how many moves in the future) this node has computed        
        self.score_accumulated = score # the score accumulated up to this point in the search

    # the division relation (splits the problem into different choices)
    def div(self):

        new_instances = [] # the list of new problem instances to be considered by the search

        if len(self.buffer) > 0:    
            # general logic for known futures (ie: the buffer has not yet been exhausted)
            
            piece = self.buffer[0]
            if piece[0] == piece[1]:
                # if the colors are identical, we need to consider this. 
                # only 2w - 1 moves to consider

                # simulate moves 2w-1, add the new problem instances to collection

                print('colors are identical')
            else: 
                # otherwise, parse the move regularly 
                # must consider 4w-2 moves 

                # simulate moves 1..4w-2, add the new problem instances to the collection

                print('colors are different')


        else: 
            # future: this will have logic for considering ALL pieces to estimate the best 
            # possible move, across all futures (not yet implemented)
            print('buffer is empty - simulating with depth')
    
    
    def advance(self,piece, move):
        # computes the desired orientation of the move and places the piece into the board accordingly. 
        

        


        print('advancing the search')





    def search(self): 
        # computes the search
        print('performing a search')


# need some code to simulate a 'move' on the board
# also need to calculate the score / update board once the move is completed


class Search:
    def __init__(self,board):
        # create a new search, with the board
        self.ap = helpers.AttackPowers() # loads the list of attack powers to be used in scoring
        self.root = AndNode(board,[]) # creates the root of the and search tree being used
        self.leaves = helpers.Stack() # a stack that will contain the leaves of the tree that will need to be searched. 

    def search(self):
        print('starting the search')
        # perform the search
        # some constraints to keep in mind: 
        #   - items added to the stack need to be done so in the correct order (higher priority to more promising leaves)





