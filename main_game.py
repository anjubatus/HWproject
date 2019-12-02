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
            if game.switch['player_1'] is not None:
                player_1.char = player_objs[game.switch['player_1']]
            if game.switch['player_2'] is not None:
                player_2.char = player_objs[game.switch['player_2']]
            # print player_1.on_tile, player_1.collision.topleft
            # for x in Enemy.all_enemies.values():
            #   print x.placement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print Maps.all_maps.keys()

    if game.switch['cur_mode'] == 'gameplay':   # Game mode is play
        # MOVEMENT
        pressed = pygame.key.get_pressed()

        # sprint
        if pressed[pygame.K_v]:  # player 1 uses sprint key
            if player_1.sprint > 0:
                player_1.sprint_in_use = True
                if game.timer:
                    player_1.sprint -= 1
                if player_1.sprint == 0:
                    player_1.sprint = -5
            else:
                player_1.sprint_in_use = False
        else:
            player_1.sprint_in_use = False

        if pressed[pygame.K_m]:  # player 2 uses sprint key
            if player_2.sprint > 0:
                player_2.sprint_in_use = True
                if game.timer:
                    player_2.sprint -= 1
                if player_2.sprint == 0:
                    player_2.sprint = -5
            else:
                player_2.sprint_in_use = False
        else:
            player_2.sprint_in_use = False

        # player 1 - walk
        game.move_press(pressed[pygame.K_w], 'w', player_1.speed)
        game.move_press(pressed[pygame.K_s], 's', player_1.speed)
        game.move_press(pressed[pygame.K_a], 'a', player_1.speed)
        game.move_press(pressed[pygame.K_d], 'd', player_1.speed)

        # player 2 - walk
        game.move_press(pressed[pygame.K_UP], 'up', player_2.speed, camera=2)
        game.move_press(pressed[pygame.K_DOWN], 'down', player_2.speed, camera=2)
        game.move_press(pressed[pygame.K_LEFT], 'left', player_2.speed, camera=2)
        game.move_press(pressed[pygame.K_RIGHT], 'right', player_2.speed, camera=2)

        # UPDATE GAME
        game.update_game()

        # enemies
        for x in maps.all_maps[game.cur_map][2].values():
            x.update('players')

        # hard objects
        for x in maps.all_maps[game.cur_map][3].values():
            x.update()

        maps.map_update()
        player_1.update()
        player_2.update()

        # D R A W
        # map
        # left screen
        game.map_screen1.blit(maps.all_maps[game.cur_map][0], (game.camera_x1, game.camera_y1))

        # right screen
        game.map_screen2.blit(maps.all_maps[game.cur_map][0], (game.camera_x2, game.camera_y2))

        # hard objects
        for x in maps.all_maps[game.cur_map][3].values():
            x.draw()

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

        # enemies
        for x in maps.all_maps[game.cur_map][2].values():
            x.draw()

        # layer 2
        game.map_screen1.blit(maps.second_layer[game.cur_map], (game.camera_x1, game.camera_y1))
        game.map_screen2.blit(maps.second_layer[game.cur_map], (game.camera_x2, game.camera_y2))

        # frames and shade
        game.map_screen1.blit(sprites.big_sprites['shade0'], (0, 0))
        game.map_screen2.blit(sprites.big_sprites['shade0'], (0, 0))
        game.map_screen1.blit(sprites.big_sprites['frame0'], (0, 0))
        game.map_screen2.blit(sprites.big_sprites['frame1'], (0, 0))

        # health bars - first draw black background, then the actual health bar
        player_1.draw_bars()
        player_2.draw_bars()

        # blit on big screen
        screen.blit(game.map_screen1, (0, 0))
        screen.blit(game.map_screen2, (500, 0))

    elif game.switch['cur_mode'] == 'menu':
        if game.switch['menu'] == 'main menu':
            title_screen.main_menu('this is text', 'This is header 1', 'This is header 2')
            game.switch['play_mode'], game.switch['player_1'], game.switch['player_2'] = None, None, None
        elif game.switch['menu'] == 'switch menu':
            title_screen.switch_menu()

    # Last updates
    game.last_update()

    # END FRAME
    clock.tick(30)

    pygame.display.update()
