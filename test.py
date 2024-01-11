import sys

import pygame

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Kyle's Chess in Python")
        self.screen = pygame.display.set_mode((1000, 800))
        
        self.clock = pygame.time.Clock()

        self.img = pygame.image.load('assets/images/pawnRed.png')

        #dont think i'll need this since my images will be transparent pngs
        #self.img.set_colorkey((0,0,0))

        self.img = pygame.transform.scale(self.img, (400,400))
        self.img_pos = [0,0]
        self.movement = [False, False]

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))
            self.img_pos[1] += self.movement[1] - self.movement[0]
            self.screen.blit(self.img, self.img_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(60)

Game().run()