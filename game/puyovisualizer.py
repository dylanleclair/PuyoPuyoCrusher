import sys
import pygame
import puyoenv


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
        self.player1 = Player(puyoenv.chain_19)
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
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if self.player1.falling and not (counter % 3):
                # compute the optimal move, and make it!
                
                # feed the board into the search
                if len(self.player1.moves_to_make) > 0:
                    # make the move, and wait
                    
                else: 
                    # perform the search
                    self.player1.moves_to_make = self.player1.searcher.search()

                keys = pygame.key.get_pressed()
                col1, row1 = self.player1.falling[0]['pos']
                col2, row2 = self.player1.falling[1]['pos']
                if keys[self.player1.controller['left']]:
                    if (row1 > 0 and self.player1.board[col1][row1 - 1] == ' ') and (
                            row2 > 0 and self.player1.board[col2][row2 - 1] == ' '):
                        self.player1.falling[0]['pos'] = (col1, row1 - 1)
                        self.player1.falling[1]['pos'] = (col2, row2 - 1)
                if keys[self.player1.controller['right']]:
                    if (row1 < self.player1.w - 1 and self.player1.board[col1][row1 + 1] == ' ') and (
                            row2 < self.player1.w - 1 and self.player1.board[col2][row2 + 1] == ' '):
                        self.player1.falling[0]['pos'] = (col1, row1 + 1)
                        self.player1.falling[1]['pos'] = (col2, row2 + 1)
                if keys[self.player1.controller['down']]:
                    if (col1 < self.player1.h - 1 and self.player1.board[col1 + 1][row1] == ' ') and (
                            col2 < self.player1.h - 1 and self.player1.board[col2 + 1][row2] == ' '):
                        self.player1.falling[0]['pos'] = (col1 + 1, row1)
                        self.player1.falling[1]['pos'] = (col2 + 1, row2)
                if keys[self.player1.controller['roll']]:
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
