import pygame
WIDTH = 352
HEIGHT = 192


FPS = 120
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ACCELERATION = 0.4

#groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
flag = pygame.sprite.Group()
jump = pygame.sprite.Group()
