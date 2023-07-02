import pygame , sys

from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("Platformer")

window = (600,400)

screen = pygame.display.set_mode(window,0,32)


display = pygame.Surface((300,200))

player_image = pygame.image.load("player.png")

true_scroll = [0,0]

player_image.set_colorkey((255,255,255))

grass = pygame.image.load("grass.png")

Tile_size = grass.get_width()

dirt = pygame.image.load("dirt.png")

def load_map(path):

    f = open(path + ".txt" , "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map("map")

def collision_test(rect,tiles):
    collision = []
    for tile in tiles:
        if rect.colliderect(tile):
            collision.append(tile)
    return collision

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False

moving_left = False

player_y_momentum = 0

air_timer = 0

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())

scroll = [0,0]
while True: # game loop
    display.fill((146,244,255))

    true_scroll[0] += (player_rect.x - true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y - true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt, (x * Tile_size - scroll[0], y * Tile_size - scroll[1]))
            if tile == '2':
                display.blit(grass, (x * Tile_size- scroll[0] , y * Tile_size - scroll[1]))
                
            if tile != '0':  
                tile_rects.append(pygame.Rect(x * Tile_size, y * Tile_size , Tile_size, Tile_size))
            x += 1
        y += 1
    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_image, (player_rect.x-scroll[0], player_rect.y-scroll[1]))

    for event in pygame.event.get(): 

        if event.type == QUIT: 

            pygame.quit() 

            sys.exit() 

        if event.type == KEYDOWN:

            if event.key == K_RIGHT:

                moving_right = True

            if event.key == K_LEFT:

                moving_left = True

            if event.key == K_UP:

                if air_timer < 6:

                    player_y_momentum = -5

        if event.type == KEYUP:

            if event.key == K_RIGHT:

                moving_right = False

            if event.key == K_LEFT:

                moving_left = False

    surf = pygame.transform.scale(display,window)

    screen.blit(surf, (0, 0))

    pygame.display.update() 

    clock.tick(60) 