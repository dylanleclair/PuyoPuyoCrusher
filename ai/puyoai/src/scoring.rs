pub struct Score {
    pub chain: i32,
    pub chain_size: i32,
    pub colors_in_chain: Vec<u8>,
    pub chain_group_sizes: Vec<i32>,
}
impl Score {
    pub fn new() -> Score {
        return Score {
            chain: 0,
            chain_size: 0,
            colors_in_chain: Vec::new(),
            chain_group_sizes: Vec::new(),
        };
    }
    pub fn _report(&mut self) {
        println!(
            "x-Chain: {}, Chain size: {}, Colors in chain: {:?}, Chain group sizes: {:?}",self.chain + 1,
            self.chain_size, self.colors_in_chain, self.chain_group_sizes
        );
    }
}
