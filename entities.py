import pygame
import settings
import random


class Enemy():
    def __init__(self, EnemyPos, color, size, delay, _player, behaviour, priority):
        self.player = _player
        self.color = color
        self.size = size
        self.delay = delay
        self.Counter = 0
        self.direction = 0
        self.NOTFINISHED = True
        self.moveTorwardSteps = 1
        self.mergCounter=0
        self.Move = behaviour
        self.priority = priority
        self.wayPoint = 0
        self.target = pygame.Vector2(random.randint(0, self.player.settings.width),random.randint(0, self.player.settings.height))
        if EnemyPos[0] == 0 and EnemyPos[1] == 0:
            self.NewPosition()
        else:
            self.EnemyPos = pygame.Vector2(EnemyPos[0], EnemyPos[1])

    def NewPosition(self):
        while self.NOTFINISHED:
                self.NOTFINISHED = False
                self.EnemyPos = pygame.Vector2(random.randint(0, self.player.settings.width), random.randint(0, self.player.settings.height))
                #print("get random Position")
                for _miniEnemy in self.player.EnemyList:
                    if self != _miniEnemy:
                        if (pygame.Rect.colliderect(pygame.Rect(self.EnemyPos.x, self.EnemyPos.y, self.size, self.size), pygame.Rect(_miniEnemy.EnemyPos.x, _miniEnemy.EnemyPos.y, _miniEnemy.size, _miniEnemy.size))):
                            self.NOTFINISHED = True
                        elif(pygame.Rect.colliderect(pygame.Rect(self.EnemyPos.x, self.EnemyPos.y, self.size, self.size), pygame.Rect(self.player.playerPos.x, self.player.playerPos.y, self.player.SpawnRadius, self.player.SpawnRadius))):
                            self.NOTFINISHED = True
                if self.NOTFINISHED:
                    print("not finished false")
                    
######################  GIVE NEW RANDOM TARGET WITH RANGE ###########################
    def NewTarget(self, xrange,yrange):
        self.target = pygame.Vector2(random.randint(0+ xrange, self.player.settings.width- xrange),random.randint(0+yrange, self.player.settings.height-yrange))

###################### COLLISION WITH DIRECTION AND RUN TO THE BORDER ###############
    def CollisionEffect(self, direction, softcollision):
        if direction == 1:
            self.EnemyPos.x -=8
            if softcollision == 0:
                self.target.x =0

        if direction == 2:
            self.EnemyPos.y -=8
            if softcollision == 0:
                self.target.y =0

        if direction == 3:
            self.EnemyPos.x +=8
            if softcollision == 0:
                self.target.x =self.player.settings.width

        if direction == 4:
            self.EnemyPos.y +=8
            if softcollision == 0:
                self.target.y =self.player.settings.height

#########################   BEHAVIOUR  ENEMY THAT FOLLOW ON THE X AXIS ################################
    def Move_toPlayerX(self):
        self.target = self.player.playerPos
        #if X reached move Y
        if self.target.x == self.EnemyPos.x:
            if self.target.y < self.EnemyPos.y:
                self.EnemyPos.y -= 1
            else:
                self.EnemyPos.y +=1
        # move X to Player        
        else:
            if self.target.x < self.EnemyPos.x:
                self.EnemyPos.x -= 1
            else:
                self.EnemyPos.x +=1
        
        
        
#########################   BEHAVIOUR  ENEMY THAT FOLLOW ON THE Y AXIS ################################
    def Move_toPlayerY(self):
        self.target = self.player.playerPos
        #if Y reached move X
        if self.target.y == self.EnemyPos.y:
            if self.target.x < self.EnemyPos.x:
                self.EnemyPos.x -= 1
            else:
                self.EnemyPos.x +=1
        # move Y to Player        
        else:
            if self.target.y < self.EnemyPos.y:
                self.EnemyPos.y -= 1
            else:
                self.EnemyPos.y +=1
        
        
#########################   BEHAVIOUR  ENEMY THAT MOVE IN A RANDOM CORNER ################################
    def Move_Corners(self):
        if self.target == self.EnemyPos:
            # get new Corner pos
            rnd = random.randint(0,3)    #which corner
            if rnd == 3:# ##### 3 corner 1050,1400      750,1000 
                self.target = pygame.Vector2((random.randint(self.player.settings.width/4*3,self.player.settings.width),random.randint(self.player.settings.height/4*3, self.player.settings.height)))
            if rnd == 2:# ###  2 corner  0,350          750,1000
                self.target = pygame.Vector2((random.randint(0,self.player.settings.width/4),random.randint(self.player.settings.height/4*3, self.player.settings.height)))
            if rnd == 1:# ###  1 corner  1050,1400      0,250
                self.target = pygame.Vector2((random.randint(self.player.settings.width/4*3,self.player.settings.width),random.randint(0, self.player.settings.height/4)))
            if rnd == 0:#####  0 Corner  0,350          0,250
                self.target = pygame.Vector2((random.randint(0,self.player.settings.width/4),random.randint(0, self.player.settings.height/4)))
            print(self.target)
        # move to Point
        self.Move_toTarget()

