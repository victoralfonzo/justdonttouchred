import pygame
import pygame
from settings import *
from tilemap import *

clock = pygame.time.Clock()
dt = clock.tick(FPS)/1000

def collision_test(rect,tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions

class Player(pygame.sprite.Sprite):
    #sprite for Player

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.size = self.width, self.height = (width,height)
        self.image = pygame.Surface((width,height))
        self.image.fill(WHITE)
        #looks at image, copies rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.movement = [0,0]
        self.jumping = False
        self.ymomentum = 0
        self.airtimer = 0
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}
        self.movement[0] = 4

    def update(self):
        self.movement[1] = 0
        self.movement[1] +=self.ymomentum
        self.ymomentum+= 1.4
    #    self.movement[0]+= self.rect.x * (1/500)
        if self.ymomentum > 20:
            self.ymomentum = 20
        self.keys()
        self.move()

    def move(self): # movement = [5,2]
        self.collision_types['top'] = False
        self.collision_types['left'] = False
        self.collision_types['bottom'] = False
        self.collision_types['right'] = False

        self.rect.x += self.movement[0]
        collisions = collision_test(self.rect,obstacles)
        for tile in collisions:

            if self.movement[0] > 0:
                self.collision_types['right'] = True
                self.rect.right = tile.rect.left

            if self.movement[0] < 0:
                self.rect.left = tile.rect.right
                self.collision_types['left'] = True


        self.rect.y += self.movement[1]
        collisions = collision_test(self.rect,obstacles)
        for tile in collisions:
            if self.movement[1] > 0:
                self.collision_types['bottom'] = True
                self.rect.bottom = tile.rect.top
                self.ymomentum =0
                self.airtimer = 0
            if self.movement[1] < 0:
                self.rect.top = tile.rect.bottom
                self.collision_types['up'] = True
            self.airtimer +=1


    def jump(self,amt):
        self.ymomentum = amt

    def keys(self):
        p = self.rect.bottomleft
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.airtimer <8 and self.collision_types['bottom']==True:
                self.jump(-14)
        if keys[pygame.K_s]:
            self.image = pygame.Surface((16,16))
            self.image.fill(WHITE)
            #looks at image, copies rect
            self.rect = self.image.get_rect()
            self.rect.bottomleft = p
        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill(WHITE)
            #looks at image, copies rect
            self.rect = self.image.get_rect()
            self.rect.bottomleft = p


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height,target):
        pygame.sprite.Sprite.__init__(self,enemies)
        self.size = self.width, self.height = (width,height)
        self.image = pygame.Surface((width,height))
        self.image.fill(RED)
        #looks at image, copies rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.movement = [0,0]
        self.ymomentum = 0
        self.health = 1
        self.target = target
        self.collision_types = {'top':False,'bottom':False,'right':False,'left':False}

    def update(self):
        self.movement= [0,0]
        self.move()

    def move(self): # movement = [5,2]            self.collision_types['top'] = False
        self.collision_types['bottom'] = False

        self.rect.x += self.movement[0]
        collisions = collision_test(self.rect,obstacles)
        for tile in collisions:

            if self.movement[0] > 0:
                self.rect.right = tile.rect.left

            if self.movement[0] < 0:
                self.rect.left = tile.rect.right


        self.rect.y += self.movement[1]
        collisions = collision_test(self.rect,obstacles)
        for tile in collisions:
            if self.movement[1] > 0:
                self.collision_types['bottom'] = True
                self.rect.bottom = tile.rect.top
                self.ymomentum =0
            if self.movement[1] < 0:
                self.rect.top = tile.rect.bottom


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self,obstacles)
        self.rect = pygame.Rect(x,y,w,h)
        self.rect.x = x
        self.rect.y = y

class Flag(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self,flag,all_sprites)
        self.image = pygame.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

class JumpBox(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self,jump,all_sprites)
        self.image = pygame.Surface((w,h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
