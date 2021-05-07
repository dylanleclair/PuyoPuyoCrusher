import helpers
import copy

class AndNode:

    # constructs the problem 
    def __init__(self,board,buffer, score, moveset):    
        self.board = board # the board representation at this state
        self.buffer = buffer # the buffer of 'known' pieces
        self.depth = 0 # keeps track of how 'deep' (ie: how many moves in the future) this node has computed        
        self.score_accumulated = score # the score accumulated up to this point in the search
        self.moves = moveset
    # the division relation (splits the problem into different choices)
    def div(self, piece):

        new_instances = [] # the list of new problem instances to be considered by the search

        piece = self.buffer[0]
        # need to flip the piece?
        piece = (piece[1], piece[0])
        board = self.board
        if piece[0] == piece[1]:
            # if the colors are identical, we need to consider this. 
            # only 2w - 1 moves to consider

            # simulate moves 2w-1, add the new problem instances to collection

            # first, simulate the vertical moves 
            
            for i in range(len(board[0])):
                b = helpers.place(board,piece[0],i)
                b = helpers.place(b,piece[0],i)
                new_instances.append((b,(i,1))) # add the new board to the new list of problem instances
            
            # then, simulate the horizontal moves
            for i in range(len(board[0])-1):
                b2 = helpers.place(board,piece[0],i)
                b2 = helpers.place(b2,piece[0],i+1)
                new_instances.append((b2,(i,2)))

        else: 
            # otherwise, parse the move regularly 
            # must consider 4w-2 moves 
            board_width = len(board[0])
            # first, simulate the vertical moves (both directions)
            for i in range(len(board[0])):
                b = helpers.place(board,piece[0],i)
                b = helpers.place(b,piece[1],i)
                new_instances.append((b,(i,1))) # add the new board to the new list of problem instances
                b2 = helpers.place(board,piece[1],i)
                b2 = helpers.place(b2, piece[0],i)
                new_instances.append((b2,(i,3))) # add the new board to the new list of problem instances
            # second, simulate the horizontal moves (both directions)
            for i in range(len(board[0])-1):
                b = helpers.place(board,piece[0],i)
                b = helpers.place(b,piece[1],i+1)
                new_instances.append((b,(i,2))) # add the new board to the new list of problem instances
                b2 = helpers.place(board,piece[1],i)
                b2 = helpers.place(b2, piece[0],i+1)
                new_instances.append((b2,(i,4))) # add the new board to the new list of problem instances
            # simulate moves 1..4w-2, add the new problem instances to the collection

            # returns column and rotation that the piece should be placed in 
            # rotations: 1 = upright, 2 = horizontal, left, 3 = downwards, 4 = horizontal, right


        return new_instances

        
    def advance(self,stack, ap):
        # terminate if the buffer is empty
        if len(self.buffer) == 0:
            return
        # take the next element from the buffer
        new_buffer = copy.deepcopy(self.buffer)
        # take the next piece
        next_piece = new_buffer.pop(0)

        # pass it through div to find the next boards
        new_boards = self.div(next_piece) 

        # create the proper search instances for them
        for pair in new_boards:
            # for each board, create a revised node 
            '''
            print()
            for x in b:
                print(x)
            print()
            '''
            b = pair[0]
            move = pair[1]
            new_moves = copy.deepcopy(self.moves)
            new_moves.append(move) # add the taken move to the list of moves
            b2, local_score = helpers.projected_score(b,ap) # returns the corrected board after removing chains, as well as score added by chain
            local_score += self.score_accumulated 
            node = AndNode(b,new_buffer, local_score, new_moves) # create the new and node 
            # add them to the stack depending on search control (right now, just exhaustive search)
            stack.push(node)
        


class Search:
    def __init__(self,board, buffer):
        # create a new search, with the board
        self.ap = helpers.AttackPowers().chain_powers # loads the list of attack powers to be used in scoring
        self.root = AndNode(board,buffer,0, []) # creates the root of the and search tree being used
        self.leaves = helpers.Stack() # a stack that will contain the leaves of the tree that will need to be searched. 
    # search
    def search(self):
        print('starting the search')
        # perform the search
        # some constraints to keep in mind: 
        #   - items added to the stack need to be done so in the correct order (higher priority to more promising leaves)
        print('active buffer', self.root.buffer)
        print('board')
        helpers.print_board(self.root.board)
        self.root.advance(self.leaves, self.ap) # advance the search
                
        best_score = 0
        best = self.root

        while self.leaves.length() != 0:

            # continue to search
            current_state = self.leaves.pop() # get the next search state
            

            if current_state.score_accumulated > best_score: # check it's score
                best_score = current_state.score_accumulated # update the best score
                best = current_state # update the best_move



            current_state.advance(self.leaves, self.ap)
        return best
        






