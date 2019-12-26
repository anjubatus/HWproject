import pygame

screen_x = 1000
screen_y = 500
screen = pygame.display.set_mode((screen_x, screen_y), pygame.HWSURFACE)
pygame.display.set_caption('Cranberry Woodlands')
pygame.init()


# G A M E
class Game(object):
    # How many keys players have found. once all three are True, players can go through the gate
    keys = {1: False, 2: False, 3: False}
    keys_total = 0

    p1_dead = False
    p2_dead = False

    # cameras  (single player will use cameras 1)
    camera_x1 = 0
    camera_y1 = 0

    camera_x2 = 0
    camera_y2 = 0

    start = {}

    p1_move = None
    p2_move = None

    # sounds
    sounds = {'select': pygame.mixer.Sound('sounds/select1.wav'), 'key': pygame.mixer.Sound('sounds/bling.wav'),
              'item': pygame.mixer.Sound('sounds/blip.wav'), 'quit': pygame.mixer.Sound('sounds/quit.wav'),
              'death': pygame.mixer.Sound('sounds/death.wav'), 'win': pygame.mixer.Sound('sounds/win.wav'),
              'damage': pygame.mixer.Sound('sounds/auch.wav'), 'exit': pygame.mixer.Sound('sounds/exit.wav'),
              'notice': pygame.mixer.Sound('sounds/jump.wav'), 'defense': pygame.mixer.Sound('sounds/defense.wav'),
              'grunt': pygame.mixer.Sound('sounds/grunt.wav'), 'grunt2': pygame.mixer.Sound('sounds/grunt2.wav'),
              'owl': pygame.mixer.Sound('sounds/owl.wav'), 'wind': pygame.mixer.Sound('sounds/wind.wav'),
              'crickets': pygame.mixer.Sound('sounds/crickets.wav'), 'squeak': pygame.mixer.Sound('sounds/squeak.wav')}

    for x in sounds.values():  # set volume lower
        x.set_volume(0.5)
    sounds['win'].set_volume(0.3)
    sounds['exit'].set_volume(0.3)
    sounds['key'].set_volume(0.3)
    sounds['owl'].set_volume(0.7)

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
    stop_time = False

    # fade ins and outs, flashes
    fade_in = False
    fade_out = False
    fade_level = 0
    fade_screen = pygame.Surface((1000, 500), pygame.SRCALPHA)

    flash_in = False
    flash_out = False
    flash_level = 0
    flash_screen = pygame.Surface((1000, 500), pygame.SRCALPHA)

    waiting_commands = {}  # will be executed in the middle of the fade/flash

    # maps
    map_class = None
    all_maps = {}  # Dictionary of all saved maps, copy from maps class
    second_layer = {}  # dictionary of saved maps' second layer
    map_size = (0, 0)

    wait_for_player1 = False
    wait_for_player2 = False

    # sprites
    sprite_size = 0

    # buttons / switches
    switch = {'cur_mode': 'menu', 'play_mode': None, 'menu': 'main menu', 'player_1': None, 'player_2': None,
              'music': 'sounds/title_music.mp3', 'music_on': True, 'stop_time': False, 'cur_map': 0,
              'start_point': 'right', 'sounds_on': True, 'pause': False, 'reset': False, 'game_over': False,
              'gate_enter': False}

    def __init__(self):
        self.clicked = False
        self.mode = 'two player'
        self.map_screen1 = pygame.Surface((500, 500), pygame.HWSURFACE | pygame.SRCALPHA)
        self.map_screen2 = pygame.Surface((500, 500), pygame.HWSURFACE | pygame.SRCALPHA)
        self.player_1 = None
        self.player_2 = None

    def reset(self):
        self.keys = {1: False, 2: False, 3: False}
        self.map_class.new_map(0, 'right')
        self.keys_total = 0
        self.p1_dead = False
        self.p2_dead = False
        self.camera_x1 = self.start['x1']
        self.camera_y1 = self.start['y1']
        self.camera_x2 = self.start['x2']
        self.camera_y2 = self.start['y2']
        self.stop_time = False
        new = {'cur_mode': 'menu', 'play_mode': None, 'menu': 'main menu', 'player_1': None,
               'player_2': None, 'music': 'sounds/title_music.mp3', 'music_on': True, 'stop_time': False,
               'cur_map': 0, 'start_point': 'right', 'sounds_on': True, 'pause': False, 'reset': False,
               'game_over': False, 'gate_enter': False}
        if not self.switch['music_on']:
            new['music_on'] = False
            new['music'] = None
        if not self.switch['sounds_on']:
            new['sounds_on'] = False

        self.switch = new

    def death(self):
        if self.switch['sounds_on']:
            pygame.mixer.Sound.play(self.sounds['death'])
        self.fade_out = True
        self.waiting_commands['cur_mode'] = 'menu'
        self.waiting_commands['menu'] = 'death screen'
        self.waiting_commands['music'] = None

    def gate_enter(self):
        if self.switch['gate_enter']:
            pygame.mixer.Sound.play(self.sounds['win'])
            self.fade_out = True
            self.waiting_commands['cur_mode'] = 'menu'
            self.waiting_commands['menu'] = 'win screen'
            self.waiting_commands['music'] = None

    def update_game(self):
        # --- PUT ACTIONS HERE ---
        if self.p1_dead:
            if (self.switch['play_mode'] == 'two' and self.p2_dead) or self.switch['play_mode'] == 'single':
                self.death()

        # clock & timer
        if not self.stop_time:
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

        # stop time
        if self.switch['stop_time']:
            self.stoptime()
            self.switch['stop_time'] = False

        # check if players are not moving
        if True not in [self.pressing['up'], self.pressing['down'], self.pressing['left'], self.pressing['right']]:
            self.p2_move = None
            self.camera_2_move = [0, 0]
        if True not in [self.pressing['a'], self.pressing['s'], self.pressing['d'], self.pressing['w']]:
            self.p1_move = None
            self.camera_1_move = [0, 0]

        # enter end gate
        self.gate_enter()

    def stoptime(self):
        if not self.stop_time:
            self.stop_time = True
        else:
            self.stop_time = False

    def fade(self):
        if self.fade_out and not self.flash_in:
            self.fade_screen = pygame.Surface((1000, 500), pygame.SRCALPHA)
            self.fade_screen.fill((0, 0, 0, self.fade_level))
            self.fade_level += 10
            if self.fade_level > 100:
                self.fade_level = 100
                self.fade_out = False
                self.fade_in = True
                for x in self.waiting_commands.keys():
                    if x == 'music' and self.switch['music'] is not None:
                        pygame.mixer.music.fadeout(600)
                    if x == 'music' and self.waiting_commands[x] is not None:
                        pygame.mixer.music.load(self.waiting_commands[x])
                        pygame.mixer.music.play(-1)
                    game.switch[x] = game.waiting_commands[x]
                game.waiting_commands.clear()
        if self.fade_in:
            self.fade_screen = pygame.Surface((1000, 500), pygame.SRCALPHA)
            self.fade_screen.fill((0, 0, 0, self.fade_level))
            self.fade_level -= 20
            if self.fade_level < 0:
                self.fade_level = 0
                self.fade_out = False
                self.fade_in = False

    def flash(self):
        if self.flash_out and not self.flash_in:
            self.flash_screen = pygame.Surface((1000, 500), pygame.SRCALPHA)
            self.flash_screen.fill((153, 48, 32, self.flash_level))
            self.flash_level += 20
            if self.flash_level > 100:
                self.flash_level = 100
                self.flash_out = False
                self.flash_in = True
                for x in self.waiting_commands.keys():
                    if x == 'music' and self.switch['music'] is not None:
                        pygame.mixer.music.fadeout(600)
                    if x == 'music' and self.waiting_commands[x] is not None:
                        pygame.mixer.music.load(self.waiting_commands[x])
                        pygame.mixer.music.play(-1)
                    game.switch[x] = game.waiting_commands[x]
                game.waiting_commands.clear()
        if self.flash_in:
            self.flash_screen = pygame.Surface((1000, 500), pygame.SRCALPHA)
            self.flash_screen.fill((153, 48, 32, self.flash_level))
            self.flash_level -= 20
            if self.flash_level < 0:
                self.flash_level = 0
                self.flash_out = False
                self.flash_in = False

    def last_update(self):
        self.camera_2_move = [0, 0]
        self.camera_1_move = [0, 0]

        self.clicked = False

        # reset
        if self.switch['reset']:
            self.reset()
            self.player_1.reset()
            self.player_2.reset()

    def move_press(self, pressed, name, speed, camera=1):   # name = 'up', 'down', etc
        if not self.stop_time:  # if time hasn't been stopped for example pausing the game
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

            # check if key is pressed -- the player is moving around.
            if pressed and ((camera == 1 and not self.p1_dead) or (camera == 2 and not self.p2_dead)):
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


