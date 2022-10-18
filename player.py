
import pygame
import settings
import math

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    K_RETURN,
    K_F4,
    QUIT
)


class Player():

    def __init__(self, startposition, color, size, delay, settings, enemylist, spawnRadius, highscore):
        self.screen = settings.screen
        self.settings = settings
        self.color = color
        self.size = size
        self.delay = delay
        self.playerMoveCounter = 0
        self.counter = 0
        self.playerPos = pygame.Vector2(startposition[0], startposition[1])
        self.EnemyList = enemylist
        self.SpawnRadius = spawnRadius
        self.Ability = False
        self.Ability_activationTime = 600
        self.Ability_counter = 0
        self.Ability_costs = 0.90  # 10%
        self.highscore = highscore
        self.abilitytext = ""

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
        if keys[K_SPACE]:
            if self.Ability == False and self.Ability_counter == -1:
                self.Ability = True
                self.Ability_counter = 0
                self.highscore.PlayerHighscore = math.floor(
                    self.highscore.PlayerHighscore * self.Ability_costs)
####################  tick every 0.0001 s #####################

    def tick(self, _clocktime):
        self.playerMoveCounter += _clocktime
        self.player_draw()

        if self.playerMoveCounter >= self.delay:
            ###################### Update Highscore ##################
            if self.Ability == False:
                self.highscore.PlayerHighscore += len(self.EnemyList)

            ###################### ABILITY CHECK #####################
            if self.Ability == True:
                self.Ability_counter += 1
                if self.Ability_counter >= self.Ability_activationTime:
                    self.Ability = False
            elif self.Ability_counter <= 1000 and self.Ability_counter > 0:  #### 1000 cooldown
                self.Ability_counter += 1
            else:
                self.Ability_counter = -1

        ######################  MOVE and counter set 0 ############
            self.playerMoveCounter = 0
            self.move()

################  DRAW PLAYER ####################
    def player_draw(self):
        pygame.draw.rect(self.screen, self.color, (self.playerPos.x,
                                                   self.playerPos.y, self.size, self.size))
    def ability_string(self):
        if self.Ability:
            self.abilitytext = " FREEZE ACTIVATED"
        elif not self.Ability and self.Ability_counter >=1:
            self.abilitytext = "COOLDOWN: {0}".format((1000 - self.Ability_counter)/100)
            
        else:
            self.abilitytext = " Freeze Ready -  press SPACE  - Costs: 10% Highscore"
        return self.abilitytext