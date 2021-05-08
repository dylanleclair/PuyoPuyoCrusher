//! The search class

struct Node {
    board: Vec<Vec<u8>>,
    buffer: Vec<(u8,u8)>,
    score_acc: i32,
    moves: Vec<(u8,u8)> 
}

impl Node {
    pub fn new (
        b: Vec<Vec<u8>>,
        buf: Vec<(u8,u8)>,
        score: i32,
        moveset: Vec<(u8,u8)>) -> Node {
            return Node {
                board:b,
                buffer: buf,
                score_acc: score,
                moves: moveset
            };
        }
    
    pub fn div(self) {
        let mut new : Vec<Node> = Vec::new();

        let piece = self.buffer[0];
        let piece = (piece.1,piece.0); // reverse it so encoding works properly
        
        if piece.0 == piece.1 
        {

        } else {
            
        }
    } 

}