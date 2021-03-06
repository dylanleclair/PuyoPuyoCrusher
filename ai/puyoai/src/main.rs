//! This is a simple module
mod scoring;
mod ai;

use std::collections::HashSet;
use std::collections::VecDeque;
use std::vec;
use std::cmp;

use actix_web::{post, web, HttpResponse, Result};
use serde::{Deserialize, Serialize};
const POWERS: [i32; 19] = [
    0, 8, 17, 23, 35, 71, 118, 178, 239, 300, 377, 454, 534, 613, 693, 699, 699, 699, 699,
];

const COLORS_BONUS: [i32; 5] = [0, 3, 6, 12, 24];

const DEPTH: u8 = 5;

const COLORS: [i32;4] = [1,2,3,4];

#[derive(Serialize, Deserialize)]
struct Board {
    width: i32,
    height: i32,
    board: Vec<Vec<u8>>,
    buffer: VecDeque<(u8,u8)>
}

#[derive(Serialize,Deserialize)]
struct Moves {
    moves: Vec<(u8,u8)>
}

#[post("/")]
async fn serve_board(body: web::Json<Board>) -> Result<HttpResponse> {

    // perform a search
    let moves = body.buffer.clone();

    let mut s = ai::Search::new(&body.board, moves); // can change moves to a static reference!

    let mut r = s.search();

    // if the board is mostly uncovered, then truncate the output so that a new best move is calculated next round
    if board_coverage(&body.board) < 0.7 
    {
        // then, trigger the AI to break the chain (ie: do not cut the output short)
        r.truncate(1);
    } 

    // return the calculated moves
    Ok(HttpResponse::Ok().json(Moves {
        moves: r,
    }))

}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    use actix_web::{App, HttpServer};

    HttpServer::new(|| App::new().service(serve_board))
        .bind("127.0.0.1:8080")?
        .run()
        .await
}

// fn main() {
//     // create a board with 6 columns and 12 rows, using 8bit unsigned integers
//     //let arr: [[u8; 6]; 12] = [[0; 6]; 12];
//     //for x in &arr {
//     //    println!("x is {:?}", x);
//     //}
//     //println!("Board is: {:?}!", arr);


//     // let mut score = scoring::Score::new();
//     // let results = drop_board(&my_board, &mut score);
//     // println!("w{:?}", results);
//     // score.report();

//     // println!("projected score: {}",projected_score(my_board).1);
// }

/// Creates a blank board with the specified width and height
fn _new_board(w: usize, h: usize) -> Vec<Vec<u8>> {
    let mut output = Vec::new();
    for _i in 0..h {
        output.push(vec![0; w]);
    }
    return output;
}

/// Prints a board out in a human readable format
fn _print_board(board: &Vec<Vec<u8>>) {
    println!("Board:");
    for x in board {
        println! {"{:?}",x}
    }
}

/// Adds a puyo to the board, with the specified colour at the highest empty row in the specified column.
/// Make sure to copy the board before performing placements.
fn place(board: &mut Vec<Vec<u8>>, color: u8, column: u8) {
    // copy the board
    for i in 1..board.len() {
        // iterate from top to bottom of a column, 
        // until a color is reached
        if !(board[i][column as usize] == 0) {
            board[i - 1][column as usize] = color; // place the color above the last item!
            break;
        } else if i == (board.len() - 1) {
            board[i][column as usize] = color;
        }
    }
}

/// Takes a board and a reference to a Score.
/// Marks the Puyos to remove, and updates the score information
fn drop_board(board: &Vec<Vec<u8>>, score: &mut scoring::Score) -> HashSet<(u8, u8)> {
    let h = board.len(); // find the height
    let w = board[0].len(); // find the width
                            // Board is intrinsically a copy
    let mut to_remove: HashSet<(u8, u8)> = HashSet::new();

    for col in 0..h {
        for row in 0..w {
            if to_remove.contains(&(col as u8, row as u8)) {
                continue;
            }
            let color = board[col][row];
            // probably want to switch chained to a vector
            let mut chained: HashSet<(u8, u8)> = HashSet::new();
            chained.insert((col as u8, row as u8));
            if color != 0 {
                scan(&board, col, row, &mut chained, color);
                let c_size = chained.len();
                if c_size >= 4 {
                    for x in chained {
                        to_remove.insert(x);
                    }
                    score.chain_size += c_size as i32;
                    score.colors_in_chain.push(color);
                    score.chain_group_sizes.push(c_size as i32);
                }
            }
        }
    }
    return to_remove;
}

/// Scans for adjacent tiles of the same color
fn scan(board: &Vec<Vec<u8>>, col: usize, row: usize, chained: &mut HashSet<(u8, u8)>, color: u8) {
    let h = board.len(); // find the height
    let w = board[0].len(); // find the width
    if row < w - 1 {
        check_neighbor(board, col, row + 1, chained, color);
    }
    if col < h - 1 {
        check_neighbor(board, col + 1, row, chained, color);
    }
    if row > 0 {
        check_neighbor(board, col, row - 1, chained, color);
    }
    if col > 0 {
        check_neighbor(board, col - 1, row, chained, color);
    }
}

