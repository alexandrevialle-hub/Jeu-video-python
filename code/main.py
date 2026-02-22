import pygame
import sys
from settings import *
from level import Level
from player import Player
from weapon import create_weapons

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Zelda de Golmon')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.main_sound = pygame.mixer.Sound('song/main.mp3')
        self.main_sound.set_volume(0.5)
        self.main_sound.play(loops=-1)

    def get_screen(self):
        return self.screen

    def get_clock(self):
        return self.clock

    def get_level(self):
        return self.level

    def set_screen(self, screen):
        self.screen = screen

    def set_clock(self, clock):
        self.clock = clock

    def set_level(self, level):
        self.level = level

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()