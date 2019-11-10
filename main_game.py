from objects import *
from maps import *
from menus import *
import sys

# HALLOWEEN BASED 2D GAME

# initialize
pygame.init()
clock = pygame.time.Clock()


# base map
maps.new_map(0, 'right')
maps.current_map(0)
# print maps.cur_size


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
            print player_1.on_tile, player_1.collision.topleft
            # for x in Enemy.all_enemies.values():
            #   print x.placement

    if game.switch['cur_mode'] == 'gameplay':   # Game mode is play
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
        player_1.update()
        player_2.update()
        maps.map_update()

        # D R A W
        # map
        # left screen
        game.map_screen1.blit(maps.all_maps[game.cur_map][0], (game.camera_x1, game.camera_y1))
        game.map_screen1.blit(maps.second_layer[game.cur_map], (game.camera_x1, game.camera_y1))

        # right screen
        game.map_screen2.blit(maps.all_maps[game.cur_map][0], (game.camera_x2, game.camera_y2))
        game.map_screen2.blit(maps.second_layer[game.cur_map], (game.camera_x2, game.camera_y2))

        # ENEMIES
        for x in maps.all_maps[game.cur_map][2].values():
            x.update('players')

        # HARD OBJECTS
        for x in maps.all_maps[game.cur_map][3].values():
            x.update()

        # PLAYERS

        # left screen
        # player in front of friend;
        p1 = player_1.char.cur_sprite
        p2 = player_2.char.cur_sprite
        if game.camera_y1 <= game.camera_y2:
            game.map_screen1.blit(p2,  # friend sprite
                                  (game.camera_x1 - game.camera_x2 + (250 - sprites.new_size/2),
                                   game.camera_y1 - game.camera_y2 + (250 - sprites.new_size/2)))
            game.map_screen1.blit(p1,  # own sprite
                                  (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
        else:
            game.map_screen1.blit(p1,  # own sprite
                                  (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
            game.map_screen1.blit(p2,  # friend sprite
                                  (game.camera_x1 - game.camera_x2 + (250 - sprites.new_size / 2),
                                   game.camera_y1 - game.camera_y2 + (250 - sprites.new_size / 2)))

        # right screen
        if game.camera_y2 <= game.camera_y1:
            game.map_screen2.blit(p1,  # friend sprite
                                  (game.camera_x2 - game.camera_x1 + (250 - sprites.new_size / 2),
                                   game.camera_y2 - game.camera_y1 + (250 - sprites.new_size / 2)))
            game.map_screen2.blit(p2,  # own sprite
                                  (250-sprites.new_size/2, 250-sprites.new_size/2))
        else:
            game.map_screen2.blit(p2,  # own sprite
                                  (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
            game.map_screen2.blit(p1,  # friend sprite
                                  (game.camera_x2 - game.camera_x1 + (250 - sprites.new_size / 2),
                                   game.camera_y2 - game.camera_y1 + (250 - sprites.new_size / 2)))

        # blit on big screen
        screen.blit(game.map_screen1, (0, 0))
        screen.blit(game.map_screen2, (500, 0))

    elif game.switch['cur_mode'] == 'title screen':
        title_screen.on_use('this is text', 'This is header 1', 'This is header 2',
                            [['gameplay', (50, 250)]])

    # Last updates
    game.last_update()

    # END FRAME
    clock.tick(30)

    pygame.display.update()
