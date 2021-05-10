//! The search class
use std::collections::VecDeque;

#[derive(Clone)]
pub struct Node {
    pub board: Vec<Vec<u8>>,
    buffer: VecDeque<(u8,u8)>,
    score_acc: i32,
    moves: Vec<(u8,u8)> 
}


impl Node {
    pub fn new (
        b: Vec<Vec<u8>>,
        buf: VecDeque<(u8,u8)>,
        score: i32,
        moveset: Vec<(u8,u8)>) -> Node {
            return Node {
                board:b,
                buffer: buf,
                score_acc: score,
                moves: moveset
            };
        }
    
    /// Returns a new board, along with the move that was taken to yield it in Simple Puyo Puyo Notation
    /// Tested, runs fine.
    pub fn div(&self, piece:(u8,u8)) -> Vec<(Vec<Vec<u8>>,(u8,u8))> {
        let mut new : Vec<(Vec<Vec<u8>>,(u8,u8))> = Vec::new();
        //println!("piece {:?}", piece);
        let piece = (piece.1,piece.0); // reverse it so encoding works properly

        let w = self.board[0].len();
        if piece.0 == piece.1 
        {
            //println!("piece {:?}", piece);
            // if the colors in the piece are the same, we only need to consider 1/2 of all possible moves
            // handle the vertical possibilities
            for i in 0..w {
                let mut b = self.board.to_vec();
                super::place(&mut b,piece.0,i as u8);
                super::place(&mut b, piece.0,i as u8);
                new.push((b,(i as u8,1)));
            }

            // handle the horizontal possibilities
            for i in 0..w-1 {
                let mut b = self.board.to_vec();
                super::place(&mut b,piece.0,i as u8);
                super::place(&mut b,piece.0,(i+1) as u8);
                new.push((b,(i as u8,2)));
            }

        } else {
            for i in 0..w {
                // handle the vertical possibilities
                // "top to bottom"
                let mut b = self.board.to_vec();
                super::place(&mut b,piece.0,i as u8);
                super::place(&mut b,piece.1,i as u8);
                new.push((b,(i as u8,1)));
                
                // "bottom to top"
                let mut b = self.board.to_vec();
                super::place(&mut b,piece.1,i as u8);
                super::place(&mut b,piece.0,i as u8);
                new.push((b,(i as u8,3)));
            }

            for i in 0..w-1 {
                // handle the horizontal possibilities
                
                // "left-to-right"
                let mut b = self.board.to_vec();
                super::place(&mut b,piece.0,i as u8);
                super::place(&mut b,piece.1,(i+1) as u8);
                new.push((b,(i as u8,2)));
                // "right-to-left"
                let mut b = self.board.to_vec();
                super::place(&mut b,piece.1,i as u8);
                super::place(&mut b,piece.0,(i+1) as u8);
                
                new.push((b,(i as u8,4)));
            }
            
        }
        return new;
    } 

    // Advances the search, creating new leaves from a given leaf
    pub fn advance(&self, stack: &mut Vec<Node>) {

        if self.buffer.len() == 0 {
            return;
        }

        let mut buffer = self.buffer.clone(); // copy the buffer -> this is to be the buffer in the next node
        let next_piece: (u8,u8) = buffer.pop_front().expect("Buffer is empty."); // get the first move
        let new_boards =  self.div(next_piece);

        for pair in new_boards {
            let board = pair.0;
            let next_move = pair.1;
            let copy = board.clone();
            let mut new_moves = self.moves.to_vec(); // clone the accumulated moves
            new_moves.push(next_move); // add the new move to end of accumulated

            let results = super::projected_score(board);
            
            // @TODO shouldn't need to return the board unless you are reconsidering after every move
            // since no side effects are possible using the current heuristic

            let new = Node::new(copy, buffer.clone(), self.score_acc + results.1, new_moves);
            stack.push(new);
        }

    } 

    pub fn inject_buffers(& self, buf: Vec<VecDeque<(u8,u8)>>) -> Vec<Node> {

        let mut result = Vec::new();

        for x in buf {
            let mut copy = self.clone(); // clone the entire node 
            copy.buffer = x; // set the new buffer
            result.push(copy);
        }

        result

    }


}


pub struct Search {
    root: Node,
    leaves: Vec<Node>
}

impl Search {
    pub fn new(board:&Vec<Vec<u8>>, buffer:VecDeque<(u8,u8)>) -> Search {
        return Search {
            root: Node::new(board.to_vec(), buffer, 0, Vec::new()),
            leaves: Vec::new()
        }

    }

    pub fn search(&mut self) -> Vec<(u8,u8)> {
        // advance the search
        self.root.advance(&mut self.leaves);
        let mut best_score = 0;
        let mut best = self.root.moves.to_vec();
        while self.leaves.len() > 0 {
            let current = self.leaves.pop().expect("Leaf expected, but none found.");
            
            if current.score_acc > best_score {
                best_score = current.score_acc;
                best = current.moves.to_vec();
            }

            current.advance(&mut self.leaves);
        }
        return best;

    }


    fn init_alt_search(&mut self) -> Vec<Node> {
        // advance the search
        // the search must have a root
        self.root.advance(&mut self.leaves);
        
        let mut leaves_max_depth = Vec::new(); // a collection of the nodes at max depth, whose buffer will need to be supplemented and searched

        while self.leaves.len() > 0 {
            let current = self.leaves.pop().expect("Leaf expected, but none found.");
            
            if current.buffer.len() == 0 
            { // if no more raw moves r made, collect the final nodes. they will be the root for the new search
                leaves_max_depth.push(current.clone());
            }

            current.advance(&mut self.leaves);
        }

        leaves_max_depth

    }


    /// The alternative search, creates a new child with each buffer
    fn alt_search_helper(&mut self) -> (u8,u8) {

        // create all of the new buffers

        let sample: Vec<u8> = vec![1,2,3,4];

        let all = super::compute_all_puyos(&sample);

        let mut bufs = Vec::new(); // the collection the buffers will be collected into
        super::compute_buffers(0, 1, &mut bufs, &all);
        
        // for each node, pass it a new buffer and advance the search

        let leaves_to_preprocess = self.init_alt_search(); // reassign the leaves in the search to be the leaves of the initial search
        for leaf in leaves_to_preprocess {
            let new_leaves = leaf.inject_buffers(bufs); // correct this to the proper type!
        }
        
        // pop from stack, advancing normally until complete.

        (0,0)
    }




}