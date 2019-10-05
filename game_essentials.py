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

    # Pressing... keys
    pressing = {'up': False, 'down': False, 'left': False, 'right': False, 'a': False, 'w': False, 's': False,
                'd': False}

    # timer for animation
    clock = 0
    timer = False

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

        # game bounds
        if self.camera_x1 > 250 - 32:
            self.camera_x1 = 250 - 32
        if self.camera_y1 > 250:
            self.camera_y1 = 250

        if self.camera_x2 > 250 - 32:
            self.camera_x2 = 250 - 32
        if self.camera_y2 > 250:
            self.camera_y2 = 250

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

        # check if key is pressed
        if pressed:
            self.pressing[name] = True

            if name == p_specs['U']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['L']], self.pressing[p_specs['R']]]:
                    camera_y += 3
                else:
                    camera_y += 4

            elif name == p_specs['D']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['L']], self.pressing[p_specs['R']]]:
                    camera_y -= 3
                else:
                    camera_y -= 4

            elif name == p_specs['L']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['U']], self.pressing[p_specs['D']]]:
                    camera_x += 3
                else:
                    camera_x += 4

            elif name == p_specs['R']:
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing[p_specs['U']], self.pressing[p_specs['D']]]:
                    camera_x -= 3
                else:
                    camera_x -= 4
        else:
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
