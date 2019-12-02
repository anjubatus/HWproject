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

    # makes it unable to move in certain direction
    no_move_1 = {'up': False, 'down': False, 'left': False, 'right': False}
    no_move_2 = {'up': False, 'down': False, 'left': False, 'right': False}

    # Pressing... keys
    pressing = {'up': False, 'down': False, 'left': False, 'right': False, 'a': False, 'w': False, 's': False,
                'd': False}

    # timer for animation
    clock = 0
    clock_2 = 0
    timer = False
    timer_2 = False

    # maps
    all_maps = {}  # Dictionary of all saved maps, copy from maps class
    second_layer = {}  # dictionary of saved maps' second layer
    cur_map = 0
    map_size = (0, 0)

    # sprites
    sprite_size = 0

    # buttons / switches
    switch = {'cur_mode': 'menu', 'play_mode': None, 'menu': 'main menu', 'player_1': None, 'player_2': None}

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

        if self.clock_2 < 3:
            self.clock_2 += 1
            self.timer_2 = False
        else:
            self.clock_2 = 0
            self.timer_2 = True

        # game bounds moved to maps_update

        # check if players are not moving
        if True not in [self.pressing['up'], self.pressing['down'], self.pressing['left'], self.pressing['right']]:
            self.p2_move = None
            self.camera_2_move = [0, 0]
        if True not in [self.pressing['a'], self.pressing['s'], self.pressing['d'], self.pressing['w']]:
            self.p1_move = None
            self.camera_1_move = [0, 0]

    def last_update(self):
        self.camera_2_move = [0, 0]
        self.camera_1_move = [0, 0]

        self.clicked = False

    def move_press(self, pressed, name, speed, camera=1):   # name = 'up', 'down', etc
        # determine cameras
        camera_y = 0
        camera_x = 0

        # diagonal speed
        diag = speed - speed/4

        if camera == 1:
            # using player specific keys
            # no_move is a dictionary that tells you if a colliding wall is in certain direction, and can't be
            # moved towards
            # no_move = self.no_move_1
            p_specs = {'U': 'w', 'D': 's', 'L': 'a', 'R': 'd'}
        else:
            # no_move = self.no_move_2
            p_specs = {'U': 'up', 'D': 'down', 'L': 'left', 'R': 'right'}

        """if True in no_move.values():
            print 'shouldn\'t move now'"""

        # check if key is pressed -- the player is moving around.
        if pressed:
            self.pressing[name] = True

            if name == p_specs['U']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['L']], self.pressing[p_specs['R']]]:
                    camera_y += 3
                    # how much camera moves:
                    if camera == 1:
                        self.camera_1_move[1] += diag
                    else:
                        self.camera_2_move[1] += diag
                else:
                    camera_y += speed
                    # how much camera moves:
                    if camera == 1:
                        self.camera_1_move[1] += speed
                    else:
                        self.camera_2_move[1] += speed

                # set player movement to up direction
                if camera == 1:
                    self.p1_move = 'UP'
                else:
                    self.p2_move = 'UP'

            elif name == p_specs['D']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['L']], self.pressing[p_specs['R']]]:
                    camera_y -= diag
                    if camera == 1:
                        self.camera_1_move[1] -= diag
                    else:
                        self.camera_2_move[1] -= diag
                else:
                    camera_y -= speed
                    if camera == 1:
                        self.camera_1_move[1] -= speed
                    else:
                        self.camera_2_move[1] -= speed

                # set player movement to up direction
                if camera == 1:
                    self.p1_move = 'DOWN'
                else:
                    self.p2_move = 'DOWN'

            elif name == p_specs['L']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['U']], self.pressing[p_specs['D']]]:
                    camera_x += diag
                    if camera == 1:
                        self.camera_1_move[0] += diag
                    else:
                        self.camera_2_move[0] += diag
                else:
                    camera_x += speed
                    if camera == 1:
                        self.camera_1_move[0] += speed
                    else:
                        self.camera_2_move[0] += speed

                # set player movement to up direction
                if camera == 1:
                    self.p1_move = 'LEFT'
                else:
                    self.p2_move = 'LEFT'

            elif name == p_specs['R']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['U']], self.pressing[p_specs['D']]]:
                    camera_x -= diag
                    if camera == 1:
                        self.camera_1_move[0] -= diag
                    else:
                        self.camera_2_move[0] -= diag
                else:
                    camera_x -= speed
                    if camera == 1:
                        self.camera_1_move[0] -= speed
                    else:
                        self.camera_2_move[0] -= speed

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
