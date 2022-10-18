import pygame
import pygame.font
pygame.font.init()
class Settings():

    def __init__(self):
        self.width = 1400
        self.height = 1000
        self.defaultSize = 32
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.small_font = pygame.font.SysFont('Arial Black', 18)
        self.big_font = pygame.font.SysFont('Arial Black', 50)
        self.tall_font = pygame.font.SysFont('Arial Black', 70)
        self.Gameversion = "0.91"
        self.PlayerName = "anonymous"
        self.highscoreHeight= 160
        