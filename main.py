import pygame
import pytmx
import random
from sprites import *
from settings import *
from tilemap import*
from itertools import *

def changeMap(maps, mapcounter):
    map = maps[mapcounter]
    all_sprites.empty()
    obstacles.empty()
    enemies.empty()
    flag.empty()
    jump.empty()
    for tile_object in map.tmxdata.objects:
        if tile_object.name == 'player':
                player = Player(tile_object.x, tile_object.y,16,24)
        if tile_object.name == 'wall':
                ob = Obstacle(tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
        if tile_object.name == 'enemy':
                e = Enemy(tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height,player)
                all_sprites.add(e)

        if tile_object.name == 'flag':
                fl = Flag(tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
        if tile_object.name == 'jump':
                ju = JumpBox(tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
        return map


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Just Don't Touch Red" )
clock = pygame.time.Clock()

#bg_img = pygame.image.load("bg.png")
#bg_rect = bg_img.get_rect()

start = pygame.image.load("startscreen.png")
start_rect = start.get_rect()

winner = pygame.image.load("winner.png")
winner_rect = winner.get_rect()

loser = pygame.image.load("endscreen.png")
loser_rect = loser.get_rect()

maps = []
one = TiledMap("maps/2.tmx")
two = TiledMap("maps/3.tmx")
three = TiledMap("maps/1.tmx")
four = TiledMap("maps/4.tmx")

maps.append(one)
maps.append(two)
maps.append(three)
maps.append(four)


#create player sprite and add it to group
player = Player(WIDTH/2,HEIGHT/2,16,32)
map = maps[0]
for tile_object in map.tmxdata.objects:
    if tile_object.name == 'player':
            player = Player(tile_object.x, tile_object.y,16,24)
    if tile_object.name == 'wall':
            ob = Obstacle(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height)
    if tile_object.name == 'enemy':
            e = Enemy(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height,player)
            all_sprites.add(e)

    if tile_object.name == 'flag':
            fl = Flag(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height)
    if tile_object.name == 'jump':
            ju = JumpBox(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height)



all_sprites.add(player)

score = 0
camera = Camera(WIDTH*4,HEIGHT)
running = True

mapcounter = 0
mapchange = False
pressed = False
won = False
endscreen = False

while running:
    if mapcounter == len(maps):
        won = True
    else:
        map = maps[mapcounter]

    if mapchange:
        all_sprites.empty()
        obstacles.empty()
        enemies.empty()
        flag.empty()
        jump.empty()

        for tile_object in map.tmxdata.objects:
            if tile_object.name == 'player':
                    player = Player(tile_object.x, tile_object.y,16,24)
            if tile_object.name == 'wall':
                    ob = Obstacle(tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
            if tile_object.name == 'enemy':
                    e = Enemy(tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height,player)
                    all_sprites.add(e)
            if tile_object.name == 'flag':
                    fl = Flag(tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
            if tile_object.name == 'jump':
                    ju = JumpBox(tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
        mapchange = False
        all_sprites.add(player)





    map_img = map.make_map()
    map_rect = map_img.get_rect()
    #process eventsa
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            pressed = True
    #updates
    all_sprites.update()
    camera.update(player)

    #screen.blit(bg_img,bg_rect)
    screen.blit(map_img, camera.apply_rect(map_rect))

    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))

    hits = pygame.sprite.spritecollide(player,flag,False)
    if len(hits)>0:

        mapcounter+=1
        mapchange = True

    hits = pygame.sprite.spritecollide(player,jump,False)
    if len(hits)>0:
        player.jump(-20)

    hits = pygame.sprite.spritecollide(player,enemies,False)
    if len(hits)>0:
        endscreen = True

    if pressed ==False:
        screen.blit(start,start_rect)
        player.movement[0] = 0
    else:
        player.movement[0] = 4

    if won:
        screen.blit(winner,winner_rect)
        all_sprites.empty()

    if endscreen:
        screen.blit(loser,loser_rect)
        keys = pygame.key.get_pressed()
        if True in keys:
            mapchange = True
            endscreen = False
            mapcounter = 0


    clock.tick(FPS)/1000

    pygame.display.flip()

pygame.quit()