# F O N T S
class Font(object):
    def __init__(self, name, size=15, colour=(0, 0, 0)):
        self.name = name
        self.size = size
        self.colour = colour
        self.font = pygame.font.SysFont(name, size)

    def text(self, text, pos=None, where=screen):
        t = self.font.render(text, 1, self.colour)
        if pos is not None:
            # setting on or both items in tuple to 'center' centers the text to the screen.
            # negative pos value will be taken from the other end of the screen
            new_pos = list(pos)
            if pos[0] == 'center':
                new_pos[0] = screen_x/2 - t.get_width()/2
            elif pos[0] < 0:
                new_pos[0] = screen_x + pos[0] - t.get_width()
            if pos[1] == 'center':
                new_pos[1] = screen_y/2 - t.get_height()/2
            elif pos[1] < 0:
                new_pos[1] = screen_y + pos[1] - t.get_height()
            where.blit(t, new_pos)
        # returns length, if assigned to a variable
        return t.get_width()


game = Game()
mouse = Mouse()
# cameras are set in maps - new_map

# FONTS
font_1 = Font('courier', colour=(230, 230, 230))
b_font = Font('courier', colour=(0, 0, 0))
header_1 = Font('courier', 25, colour=(230, 230, 230))
header_2 = Font('courier', 20, colour=(230, 230, 230))
header_1_b = Font('courier', 25, colour=(0, 0, 0))  # black headers
header_2_b = Font('courier', 20, colour=(0, 0, 0))
