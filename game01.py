import pygame
import math
import entities
import player
import settings
import random
import highscore as h
import inputbox

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_RETURN,
    K_F4,
    K_BACKSPACE,
    QUIT
)
def Credits(gamestate, _Counter):
    while gamestate == -1:
        
        _settings.screen.fill((255, 255, 255))
        textsurface0 = _settings.big_font.render(("SCRIPT WRITER"), False, (0, 0, 0))
        textsurface1 = _settings.big_font.render(("Robert Moegenburg"), False, (0, 0, 0))
        textsurface2 = _settings.big_font.render(("Special Thanks"), False, (0, 0, 0))
        textsurface3 = _settings.big_font.render(("MisterIXI"), False, (0, 0, 0))
        _settings.screen.blit(textsurface0, (640, 500))
        _settings.screen.blit(textsurface1, (640, 550))
        _settings.screen.blit(textsurface2, (640, 700))
        _settings.screen.blit(textsurface3, (640, 750))
        pygame.display.update()
        _Counter += 1
        if _Counter >= 5000:
            gamestate=0
        
    return gamestate, _Counter

pygame.init()

_settings = settings.Settings()
# creating enemylist
enemylist = []
difficult = 5000
############### Gamestate ###############
gamestate = 0
############### running time ####################
currenttime = 0
totaltime = 0
# Clock
clock = pygame.time.Clock()
# Highscore
_highscore = h.HighscoreManager()
_highscore.PlayerHighscore = 0
# GameOver State
game_over = False
_rect_Start = pygame.Rect(444,328,441,99)
_rect_Credits= pygame.Rect(444,463,441,99)
_rect_Exit = pygame.Rect(444,600,4441,95)

