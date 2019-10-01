from game_essentials import *
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
game.camera_y1 = 0 - (maps.cur_size[1]*sprites.new_size - (250 - sprites.new_size/2))

game.camera_x2 = 0 - (maps.cur_size[0]*sprites.new_size/2 - (250 - sprites.new_size/2))
game.camera_y2 = 0 - (maps.cur_size[1]*sprites.new_size - (250 - sprites.new_size/2))


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

    # MOVEMENT
    pressed = pygame.key.get_pressed()

    # player 2
    game.move_press(pressed[pygame.K_UP], 'up')
    game.move_press(pressed[pygame.K_DOWN], 'down')
    game.move_press(pressed[pygame.K_LEFT], 'left')
    game.move_press(pressed[pygame.K_RIGHT], 'right')

    # UPDATE GAME
    game.update_game()

    # DRAW
    # map
    game.map_screen1.blit(maps.all_maps['base'][0], (game.camera_x1, game.camera_y1))
    game.map_screen2.blit(maps.all_maps['base'][0], (game.camera_x2, game.camera_y2))

    screen.blit(game.map_screen1, (0, 0))
    screen.blit(game.map_screen2, (500, 0))

    # players
    screen.blit(sprites.big_sprites['playerSPR0'], (250-sprites.new_size/2, 250-sprites.new_size/2))
    screen.blit(sprites.big_sprites['playerSPR1'], (250-sprites.new_size/2+500, 250-sprites.new_size/2))

    # END FRAME
    clock.tick(30)

    pygame.display.update()
