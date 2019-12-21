from scripts.maps import *
from scripts.menus import *
import sys

# HALLOWEEN BASED 2D GAME

# initialize
pygame.init()
clock = pygame.time.Clock()


# base map
maps.new_map(0, 'right')
maps.current_map(0)

# sounds
pygame.mixer.init()
pygame.mixer.music.load(game.switch['music'])
pygame.mixer.music.play(-1)


# START GAME
while True:
    screen.fill((0, 0, 0))
    game.map_screen1.fill((0, 0, 0))
    game.map_screen2.fill((0, 0, 0))
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
            if game.switch['player_1'] is not None and game.switch['cur_mode'] == 'menu':
                player_1.char = player_objs[game.switch['player_1']]
            if game.switch['player_2'] is not None and game.switch['cur_mode'] == 'menu':
                player_2.char = player_objs[game.switch['player_2']]

        if event.type == pygame.KEYDOWN:
            """if event.key == pygame.K_1:
                game.stoptime()"""
            if event.key == pygame.K_SPACE:
                if game.switch['play_mode'] == 'single' and game.player_1.ready_to_leave:
                    game.switch['gate_enter'] = True
                elif game.switch['play_mode'] == 'two' and game.player_1.ready_to_leave and\
                        game.player_2.ready_to_leave:
                    game.switch['gate_enter'] = True

    if game.switch['cur_mode'] == 'gameplay':   # Game mode is play
        # MOVEMENT
        pressed = pygame.key.get_pressed()

        if game.switch['play_mode'] == 'single':
            # S I N G L E P L A Y E R MODE
            # sprint
            if pressed[pygame.K_m]:  # player uses sprint key
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

            v = 1
            # player 1 - walk
            game.move_press(pressed[pygame.K_w], 'w', player_1.speed)
            game.move_press(pressed[pygame.K_s], 's', player_1.speed)
            game.move_press(pressed[pygame.K_a], 'a', player_1.speed)
            game.move_press(pressed[pygame.K_d], 'd', player_1.speed)

            # UPDATE GAME
            game.update_game()

            # enemies
            for x in maps.all_maps[maps.cur_name][2].values():
                x.update('players')

            # hard objects
            for x in maps.all_maps[maps.cur_name][3].values():
                x.update()

            maps.map_update()
            player_1.update()

            # D R A W
            # map
            game.map_screen1.blit(maps.all_maps[game.switch["cur_map"]][0], (game.camera_x1, game.camera_y1))

            # hard objects
            for x in maps.all_maps[game.switch["cur_map"]][3].values():
                x.draw()

            p1 = player_1.char.cur_sprite
            game.map_screen1.blit(p1, (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))

            # enemies
            for x in maps.all_maps[game.switch["cur_map"]][2].values():
                x.draw()

            # layer 2
            game.map_screen1.blit(maps.second_layer[game.switch["cur_map"]], (game.camera_x1, game.camera_y1))

            # health bars - first draw black background, then the actual health bar
            player_1.draw_bars()

            # blit on big screen
            screen.blit(game.map_screen1, (250, 0))

            # Ready for leaving
            if player_1.ready_to_leave:
                font_1.text("PRESS SPACE TO ENTER GATE", ('center', 200))

        else:
            # T W O P L A Y E R MODE

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
            for x in maps.all_maps[maps.cur_name][2].values():
                x.update('players')

            # hard objects
            for x in maps.all_maps[maps.cur_name][3].values():
                x.update()

            maps.map_update()
            player_1.update()
            player_2.update()

            # D R A W
            # map
            # left screen
            game.map_screen1.blit(maps.all_maps[game.switch["cur_map"]][0], (game.camera_x1, game.camera_y1))

            # right screen
            game.map_screen2.blit(maps.all_maps[game.switch["cur_map"]][0], (game.camera_x2, game.camera_y2))

            # hard objects
            for x in maps.all_maps[game.switch["cur_map"]][3].values():
                x.draw()

            # PLAYERS

            # left screen
            # player in front of friend;
            p1 = player_1.char.cur_sprite
            p2 = player_2.char.cur_sprite
            shade = sprites.big_sprites['shadow0']
            if game.camera_y1 <= game.camera_y2:
                game.map_screen1.blit(shade,  # friend shade
                                      (game.camera_x1 - game.camera_x2 + (250 - sprites.new_size / 2),
                                       game.camera_y1 - game.camera_y2 + (250 - sprites.new_size / 2)))
                game.map_screen1.blit(shade,  # own shade
                                      (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
                game.map_screen1.blit(p2,  # friend sprite
                                      (game.camera_x1 - game.camera_x2 + (250 - sprites.new_size/2),
                                       game.camera_y1 - game.camera_y2 + (250 - sprites.new_size/2)))
                game.map_screen1.blit(p1,  # own sprite
                                      (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
            else:
                game.map_screen1.blit(shade,  # own shade
                                      (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
                game.map_screen1.blit(shade,  # friend shade
                                      (game.camera_x1 - game.camera_x2 + (250 - sprites.new_size / 2),
                                       game.camera_y1 - game.camera_y2 + (250 - sprites.new_size / 2)))
                game.map_screen1.blit(p1,  # own sprite
                                      (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
                game.map_screen1.blit(p2,  # friend sprite
                                      (game.camera_x1 - game.camera_x2 + (250 - sprites.new_size / 2),
                                       game.camera_y1 - game.camera_y2 + (250 - sprites.new_size / 2)))

            # right screen
            if game.camera_y2 <= game.camera_y1:
                game.map_screen2.blit(shade,  # friend shade
                                      (game.camera_x2 - game.camera_x1 + (250 - sprites.new_size / 2),
                                       game.camera_y2 - game.camera_y1 + (250 - sprites.new_size / 2)))
                game.map_screen2.blit(shade,  # own shade
                                      (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
                game.map_screen2.blit(p1,  # friend sprite
                                      (game.camera_x2 - game.camera_x1 + (250 - sprites.new_size / 2),
                                       game.camera_y2 - game.camera_y1 + (250 - sprites.new_size / 2)))
                game.map_screen2.blit(p2,  # own sprite
                                      (250-sprites.new_size/2, 250-sprites.new_size/2))
            else:
                game.map_screen2.blit(shade,  # own shade
                                      (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
                game.map_screen2.blit(shade,  # friend shade
                                      (game.camera_x2 - game.camera_x1 + (250 - sprites.new_size / 2),
                                       game.camera_y2 - game.camera_y1 + (250 - sprites.new_size / 2)))
                game.map_screen2.blit(p2,  # own sprite
                                      (250 - sprites.new_size / 2, 250 - sprites.new_size / 2))
                game.map_screen2.blit(p1,  # friend sprite
                                      (game.camera_x2 - game.camera_x1 + (250 - sprites.new_size / 2),
                                       game.camera_y2 - game.camera_y1 + (250 - sprites.new_size / 2)))

            # enemies
            for x in maps.all_maps[game.switch["cur_map"]][2].values():
                x.draw()

            # layer 2
            game.map_screen1.blit(maps.second_layer[game.switch["cur_map"]], (game.camera_x1, game.camera_y1))
            game.map_screen2.blit(maps.second_layer[game.switch["cur_map"]], (game.camera_x2, game.camera_y2))

            # health bars - first draw black background, then the actual health bar
            player_1.draw_bars()
            player_2.draw_bars()

            # blit on big screen
            screen.blit(game.map_screen1, (0, 0))
            screen.blit(game.map_screen2, (500, 0))

            # Ready for leaving
            if player_1.ready_to_leave and player_2.ready_to_leave:
                font_1.text("PRESS SPACE TO ENTER GATE", ('center', 200))

        # BOTH MODES
        # draw collectibles / progress
        obj_class.draw_collected_items()

        # Pause and pause menu
        if not game.switch['pause']:
            button.draw_button((950, 20), image=sprites.images['pause'], hower=sprites.images['pause hower'],
                               stop_time=True, pause=True)
        else:
            screen.blit(sprites.images['pause bg'], (0, 0))
            button.draw_button((950, 20), image=sprites.images['play'], hower=sprites.images['play hower'],
                               stop_time=True, pause=False)
            button.draw_button(('center', 180), text='Resume', stop_time=True, pause=False)
            if game.switch['music_on']:
                button.draw_button(('center', 210), text='Quit Game', reset=True, music=Menu.music['title'])
                button.draw_button(('center', 240), text='music OFF', music=None, music_on=False)
            else:
                button.draw_button(('center', 210), text='Quit Game', reset=True)
                button.draw_button(('center', 240), text='music ON', music=Menu.music['ingame'], music_on=True)
            if game.switch['sounds_on']:
                button.draw_button(('center', 270), text='sounds OFF', sounds_on=False)
            else:
                button.draw_button(('center', 270), text='sounds ON', sounds_on=True)

    elif game.switch['cur_mode'] == 'menu':
        # M E N U MODE
        if game.switch['menu'] == 'main menu':
            title_screen.main_menu()
            game.switch['play_mode'], game.switch['player_1'], game.switch['player_2'] = None, None, None
        elif game.switch['menu'] == 'switch menu':
            title_screen.switch_menu()
        elif game.switch['menu'] == 'info screen':
            title_screen.info_screen()
        elif game.switch['menu'] == 'credits':
            title_screen.credits()
        elif game.switch['menu'] == 'story screen':
            title_screen.story_screen()
        elif game.switch['menu'] == 'death screen':
            title_screen.death_screen()
        elif game.switch['menu'] == 'win screen':
            title_screen.win_screen()

    # Last updates
    game.last_update()

    # fades
    game.fade()
    screen.blit(game.fade_screen, (0, 0))

    # END FRAME
    clock.tick(30)

    pygame.display.update()
