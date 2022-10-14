from turtle import pos
import pygame
import settings
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_RETURN,
    K_F4,
    QUIT
)


class Player():

    def __init__(self, startposition, color, size, delay, settings, enemylist, spawnRadius):
        self.screen = settings.screen
        self.settings = settings
        self.color = color
        self.size = size
        self.delay = delay
        self.playerSpeedCounter = 0
        self.counter = 0
        self.playerPos = pygame.Vector2(startposition[0], startposition[1])
        self.EnemyList = enemylist
        self.SpawnRadius = spawnRadius

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[pygame.K_a]:
            if self.playerPos.x > 0:
                self.playerPos.x -= 1
                if not keys[K_RIGHT]:
                    self.counter += 1

        if keys[K_RIGHT] or keys[pygame.K_d]:
            if self.playerPos.x < self.settings.width - self.settings.defaultSize:
                self.playerPos.x += 1
                if not keys[K_LEFT]:
                    self.counter += 1

        if keys[K_UP] or keys[pygame.K_w]:
            if self.playerPos.y > 0:
                self.playerPos.y -= 1
                if not keys[K_DOWN]:
                    self.counter += 1

        if keys[K_DOWN] or keys[pygame.K_s]:
            if self.playerPos.y < self.settings.height-self.settings.defaultSize:
                self.playerPos.y += 1
                if not keys[K_UP]:
                    self.counter += 1

    def tick(self, _clocktime):
        self.playerSpeedCounter += _clocktime
        self.player_draw()
        if (self.playerSpeedCounter >= self.delay):
            self.playerSpeedCounter = 0
            self.move()
            

    def player_draw(self):
        pygame.draw.rect(self.screen, self.color, (self.playerPos.x,
                                                       self.playerPos.y, self.size, self.size))