/// Recursively performs scans to locate an entire chain
fn check_neighbor(
    board: &Vec<Vec<u8>>,
    col: usize,
    row: usize,
    chained: &mut HashSet<(u8, u8)>,
    color: u8,
) {
    let ar_color = board[col][row];
    if color == ar_color {
        if chained.contains(&(col as u8, row as u8)) {
            return;
        }
        chained.insert((col as u8, row as u8));
        scan(board, col, row, chained, color);
    }
}

fn projected_score(board: Vec<Vec<u8>>) -> (Vec<Vec<u8>>,i32) {
    let mut b = board.to_vec();
    let mut s = scoring::Score::new();
    let mut to_remove = drop_board(&board, & mut s);
    let mut chain = 0;
    while to_remove.len() > 0 {
        remove_puyos(&mut b, & mut to_remove);
        
        // apply gravity
        correct_board(&mut b);

        to_remove = drop_board(&b,& mut s);
        chain += 1;
    }
    s.chain = chain;
    return (b,get_score(&s));
    
}

fn chain_power(chain: i32) -> i32 {
    if chain == 0 {
        return 0;
    }

    else if chain < POWERS.len() as i32 {
        return POWERS[(chain - 1) as usize];
    } else {
        return POWERS[POWERS.len() - 1];
    }
}

fn color_bonus(num_colors: usize) -> i32 {
    if num_colors == 0 {
        return 0;
    }
    if num_colors < COLORS_BONUS.len() {
        return COLORS_BONUS[num_colors - 1];
    }
    return COLORS_BONUS[COLORS_BONUS.len() - 1];
}

fn group_bonus(groups: &Vec<i32>) -> i32 {
    let mut local_sum = 0;
    for &i in groups {
        if i == 4 {
            local_sum += 0;
        } else if i <= 10 {
            local_sum += i - 3;
        } else {
            local_sum += 10;
        }
    }
    return local_sum;
}

fn remove_puyos(board:& mut Vec<Vec<u8>>, puyos:& mut HashSet<(u8,u8)>) {
    for x in puyos.iter()
    {
        let (a,b) = *x;
        board[a as usize][b as usize] = 0;
    }
    puyos.clear();

}

fn check_correctness(board:& Vec<Vec<u8>>) -> bool
{
    for c in 0..board[0].len()
    {
        for r in 0..(board.len()-1)
        {
            if board[r+1][c] == 0 && !(board[r][c] == 0)
            {
                return false;
            }
        }
    }
    return true;
}

fn correct_board(board:&mut Vec<Vec<u8>>) {
    // corrects the board after puyos are removed from it (in the even gaps exist)
    while !check_correctness(board){
        apply_gravity(board);
    }
}

fn apply_gravity(board:&mut Vec<Vec<u8>>) {
    let h = board.len() - 1; // find the height
    let w = board[0].len(); // find the width
    for c in 0..w {
        for r in 0..h {
            if board[r+1][c] == 0 && !(board[r][c]==0) {
                board[r+1][c] = board[r][c];
                board[r][c] = 0;
            }
            
        } 
    }

}

fn get_score(score:& scoring::Score) -> i32
{
    let m = cmp::min(chain_power(score.chain) + color_bonus(score.colors_in_chain.len()) +group_bonus(&score.chain_group_sizes),999);
    return (10 * score.chain_size) * cmp::max(1,m) 
}

/// Returns the normalized value representing the percentage of the board that is filled. 
fn board_coverage(board:&Vec<Vec<u8>>) -> f32 {
    let w = board[0].len();
    let h = board.len();

    let mut count = 0;

    // count non-zero values on board
    for i in board {
        for j in i {
            if *j != 0 {
                count += 1;
            }
        }
    }

    count as f32 / (w * h) as f32

}

/// Computes every single distinct possible puyo piece
fn compute_all_puyos(colors:&Vec<u8>) -> Vec<(u8,u8)>
{
    // for N colors, there are N^2 distinct puyo puyo pieces.
    let mut all_puyos = Vec::new();


    // thankfully, div handles all orientations of a piece
    // so, for ex. we can treat (1,2) and (2,1) as equivalent
    // hence the division by 2 above

    for i in 0..colors.len() {
        for j in 0..colors.len()
        {
            if !all_puyos.contains(&(colors[i],colors[j])) {
                all_puyos.push((colors[i],colors[j]));
            }
        }
    }
    all_puyos
}

#[cfg(test)]
mod tests {
    #[test]
    fn compute_puyos_correctness(){
        let sample: Vec<u8> = vec![1,2,3,4];

        let results = super::compute_all_puyos(&sample);
        
        let expected: Vec<(u8,u8)> = vec![(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(3,4),(4,1),(4,2),(4,3),(4,4)];
        assert_eq!(results,expected);
    }

    #[test]
    fn place_correctness(){
        let mut b = super::_new_board(6, 12);
        let mut copy = b.clone();

        super::place(&mut b, 3, 1);
        super::place(&mut b, 2, 1);
        super::place(&mut b, 1, 1);

        copy[11][1] = 3;
        copy[10][1] = 2;
        copy[9][1] = 1;

        assert_eq!(copy, b);
    }

}
