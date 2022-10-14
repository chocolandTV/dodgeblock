
from operator import truediv
import pygame
import math
import entities
import player
import settings
import random
import sys

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

# creating enemylist
enemylist = []

# Clock
clock = pygame.time.Clock()

# Settings init
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

_settings = settings.Settings()
game_over = False


def message(msg, color):
    mesg = my_font.render(msg, True, color)
    _settings.screen.blit(mesg, (_settings.width/2, _settings.height/2))

############### GAME LOOP ###############
GameState_running = 0
currenttime = 0
# 0 splash screen /// 1 Spawn  /// 2 Game   //// 3 Gameover
while True:
    #####################  INTRO ######################
    if GameState_running == 0:
        img = pygame.image.load("splash.png")
        _settings.screen.fill((255, 255, 255))
        _settings.screen.blit(img, (10, 10))
        
        clock.tick()
        currenttime += clock.get_rawtime()
        pygame.display.update()
        print (currenttime)
        if currenttime >= 2000:
            _settings.screen.fill((0, 0, 0))

            GameState_running = 1
    #####################  GAME OVER ######################
    if GameState_running == 3:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_F4:
                    GameState_running = 0
                    del _player
                    for obj in enemylist:
                        del obj

            if event.type == QUIT:
                pygame.quit()

        message("Retry : F4 or Return", (255, 0, 0))
        pygame.display.update()

        # Show Score BIG
        # Show Highscore
    ################ START GAME ###############
    if GameState_running == 1:
    
        # Speed per Second
        counter = 0
        # PixelperSecond
        currenttime = 0
        lasttime = 0
        ################# Create Player ################
        _player = player.Player((500, 350), (0, 0, 250),
                                32, 2, _settings, enemylist, 250)
        ################ Create Enemys -( POSITION X,Y - COLOR - SIZE, DELAY , PLAYER, BEHAVIOUR, PRIORITY) ##################
        enemylist.clear()
        enemylist.append(entities.Enemy(
            (1400, 200), (255, 0, 0), 50, 10, _player, entities.Enemy.Move_Corners, 1))
        enemylist.append(entities.Enemy(
            (1100, 300), (255, 0, 0), 50, 8, _player, entities.Enemy.Move_toPlayerX, 1))
        enemylist.append(entities.Enemy(
            (800, 400), (255, 0, 0), 50, 8, _player, entities.Enemy.Move_toPlayerY, 1))
        enemylist.append(entities.Enemy(
            (600, 500), (255, 0, 0), 50, 5, _player, entities.Enemy.Move_Borders, 1))
        enemylist.append(entities.Enemy(
            (500, 600), (255, 0, 0), 50, 8, _player, entities.Enemy.Move_Corners, 1))
        enemylist.append(entities.Enemy(
            (400, 700), (255, 0, 0), 50, 5, _player, entities.Enemy.Move_Borders, 1))
        enemylist.append(entities.Enemy(
            (300, 800), (255, 0, 0), 50, 10, _player, entities.Enemy.Move_toPlayerX, 1))
        enemylist.append(entities.Enemy(
            (200, 900), (255, 0, 0), 50, 8, _player, entities.Enemy.Move_toPlayerY, 1))
        GameState_running = 2
    ############################ Game Running ############################## 
    if GameState_running == 2:
        _settings.screen.fill((0, 0, 0))
        ##################### TIME UPDATE #########################
        clock.tick()
        currenttime += clock.get_rawtime()
        ##################### Spawn Enemy after 1 Minute ##########
        # print(currenttime)
        if currenttime >= 5000:
            # print(currenttime)
            enemylist.append(entities.Enemy((0, 0), (random.randint(0, 255), random.randint(
                0, 255), 0), random.randint(25, 100), random.randint(15, 30), _player, entities.Enemy.Move_toTarget, 0))
            currenttime = 0
        ##################### CHECK COLLISION #####################
        for obj in enemylist:
            if (pygame.Rect.colliderect(pygame.Rect(_player.playerPos.x, _player.playerPos.y, _player.size, _player.size), pygame.Rect(obj.EnemyPos.x, obj.EnemyPos.y, obj.size, obj.size))):
                obj.tick(clock.get_time())
                GameState_running = 3
                print(" Game Over")
            else:
                obj.tick(clock.get_time())
        _player.tick(clock.get_time())

        for event in pygame.event.get():
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    GameState_running = 3
            if event.type == QUIT:
                GameState_running = 3
        ############ SCORE UPDATE #################
        counter += len(enemylist)
        # highscore Printen
        ############ UI UPDATE ####################
        textsurface = my_font.render(" HIGHSCORE: " +
                                     str(math.floor(counter/1000)), False, (255, 255, 255))
        _settings.screen.blit(textsurface, (0, 0))
        pygame.display.update()
