import sys
import pygame
import puyoenv
import helpers

class Player(puyoenv.PuyoEnv):
    offset = (100, 100)
    controller = {'left': pygame.K_LEFT,
                  'down': pygame.K_DOWN,
                  'right': pygame.K_RIGHT,
                  'roll': pygame.K_a}


class Game:

    def __init__(self, screen=(640, 480)):
        pygame.init()
        self.screen = pygame.display.set_mode(screen)
        self.puyo = {'1': pygame.transform.scale(pygame.image.load('resource/r.png').convert_alpha(), (24, 24)),
                     '2': pygame.transform.scale(pygame.image.load('resource/g.png').convert_alpha(), (24, 24)),
                     '3': pygame.transform.scale(pygame.image.load('resource/b.png').convert_alpha(), (24, 24)),
                     '4': pygame.transform.scale(pygame.image.load('resource/y.png').convert_alpha(), (24, 24))}
        self.x = pygame.image.load('resource/x.png').convert_alpha()
        self.player1 = Player()
        self.screen.fill((255, 255, 255),
                         (self.player1.offset[0], self.player1.offset[1],
                          self.player1.w * 24, self.player1.h * 24))
        self.draw(self.player1)
        pygame.display.update()
        self.clock = pygame.time.Clock()

    def draw(self, p):
        x_offset, y_offset = p.offset
        self.screen.blit(self.x, (x_offset + 2 * 24, y_offset + 1 * 24))
        for y, row in enumerate(p.board):
            for x, colour in enumerate(row):
                if colour != ' ':
                    self.screen.blit(self.puyo[colour], (x_offset + x * 24, y_offset + y * 24))
        if p.falling:
            for i in range(2):
                y, x = p.falling[i]['pos']
                if y >= 0 and x >= 0:
                    self.screen.blit(self.puyo[p.falling[i]['colour']], (x_offset + x * 24, y_offset + y * 24))

    def play(self):
        counter = 0
        while True:
            counter += 1
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if self.player1.falling and not (counter % 3):

                keys = pygame.key.get_pressed()
                col1, row1 = self.player1.falling[0]['pos']
                col2, row2 = self.player1.falling[1]['pos']
                '''
                print(col1,row1)
                print(col2,row2)
                print('current',self.player1.current)
                '''
                
                code = helpers.get_code(row1,col1,row2,col2)
                print('code',code)
                
                
                # compute the optimal move, and make it!
                actions = [0,0,0,0]
                # feed the board into the search
                if len(self.player1.moves_to_make) > 0:
                    # make the move, and wait
                    # calculate what move to make to align with the desired move (first in list)
                    # create fake input to mimic this
                    move = self.player1.moves_to_make[0]
                    print('move', move)
                    if (code != move):
                        
                        if code[1] != move[1]: # the alignment does not match
                            actions[3] = 1
                        else:
                            if (code[0] < move[0]): # if the move specifies a greater col, move right
                                actions[1] = 1
                            else: # move left
                                actions[0] = 1
                            


                    else: # the piece is in the correct column, with correct orientation    
                        # all we gotta do is move down
                        actions[2] = 1

                else: 
                    # perform the search
                    print(self.player1.moves_to_make)
                    result = self.player1.searcher.search()
                    self.player1.moves_to_make = result.moves
                    if not self.player1.moves_to_make:
                        self.player1.moves_to_make.append((5,1))
                    else: 
                        helpers.print_board(result.board)
                        print('ai recommends moves:', result.moves)

                
                if actions[0]:
                    if (row1 > 0 and self.player1.board[col1][row1 - 1] == ' ') and (
                            row2 > 0 and self.player1.board[col2][row2 - 1] == ' '):
                        self.player1.falling[0]['pos'] = (col1, row1 - 1)
                        self.player1.falling[1]['pos'] = (col2, row2 - 1)
                if actions[1]:
                    if (row1 < self.player1.w - 1 and self.player1.board[col1][row1 + 1] == ' ') and (
                            row2 < self.player1.w - 1 and self.player1.board[col2][row2 + 1] == ' '):
                        self.player1.falling[0]['pos'] = (col1, row1 + 1)
                        self.player1.falling[1]['pos'] = (col2, row2 + 1)
                if actions[2]:
                    if (col1 < self.player1.h - 1 and self.player1.board[col1 + 1][row1] == ' ') and (
                            col2 < self.player1.h - 1 and self.player1.board[col2 + 1][row2] == ' '):
                        self.player1.falling[0]['pos'] = (col1 + 1, row1)
                        self.player1.falling[1]['pos'] = (col2 + 1, row2)
                if actions[3]:
                    col1, row1 = self.player1.falling[0]['pos']
                    col2, row2 = self.player1.falling[1]['pos']
                    a1 = col1 - col2
                    a2 = row1 - row2
                    if (row1 + a1 in (-1, self.player1.w)) or col1 - a2 == self.player1.h or \
                            self.player1.board[col1 - a2][row1 + a1] != ' ':
                        pass
                    else:
                        self.player1.falling[1]['pos'] = (col1 - a2, row1 + a1)
            if not (counter % 50):
                self.player1.update(display=True)
            self.screen.fill((255, 255, 255),
                             (self.player1.offset[0],
                              self.player1.offset[1],
                              self.player1.w * 24,
                              self.player1.h * 24)
                             )
            self.draw(self.player1)
            pygame.display.update()
            if counter == 300:
                counter = 0


if __name__ == '__main__':
    Game().play()
