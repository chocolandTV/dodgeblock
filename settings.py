import pygame

class Settings():

    def __init__(self):
        self.width = 1400
        self.height = 1000
        self.defaultSize = 32
        self.screen = pygame.display.set_mode((self.width, self.height))