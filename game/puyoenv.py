import copy
import random
import ai
import helpers

class PuyoEnv:
    w = 6
    h = 13

    def __init__(self, template=None):
        self.board = [[' ' for x in range(self.w)] for y in range(self.h)]
        self.prev_board = [[' ' for x in range(self.w)] for y in range(self.h)]
        self.chain = 0
        self.puyo_to_remove = set()
        self.falling = None
        self.trigger = None
        self.moves = [((-1, 0), (0, 0)),
                      ((-1, 1), (0, 1)),
                      ((-1, 2), (0, 2)),
                      ((-1, 3), (0, 3)),
                      ((-1, 4), (0, 4)),
                      ((-1, 5), (0, 5)),
                      ((0, 0), (-1, 0)),
                      ((0, 1), (-1, 1)),
                      ((0, 2), (-1, 2)),
                      ((0, 3), (-1, 3)),
                      ((0, 4), (-1, 4)),
                      ((0, 5), (-1, 5)),
                      ((-1, 0), (-1, 1)),
                      ((-1, 1), (-1, 2)),
                      ((-1, 2), (-1, 3)),
                      ((-1, 3), (-1, 4)),
                      ((-1, 4), (-1, 5)),
                      ((-1, 1), (-1, 0)),
                      ((-1, 2), (-1, 1)),
                      ((-1, 3), (-1, 2)),
                      ((-1, 4), (-1, 3)),
                      ((-1, 5), (-1, 4))]
        self.buffer = [self.next(), self.next()]
        self.current = self.next()

        # AI specific
        self.moves_to_make = []
        
        self.searcher = ai.Search(self.board, [self.current] + self.buffer)
        # end of ai specific
        
        row = 0
        col = 0
        if template:
            for puyos in template:
                if puyos == "\n":
                    col += 1
                    row = 0
                    continue
                else:
                    self.board[col][row] = puyos
                    row += 1

    def next(self):
        return random.choice(['1', '2', '3', '4']), random.choice(['1', '2', '3', '4'])

    def scan(self, col, row, chained, color):
        if row < self.w - 1:
            chained = self._check_neighbor(col, row + 1, chained, color)
        if col < self.h - 1:
            chained = self._check_neighbor(col + 1, row, chained, color)
        if row > 0:
            chained = self._check_neighbor(col, row - 1, chained, color)
        if col > 0:
            chained = self._check_neighbor(col - 1, row, chained, color)
        return chained

    def _check_neighbor(self, col, row, chained, color):
        ar_color = self.board[col][row]
        if color == ar_color:
            if (col, row) in chained:
                return chained
            chained.append((col, row))
            chained = self.scan(col, row, chained, color)
        return chained

    def fill(self):
        prev_board = None
        while self.board != prev_board:
            prev_board = copy.deepcopy(self.board)
            for col in range(12, 0, -1):
                for row in range(6):
                    if self.board[col][row] == ' ':
                        self.board[col][row] = self.board[col - 1][row]
                        self.board[col - 1][row] = ' '

    def remove_puyo(self, puyos):
        for x in puyos:
            self.board[x[0]][x[1]] = ' '
        self.puyo_to_remove = set()

    def drop(self):
        self.fill()
        for col in range(self.h):
            for row in range(self.w):
                if (col, row) in self.puyo_to_remove:
                    continue
                color = self.board[col][row]
                chained = [(col, row)]

                if color != ' ':
                    chained = self.scan(col, row, chained, color)

                    if len(chained) >= 4:
                        self.puyo_to_remove = self.puyo_to_remove.union(chained)

    def move(self, display=False):
        self.drop()
        if display:
            self.chain += 1
            if self.chain == 1:
                self.trigger = True
            else:
                self.trigger = False
            self.remove_puyo(self.puyo_to_remove)
            self.drop()
        else:
            while self.puyo_to_remove:
                self.chain += 1
                if self.chain == 1:
                    self.trigger = True
                else:
                    self.trigger = False
                self.remove_puyo(self.puyo_to_remove)
                self.drop()

    def update(self, display=False):
        if self.falling is None:
            self.prev_board = copy.deepcopy(self.board)
            self.move(display=display)
            if self.board == self.prev_board:
                self.chain = 0
                if self.board[1][2] != ' ':
                    print("GAME OVER")
                    return False
                else:
                    # add a new piece
                    colour0, colour1 = self.buffer.pop(0)
                    self.falling = ({'colour': colour0, 'pos': (-1, 2)},
                                    {'colour': colour1, 'pos': (0, 2)})
                    self.buffer.append(self.next())
                    self.current = (colour0,colour1)
                    if len(self.moves_to_make) > 0:
                        self.moves_to_make.pop(0)
                    self.searcher = ai.Search(self.board, [self.current] + self.buffer)
                    # initialize the search
        else:
            col1, row1 = self.falling[0]['pos']
            col2, row2 = self.falling[1]['pos']
            if (col1 == (self.h - 1) or self.board[col1 + 1][row1] != ' '
                    or col2 == (self.h - 1) or self.board[col2 + 1][row2] != ' '):
                self.board[col1][row1] = self.falling[0]['colour']
                self.board[col2][row2] = self.falling[1]['colour']
                self.falling = None
                
            else:
                self.falling[0]['pos'] = (col1 + 1, row1)
                self.falling[1]['pos'] = (col2 + 1, row2)

        return True

    def place(self, move):
        pos0, pos1 = self.moves[move]
        col0, col1 = self.current
        self.board[pos0[0] + 1][pos0[1]] = col0
        self.board[pos1[0] + 1][pos1[1]] = col1
        self.drop()

    def play(self, move):
        self.prev_board = copy.deepcopy(self.board)
        self.place(move)
        self.chain = 0
        self.move()
        if self.board[1][2] != ' ':
            print("GAME OVER")
            return False
        else:
            self.current = self.buffer.pop(0)
            self.buffer.append(self.next())
        return True


chain_19 = \
    """  3211
122323
323211
123213
232123
321213
232121
232121
211313
123233
312321
312321
312321"""


def main():
    pe = PuyoEnv()
    for x in range(25):
        pe.play(random.randint(0, 21))
        boards = 'Boards:\n'
        for horizontal in zip(pe.board, pe.prev_board):
            boards += ''.join(horizontal[0]) + ' ' + ''.join(horizontal[1]) + '\n'
        print(boards)
        print(f'Chain: {pe.chain}')
        print(f'Puyo Buffer: {pe.buffer}')


if __name__ == '__main__':
    main()
