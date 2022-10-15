import pygame
import pygame.font
pygame.font.init()
class Settings():

    def __init__(self):
        self.width = 1400
        self.height = 1000
        self.defaultSize = 32
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.Gameversion = "0.10"
        self.PlayerName = "anonymous"