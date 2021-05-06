import helpers


class AndNode:

    # constructs the problem 
    def __init__(self,board,buffer, score):    
        self.board = board # the board representation at this state
        self.buffer = buffer # the buffer of 'known' pieces
        self.depth = 0 # keeps track of how 'deep' (ie: how many moves in the future) this node has computed        
        self.score_accumulated = score # the score accumulated up to this point in the search

    # the division relation (splits the problem into different choices)
    def div(self):

        new_instances = [] # the list of new problem instances to be considered by the search

        if len(self.buffer) > 0:    
            # general logic for known futures (ie: the buffer has not yet been exhausted)
            
            piece = self.buffer[0]
            board = self.board
            if piece[0] == piece[1]:
                # if the colors are identical, we need to consider this. 
                # only 2w - 1 moves to consider

                # simulate moves 2w-1, add the new problem instances to collection

                # first, simulate the vertical moves 
                
                for i in range(len(board[0])):
                    b = helpers.place(board,piece[0],i)
                    b = helpers.place(b,piece[0],i)
                    new_instances.append(b) # add the new board to the new list of problem instances
                
                # then, simulate the horizontal moves
                for i in range(len(board[0])-1):
                    b = helpers.place(board,piece[0],i)
                    b = helpers.place(b,piece[0],i+1)

                print('colors are identical')
            else: 
                # otherwise, parse the move regularly 
                # must consider 4w-2 moves 

                # first, simulate the vertical moves (both directions)
                for i in range(len(board[0])):
                    b = helpers.place(board,piece[0],i)
                    b = helpers.place(b,piece[1],i)
                    new_instances.append(b) # add the new board to the new list of problem instances
                    b2 = helpers.place(board,piece[1],i)
                    b2 = helpers.place(b2, piece[0],i)
                    new_instances.append(b2) # add the new board to the new list of problem instances
                # second, simulate the horizontal moves (both directions)
                for i in range(len(board[0])-1):
                    b = helpers.place(board,piece[0],i)
                    b = helpers.place(b,piece[1],i+1)
                    new_instances.append(b) # add the new board to the new list of problem instances
                    b2 = helpers.place(board,piece[1],i)
                    b2 = helpers.place(b2, piece[0],i+1)
                    new_instances.append(b2) # add the new board to the new list of problem instances
                # simulate moves 1..4w-2, add the new problem instances to the collection

        else: 
            # future: this will have logic for considering ALL pieces to estimate the best 
            # possible move, across all futures (not yet implemented)
            print('buffer is empty - simulating with depth')
    
        return new_instances
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
        self.root = AndNode(board,[('1','2')],0) # creates the root of the and search tree being used
        self.leaves = helpers.Stack() # a stack that will contain the leaves of the tree that will need to be searched. 

    def search(self, board, buffer):

        

        print('starting the search')
        # perform the search
        # some constraints to keep in mind: 
        #   - items added to the stack need to be done so in the correct order (higher priority to more promising leaves)





