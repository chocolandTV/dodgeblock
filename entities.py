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
        self.mergCounter=0
        self.Move = behaviour
        self.priority = priority
        self.target = pygame.Vector2(random.randint(0, self.player.settings.width),random.randint(0, self.player.settings.height))
        if EnemyPos[0] == 0 and EnemyPos[1] == 0:
            self.NewPosition()
        else:
            self.EnemyPos = pygame.Vector2(EnemyPos[0], EnemyPos[1])

    def NewPosition(self):
        while self.NOTFINISHED:
                self.NOTFINISHED = False
                self.EnemyPos = pygame.Vector2(random.randint(0, self.player.settings.width), random.randint(0, self.player.settings.height))
                
                for _miniEnemy in self.player.EnemyList:
                    if self != _miniEnemy:
                        if (pygame.Rect.colliderect(pygame.Rect(self.EnemyPos.x, self.EnemyPos.y, self.size, self.size), pygame.Rect(_miniEnemy.EnemyPos.x-(_miniEnemy.size/2), _miniEnemy.EnemyPos.y-(_miniEnemy.size/2), _miniEnemy.size, _miniEnemy.size))):
                            self.NOTFINISHED = True
                        elif(pygame.Rect.colliderect(pygame.Rect(self.EnemyPos.x, self.EnemyPos.y, self.size, self.size), pygame.Rect(self.player.playerPos.x- (self.player.SpawnRadius/2), self.player.playerPos.y- (self.player.SpawnRadius/2), self.player.SpawnRadius, self.player.SpawnRadius))):
                            self.NOTFINISHED = True
                if self.NOTFINISHED:
                    print("not finished false")
                    

###################### COLLISION WITH DIRECTION AND RUN TO THE BORDER ###############
    def CollisionEffect(self, direction):
        _rnd =random.randint(5,30)
        if direction == 1:
            self.EnemyPos.x -=_rnd
            self.target = pygame.Vector2(random.randint(0, self.player.settings.width),random.randint(0, self.player.settings.height))

            
        if direction == 2:
            self.EnemyPos.y -=_rnd
            self.target = pygame.Vector2(random.randint(0, self.player.settings.width),random.randint(0, self.player.settings.height))

            
        if direction == 3:
            self.EnemyPos.x +=_rnd
            self.target = pygame.Vector2(random.randint(0, self.player.settings.width),random.randint(0, self.player.settings.height))

            
        if direction == 4:
            self.EnemyPos.y +=_rnd
            self.target = pygame.Vector2(random.randint(0, self.player.settings.width),random.randint(0, self.player.settings.height))

            
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
        

###################### approximation update #######################
    def Move_toTarget(self):
        #if target is reached get new random Target
        if self.target == self.EnemyPos:
            random.seed(20)
            print("Enemy - MovetoTarget Behaviour seed",random.random())
            self.target = pygame.Vector2(random.randint(0, self.player.settings.width),random.randint(0, self.player.settings.height))

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
                    ############# EATING ##################
                    self.mergCounter +=1
                    if self.mergCounter >=10 and _miniEnemy.priority == 0:
                        self.mergCounter =0
                        self.size += 10
                        self.player.EnemyList.remove(_miniEnemy)
                        del _miniEnemy
                    else:
                        ############# COLLIDING ##############
                        if self.EnemyPos.x <= _miniEnemy.EnemyPos.x:
                            self.CollisionEffect(1)
                            _miniEnemy.CollisionEffect(3)
                        elif self.EnemyPos.y <= _miniEnemy.EnemyPos.y:
                            self.CollisionEffect(2)
                            _miniEnemy.CollisionEffect(4)
                    
      
## SPAWN 
    def EnemyDraw(self):
        pygame.draw.rect(self.player.screen, self.color, (self.EnemyPos.x,
                                                          self.EnemyPos.y, self.size, self.size))

#########################    DELAY, DRAW AND DEFINE BEHAVIOUR ################################
    def tick(self, _clocktime, ability):
        self.Counter += _clocktime
        self.EnemyDraw()
        if (self.Counter >= self.delay and ability == False):
            self.Counter = 0
            self.Collision()
            self.Move(self)