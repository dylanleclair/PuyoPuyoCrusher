//! The search class
use std::collections::VecDeque;
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
                println!("piece {:?}", piece);
                // "top to bottom"
                let mut b = self.board.to_vec();
                super::place(&mut b,piece.0,i as u8);
                super::place(&mut b,piece.1,i as u8);
                super::print_board(&b);
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
        println!("before {:?}", buffer);
        let next_piece: (u8,u8) = buffer.pop_front().expect("Buffer is empty."); // get the first move
        println!("after {:?}", buffer);
        println!("next piece: {:?}", next_piece);
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
        let mut best_board = self.root.board.to_vec();
        while self.leaves.len() > 0 {
            let current = self.leaves.pop().expect("Leaf expected, but none found.");
            
            if current.score_acc > best_score {
                best_score = current.score_acc;
                best = current.moves.to_vec();
                best_board = current.board.to_vec();
            }

            current.advance(&mut self.leaves);
        }
        super::print_board(&best_board);
        println!("{}",best_score);
        return best;

    }
}