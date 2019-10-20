import pygame

screen_x = 1000
screen_y = 500
screen = pygame.display.set_mode((screen_x, screen_y), pygame.HWSURFACE)
pygame.display.set_caption('HALLOWEEN')


# G A M E
class Game(object):
    # cameras  (single player will use cameras 1)
    camera_x1 = 0
    camera_y1 = 0

    camera_x2 = 0
    camera_y2 = 0

    p1_move = None
    p2_move = None

    # indicates how many pixels cameras are moving currently
    camera_1_move = [0, 0]
    camera_2_move = [0, 0]

    # Pressing... keys
    pressing = {'up': False, 'down': False, 'left': False, 'right': False, 'a': False, 'w': False, 's': False,
                'd': False}

    # timer for animation
    clock = 0
    timer = False

    # maps
    all_maps = {}  # Dictionary of all saved maps, copy from maps class
    second_layer = {}  # dictionary of saved maps' second layer
    cur_map = 0
    map_size = (0, 0)

    # sprites
    sprite_size = 0

    # buttons / switches
    switch = {'cur_mode': 'title screen'}

    def __init__(self):
        self.clicked = False
        self.mode = 'two player'
        self.map_screen1 = pygame.Surface((500, 500), pygame.HWSURFACE | pygame.SRCALPHA)
        self.map_screen2 = pygame.Surface((500, 500), pygame.HWSURFACE | pygame.SRCALPHA)

    def update_game(self):
        # --- PUT ACTIONS HERE ---

        # clock & timer
        if self.clock < 6:
            self.clock += 1
            self.timer = False
        else:
            self.clock = 0
            self.timer = True

        # game bounds moved to maps_update

        # check if players are not moving
        if True not in [self.pressing['up'], self.pressing['down'], self.pressing['left'], self.pressing['right']]:
            self.p2_move = None
            self.camera_2_move = [0, 0]
        if True not in [self.pressing['a'], self.pressing['s'], self.pressing['d'], self.pressing['w']]:
            self.p1_move = None
            self.camera_1_move = [0, 0]

        # Reset needed actions to neutral state
        self.clicked = False

    def move_press(self, pressed, name, camera=1):   # name = 'up', 'down', etc
        # determine cameras
        camera_y = 0
        camera_x = 0

        if camera == 1:
            # using player specific keys
            p_specs = {'U': 'w', 'D': 's', 'L': 'a', 'R': 'd'}
        else:
            p_specs = {'U': 'up', 'D': 'down', 'L': 'left', 'R': 'right'}

        # check if key is pressed -- the player is moving around.
        if pressed:
            self.pressing[name] = True
            self.camera_1_move = [0, 0]
            self.camera_2_move = [0, 0]

            if name == p_specs['U']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['L']], self.pressing[p_specs['R']]]:
                    camera_y += 3
                    # how much camera moves:
                    if camera == 1:
                        self.camera_1_move[1] += 3
                    else:
                        self.camera_2_move[1] += 3
                else:
                    camera_y += 4
                    # how much camera moves:
                    if camera == 1:
                        self.camera_1_move[1] += 4
                    else:
                        self.camera_2_move[1] += 4

                # set player movement to up direction
                if camera == 1:
                    self.p1_move = 'UP'
                else:
                    self.p2_move = 'UP'

            elif name == p_specs['D']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['L']], self.pressing[p_specs['R']]]:
                    camera_y -= 3
                    if camera == 1:
                        self.camera_1_move[1] -= 3
                    else:
                        self.camera_2_move[1] -= 3
                else:
                    camera_y -= 4
                    if camera == 1:
                        self.camera_1_move[1] -= 4
                    else:
                        self.camera_2_move[1] -= 4

                # set player movement to up direction
                if camera == 1:
                    self.p1_move = 'DOWN'
                else:
                    self.p2_move = 'DOWN'

            elif name == p_specs['L']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['U']], self.pressing[p_specs['D']]]:
                    camera_x += 3
                    if camera == 1:
                        self.camera_1_move[0] += 3
                    else:
                        self.camera_2_move[0] += 3
                else:
                    camera_x += 4
                    if camera == 1:
                        self.camera_1_move[0] += 4
                    else:
                        self.camera_2_move[0] += 4

                # set player movement to up direction
                if camera == 1:
                    self.p1_move = 'LEFT'
                else:
                    self.p2_move = 'LEFT'

            elif name == p_specs['R']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['U']], self.pressing[p_specs['D']]]:
                    camera_x -= 3
                    if camera == 1:
                        self.camera_1_move[0] -= 3
                    else:
                        self.camera_2_move[0] -= 3
                else:
                    camera_x -= 4
                    if camera == 1:
                        self.camera_1_move[0] -= 4
                    else:
                        self.camera_2_move[0] -= 4

                # set player movement to up direction
                if camera == 1:
                    self.p1_move = 'RIGHT'
                else:
                    self.p2_move = 'RIGHT'
        else:
            # The player isn't moving in that direction.
            self.pressing[name] = False

        if camera == 1:
            self.camera_x1 += camera_x
            self.camera_y1 += camera_y
        else:
            self.camera_x2 += camera_x
            self.camera_y2 += camera_y


# M O U S E
class Mouse(object):
    used_screen = screen

    def __init__(self):
        self.pos = (0, 0)

    def check_pos(self):
        self.pos = pygame.mouse.get_pos()


game = Game()
mouse = Mouse()
# cameras are set in maps - new_map
