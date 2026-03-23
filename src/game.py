import pygame, sys
from settings.settings import *
from scenes import Level
from ui import Renderer

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.level = Level(self.renderer)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("blue")
            self.level.update()
            self.level.draw()
            pygame.display.update()
            self.clock.tick(60)


game = Game()
game.run()