# 0 splash screen and Hmenu  /// 1 Spawn  /// 2 Game   //// 3 Gameover
while True:
    #####################  INTRO AND MENU ######################
    if gamestate == 0:
        img = pygame.image.load("splash.png")
        _settings.screen.fill((255, 255, 255))
        _settings.screen.blit(img, (0, 0))
        ################## Time update ###################
        clock.tick()
        currenttime += clock.get_rawtime()
        pygame.display.update()
        ################# Main Menu #################
        
        if _settings.PlayerName == "anonymous" and currenttime >= 3000:
            img = pygame.image.load("Hmenu.png")
            _settings.screen.blit(img, (0, 0))
            
            ################# Display Input Box  ####################
            textsurface = _settings.small_font.render(("Playername:     (type in and press Return)"), False, (255, 0, 0))
            _settings.screen.blit(textsurface, (500, 250))
            input_box1 = inputbox.InputBox(520,280, 300, 40)
            done = False
            pygame.display.update()
            ################### input loop ################
            while not done:
                _settings.screen.blit(img, (0, 0))
                _settings.screen.blit(textsurface, (500, 250))
                        
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    input_box1.handle_event(event)
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN or event.key == K_F4:
                            done = True
                        elif event.key == K_BACKSPACE:
                            input_box1.text = input_box1.text[:-1]
                    ###### Mouse Click  switch State Start, Credits and Exit
                input_box1.draw(_settings.screen)
                if pygame.mouse.get_pressed(3)[0] == True:
                    x,y = pygame.mouse.get_pos()
                    if(gamestate == 0 and x >= _rect_Start.left and x <= _rect_Start.right and y <= _rect_Start.bottom and y >= _rect_Start.top):
                        print (" Start Button")
                        gamestate = 1
                        done=True
                    elif(gamestate == 0 and x >= _rect_Credits.left and x <= _rect_Credits.right and y <= _rect_Credits.bottom and y >= _rect_Credits.top):
                        print (" Credits Button")
                        gamestate = -1
                        _Counter =0
                        creditReturn=Credits(gamestate, _Counter)
                        gamestate = creditReturn[0]
                        _Counter= creditReturn[1]
                        
                    elif(gamestate == 0 and x >= _rect_Exit.left and x <= _rect_Exit.right and y <= _rect_Exit.bottom and y >= _rect_Exit.top):
                        print (" Exit Button")
                        pygame.quit()    
                pygame.display.flip()
                ############ output and define var #################
            if input_box1.text != "":
                _settings.PlayerName = input_box1.text
            gamestate = 1
        else:
            if currenttime >= 3000:
                gamestate = 1
        
    #####################  GAME OVER ######################
    if gamestate == 3:
        _settings.screen.fill((70, 70, 70))
        textsurface = _settings.big_font.render(("Please try again : Press F4 or Return"), False, (255, 0, 0))
        _settings.screen.blit(textsurface, (25, 25))
        ################# Leaderboard image ###################
        imgLeaderboard = pygame.image.load("leaderboard.png")
        _settings.screen.blit(imgLeaderboard, (0, 0))
        #################  Highscore on Screen #######################
        
        scorelist =_highscore.highscorestring()
        for y in range(len(scorelist)):
            imgEntry = pygame.image.load("entry.png")
            _settings.screen.blit(imgEntry, (0,_settings.highscoreHeight-7+(40*(y+1))))
            tempstring = scorelist[y].split(", ")
            
            for x in range(len(tempstring)):
                textsurface = _settings.small_font.render(tempstring[x], False, (0, 0, 0))
                if x == 4:
                    _settings.screen.blit(textsurface, ((250*(x+1)-160), _settings.highscoreHeight +(40*(y+1))))
                else:
                    _settings.screen.blit(textsurface, ((250*(x+1)-150), _settings.highscoreHeight +(40*(y+1))))
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_F4:
                    gamestate = 0
                    del _player
                    for obj in enemylist:
                        del obj

            if event.type == QUIT:
                pygame.quit()
        
        pygame.display.update()
            
        
    ################ START GAME ###############
    if gamestate == 1:
        _highscore.PlayerHighscore = 0
        currenttime = 0
        lasttime = 0
        ################# Create Player ################
        _player = player.Player((100, 100), (0, 0, 250),
                                32, 2, _settings, enemylist, 250,_highscore)
        ################ Create Enemys -( POSITION X,Y - COLOR - SIZE, DELAY , PLAYER, BEHAVIOUR, PRIORITY) ##################
        enemylist.clear()
        enemylist.append(entities.Enemy(
            (1400, 200), (200, 50, 0), 50, 5, _player, entities.Enemy.Move_toTarget, 1))
        enemylist.append(entities.Enemy(
            (1100, 300), (255, 0, 0), 50, 5, _player, entities.Enemy.Move_toPlayerX, 1))
        enemylist.append(entities.Enemy(
            (800, 400), (255, 0, 0), 50, 5, _player, entities.Enemy.Move_toPlayerY, 1))
        enemylist.append(entities.Enemy(
            (600, 500), (180, 0, 0), 50, 5, _player, entities.Enemy.MoveRandomDirection, 1))
        enemylist.append(entities.Enemy(
            (500, 600), (200, 50, 0), 50, 6, _player, entities.Enemy.MoveRandomDirection, 1))
        enemylist.append(entities.Enemy(
            (400, 700), (180, 0, 0), 50, 6, _player, entities.Enemy.Move_toTarget, 1))
        enemylist.append(entities.Enemy(
            (300, 800), (255, 0, 0), 50, 6, _player, entities.Enemy.Move_toPlayerX, 1))
        enemylist.append(entities.Enemy(
            (200, 900), (255, 0, 0), 50, 6, _player, entities.Enemy.Move_toPlayerY, 1))
        gamestate = 2
    ############################ Game Running ############################## 
    if gamestate == 2:
        if _player.Ability == True:
            _settings.screen.fill((0, 0, 100))
        else:
            _settings.screen.fill((70, 70, 70))
        ##################### TIME UPDATE #########################
        clock.tick()
        currenttime += clock.get_rawtime()
        totaltime += clock.get_rawtime()
        ##################### Spawn Enemy after  ##########
        # print(currenttime)
        if currenttime >= difficult:
            difficult -=100
            if difficult <=0:
                difficult = 100
            enemylist.append(entities.Enemy((0, 0), (random.randint(0, 255), random.randint(
                0, 255), 0), random.randint(25, 100), random.randint(5, 10), _player, entities.Enemy.Move_toTarget, 0))
            currenttime = 0
            random.seed(23)
            print("Enemy - Spawned by seed ",random.random())
        ##################### CHECK COLLISION #####################
        for obj in enemylist:
            if (pygame.Rect.colliderect(pygame.Rect(_player.playerPos.x, _player.playerPos.y, _player.size, _player.size), pygame.Rect(obj.EnemyPos.x, obj.EnemyPos.y, obj.size, obj.size))):
                
                obj.tick(clock.get_time(),_player.Ability)
                gamestate = 3
                print(" Game Over")
                
                ####### Save only under 5 pause ######
                if _highscore.pausedUsed<=5:
                    print ("highscore saved")
                    _highscore.save(_settings.PlayerName,  math.floor(_highscore.PlayerHighscore/1000), _settings.Gameversion, totaltime)
                    
                else:
                    textsurface = _settings.tall_font.render(" Highscore will not saved because too many Pausedtimes", False, (255, 255, 255))
                    _settings.screen.blit(textsurface, (_settings.width/2-250, _settings.height/2-40))
        
            else:
############################# ABILITY CHECK #############################
                
                obj.tick(clock.get_time(),_player.Ability)
        _player.tick(clock.get_time())

        for event in pygame.event.get():
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    gamestate=4
                    _highscore.pausedUsed +=1
            if event.type == QUIT:
                gamestate = 3
        
        ############ UI UPDATE ####################
        
        
        textsurface = _settings.small_font.render(" HIGHSCORE: " +
                                     str(math.floor(_highscore.PlayerHighscore/1000)) + _player.ability_string(), False, (255, 255, 255))
        _settings.screen.blit(textsurface, (0, 0))
        pygame.display.update()
############################## PAUSE MENU ##########################
    if gamestate == 4:
        for event in pygame.event.get():
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    gamestate=2
            if event.type == QUIT:
                gamestate = 3
        textsurface = _settings.tall_font.render(" Paused ", False, (255, 255, 255))
        _settings.screen.blit(textsurface, (_settings.width/2-100, _settings.height/2-40))
        pygame.display.update()
    