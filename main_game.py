from objects import *
from maps import *
import sys

# HALLOWEEN BASED 2D GAME

# initialize
pygame.init()
clock = pygame.time.Clock()


# base map
maps.new_map('base')
maps.current_map('base')
print maps.cur_size


# CAMERA
game.camera_x1 = 0 - (maps.cur_size[0]*sprites.new_size/2 - (250 - sprites.new_size/2))
game.camera_y1 = 0 - ((maps.cur_size[1]-1)*sprites.new_size - (250 - sprites.new_size/2))

game.camera_x2 = 0 - (maps.cur_size[0]*sprites.new_size/2 - (250 - sprites.new_size/2))
game.camera_y2 = 0 - ((maps.cur_size[1]-1)*sprites.new_size - (250 - sprites.new_size/2))


# START GAME
while True:
    screen.fill((50, 50, 50))
    game.map_screen1.fill((50, 50, 50))
    game.map_screen2.fill((50, 50, 50))
    mouse.check_pos()

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # close game
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        # MOUSE CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.clicked = True
            print game.camera_x1, game.camera_y1

    # MOVEMENT
    pressed = pygame.key.get_pressed()

    # player 1
    game.move_press(pressed[pygame.K_w], 'w')
    game.move_press(pressed[pygame.K_s], 's')
    game.move_press(pressed[pygame.K_a], 'a')
    game.move_press(pressed[pygame.K_d], 'd')

    # player 2
    game.move_press(pressed[pygame.K_UP], 'up', camera=2)
    game.move_press(pressed[pygame.K_DOWN], 'down', camera=2)
    game.move_press(pressed[pygame.K_LEFT], 'left', camera=2)
    game.move_press(pressed[pygame.K_RIGHT], 'right', camera=2)

    # UPDATE GAME
    game.update_game()

    # D R A W
    # map
    # left screen
    game.map_screen1.blit(maps.all_maps['base'][0], (game.camera_x1, game.camera_y1))
    game.map_screen1.blit(maps.second_layer['base'], (game.camera_x1, game.camera_y1))

    # right screen
    game.map_screen2.blit(maps.all_maps['base'][0], (game.camera_x2, game.camera_y2))
    game.map_screen2.blit(maps.second_layer['base'], (game.camera_x2, game.camera_y2))

    # PLAYERS

    # left screen
    # player in front of friend;
    p1 = pig_witch
    p2 = cat_clown
    if game.camera_y1 <= game.camera_y2:
        game.map_screen1.blit(p2.cur_sprite,  # friend sprite
                              (game.camera_x1 - game.camera_x2 + (250 - sprites.new_size/2),
                               game.camera_y1 - game.camera_y2 + (250 - sprites.new_size/2)))
        game.map_screen1.blit(p1.cur_sprite,  # own sprite
                              (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
    else:
        game.map_screen1.blit(p1.cur_sprite,  # own sprite
                              (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
        game.map_screen1.blit(p2.cur_sprite,  # friend sprite
                              (game.camera_x1 - game.camera_x2 + (250 - sprites.new_size / 2),
                               game.camera_y1 - game.camera_y2 + (250 - sprites.new_size / 2)))

    # right screen
    if game.camera_y2 <= game.camera_y1:
        game.map_screen2.blit(p1.cur_sprite,  # friend sprite
                              (game.camera_x2 - game.camera_x1 + (250 - sprites.new_size / 2),
                               game.camera_y2 - game.camera_y1 + (250 - sprites.new_size / 2)))
        game.map_screen2.blit(p2.cur_sprite,  # own sprite
                              (250-sprites.new_size/2, 250-sprites.new_size/2))
    else:
        game.map_screen2.blit(p2.cur_sprite,  # own sprite
                              (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
        game.map_screen2.blit(p1.cur_sprite,  # friend sprite
                              (game.camera_x2 - game.camera_x1 + (250 - sprites.new_size / 2),
                               game.camera_y2 - game.camera_y1 + (250 - sprites.new_size / 2)))

    # ANIM. TEST...
    pig_witch.work_cycle('LEFT')
    cat_clown.work_cycle('LEFT')

    # blit on big screen
    screen.blit(game.map_screen1, (0, 0))
    screen.blit(game.map_screen2, (500, 0))

    # END FRAME
    clock.tick(30)

    pygame.display.update()
