//! The search class
use std::collections::VecDeque;

struct Node {
    board: Vec<Vec<u8>>,
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
    pub fn div(&mut self, piece:(u8,u8)) -> Vec<(Vec<Vec<u8>>,(u8,u8))> {
        let mut new : Vec<(Vec<Vec<u8>>,(u8,u8))> = Vec::new();

        let piece = (piece.1,piece.0); // reverse it so encoding works properly
        let w = self.board[0].len();
        if piece.0 == piece.1 
        {
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
    fn advance(&mut self, stack: &mut Vec<Node>) {

        if self.buffer.len() == 0 {
            return;
        }

        let mut buffer = self.buffer.clone(); // copy the buffer -> this is to be the buffer in the next node
        let next_piece: (u8,u8) = buffer.pop_front().expect("Buffer is empty."); // get the first move

        let new_boards =  self.div(next_piece);

        for pair in new_boards {
            let board = pair.0;
            let next_move = pair.1;
            
            let mut new_moves = self.moves.to_vec(); // clone the accumulated moves
            new_moves.push(next_move); // add the new move to end of accumulated

            let results = super::projected_score(board);

            // @TODO shouldn't need to return the board unless you are reconsidering after every move
            // since no side effects are possible using the current heuristic

            let new = Node::new(results.0, buffer.clone(), self.score_acc + results.1, new_moves);
            stack.push(new);
        }

    }

}