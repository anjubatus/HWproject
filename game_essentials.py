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
    pressing = {'up': False, 'down': False, 'left': False, 'right': False}

    def __init__(self):
        self.clicked = False
        self.mode = 'two player'
        self.map_screen1 = pygame.Surface((500, 500), pygame.HWSURFACE | pygame.SRCALPHA)
        self.map_screen2 = pygame.Surface((500, 500), pygame.HWSURFACE | pygame.SRCALPHA)

    def update_game(self):
        # --- PUT ACTIONS HERE ---

        # Reset needed actions to neutral state
        self.clicked = False

    def move_press(self, pressed, name, camera=1):   # name = 'up', 'down', etc
        # determine cameras
        if camera == 1:
            camera_x = self.camera_x1
            camera_y = self.camera_y1
        else:
            camera_x = self.camera_x2
            camera_y = self.camera_y2

        if pressed:
            self.pressing[name] = True

            if name == 'up':
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing['left'], self.pressing['right']]:
                    self.camera_y += 3
                else:
                    self.camera_y += 4

            elif name == 'down':
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing['left'], self.pressing['right']]:
                    self.camera_y -= 3
                else:
                    self.camera_y -= 4

            elif name == 'left':
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing['up'], self.pressing['down']]:
                    self.camera_x += 3
                else:
                    self.camera_x += 4

            elif name == 'right':
                # confirm if moving diagonally; movement should be slower in that case
                if True in [self.pressing['up'], self.pressing['down']]:
                    self.camera_x -= 3
                else:
                    self.camera_x -= 4
        else:
            self.pressing[name] = False


# M O U S E
class Mouse(object):
    used_screen = screen

    def __init__(self):
        self.pos = (0, 0)

    def check_pos(self):
        self.pos = pygame.mouse.get_pos()


game = Game()
mouse = Mouse()