#########################   BEHAVIOUR  ENEMY THAT MOVE ALONG THE BORDERS ################################
    def Move_Borders(self):
        if self.target == self.EnemyPos:
            # get new Corner pos
            rnd = random.randint(0,7)    #which border and which way
            rnd_offset= random.randint(0,20) # offset for more dynamic movement
            if rnd == 0:# ##### 1 Border 0-20,1000 
                if self.wayPoint == 0: 
                    self.target = pygame.Vector2((random.randint(0,rnd_offset),random.randint(self.player.settings.height-rnd_offset, self.player.settings.height)))
                    self.wayPoint = 1
                else:
                    self.target = pygame.Vector2(self.target.x, 0)  
                    self.wayPoint = 0  
            if rnd == 1:# ###  2 border  0,350          750,1000
                self.target = pygame.Vector2((random.randint(0,self.player.settings.width/4),random.randint(self.player.settings.height/4*3, self.player.settings.height)))
            if rnd == 2:# ###  1 border 1050,1400      0,250
                self.target = pygame.Vector2((random.randint(self.player.settings.width/4*3,self.player.settings.width),random.randint(0, self.player.settings.height/4)))
            if rnd == 3:#####  0 border  0,350          0,250
                self.target = pygame.Vector2((random.randint(0,self.player.settings.width/4),random.randint(0, self.player.settings.height/4)))
            if rnd == 4:# ##### 3 border 1050,1400      750,1000 
                self.target = pygame.Vector2((random.randint(self.player.settings.width/4*3,self.player.settings.width),random.randint(self.player.settings.height/4*3, self.player.settings.height)))
            if rnd == 5:# ###  2 border  0,350          750,1000
                self.target = pygame.Vector2((random.randint(0,self.player.settings.width/4),random.randint(self.player.settings.height/4*3, self.player.settings.height)))
            if rnd == 6:# ###  1 border 1050,1400      0,250
                self.target = pygame.Vector2((random.randint(self.player.settings.width/4*3,self.player.settings.width),random.randint(0, self.player.settings.height/4)))
            if rnd == 7:#####  0 border  0,350          0,250
                self.target = pygame.Vector2((random.randint(0,self.player.settings.width/4),random.randint(0, self.player.settings.height/4)))
            print(self.target)
        # move to Point
        self.Move_toTarget()

###################### approximation update #######################
    def Move_toTarget(self):
        #if target is reached get new random Target
        if self.target == self.EnemyPos and self.priority ==0:
            self.NewTarget(0,0)
        if self.target.x != self.EnemyPos.x:
            if self.target.x < self.EnemyPos.x:
                self.EnemyPos.x -= 1
            else:
                self.EnemyPos.x +=1

        if self.target.y != self.EnemyPos.y:
            if self.target.y < self.EnemyPos.y:
                self.EnemyPos.y -= 1
            else:
                self.EnemyPos.y +=1
        
 ######################### COLLISION WITH OTHER ENEMYS ################################
    def Collision(self):
       
        for _miniEnemy in self.player.EnemyList:
            if self != _miniEnemy:
                
                if (pygame.Rect.colliderect(pygame.Rect(self.EnemyPos.x, self.EnemyPos.y, self.size, self.size), pygame.Rect(_miniEnemy.EnemyPos.x, _miniEnemy.EnemyPos.y, _miniEnemy.size, _miniEnemy.size))):
                    if self.priority == 0 and _miniEnemy.priority == 0:
                        direction = 0
                        direction2 = 0
                        self.mergCounter +=1
                        #print ("eating ++ ", self.mergCounter)
                        if self.mergCounter >=5:
                            self.mergCounter =0
                            self.size += _miniEnemy.size
                            self.player.EnemyList.remove(_miniEnemy)
                            del _miniEnemy
                        else:
                            if self.EnemyPos.x <= _miniEnemy.EnemyPos.x:
                                direction = 1
                                direction2 = 3
                                self.CollisionEffect(direction,0)
                                _miniEnemy.CollisionEffect(direction2,0)
                            elif self.EnemyPos.y <= _miniEnemy.EnemyPos.y:
                                direction = 2
                                direction2 = 4
                                self.CollisionEffect(direction,0)
                                _miniEnemy.CollisionEffect(direction2,0)
                    else:
                        ##### SOFT COLLISION ########
                        if self.EnemyPos.x <= _miniEnemy.EnemyPos.x:
                            direction = 1
                            direction2 = 3
                            self.CollisionEffect(direction,1)
                            _miniEnemy.CollisionEffect(direction2,1)
                        elif self.EnemyPos.y <= _miniEnemy.EnemyPos.y:
                            direction = 2
                            direction2 = 4
                            self.CollisionEffect(direction,1)
                            _miniEnemy.CollisionEffect(direction2,1)
                
                        

            
## SPAWN 
    def EnemyDraw(self):
        pygame.draw.rect(self.player.screen, self.color, (self.EnemyPos.x,
                                                          self.EnemyPos.y, self.size, self.size))

#########################    DELAY, DRAW AND DEFINE BEHAVIOUR ################################
    def tick(self, _clocktime):
        self.Counter += _clocktime
        self.EnemyDraw()

        if (self.Counter >= self.delay):
            self.Counter = 0
            self.Collision()
            self.Move(self)

