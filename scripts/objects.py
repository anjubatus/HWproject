from sprites import *


class Obj(object):   # mostly sprite and animation cycle work
    all_obj = {}  # name: obj
    rand_pos = []
    enemy_obj = []
    cont_objs = {}  # of form name: [object_to_continue, pos, layer]
    scnd_layer_obj = []
    collectibles = []
    gate = None

    def __init__(self, name, base_sprite=None, cycle=None, rand_pos=False, enemy=False, l2_sprites=None,
                 collision=(0, 0, sprites.new_size, sprites.new_size), cont=None, speed=None,
                 collectible=False, cont_tiles_to_right=0, tiles_up=0, tiles_left=0, gate=False):
        self.name = name
        if base_sprite is not None:
            self.sprite = sprites.big_sprites[base_sprite]
            self.cur_sprite = self.sprite
        if type(l2_sprites) is dict:
            self.l2_sprites = l2_sprites  # layer 2 sprites for multi-tile objects in  dict mode: (pos): sprite
        else:
            self.l2_sprites = None

        self.collision = collision  # rect arguments inside a single tile-sized surface

        if speed is None and enemy:
            self.speed = 3
        else:
            self.speed = speed

        self.tiles_right = cont_tiles_to_right  # tell how many continuing tiles there is to expect to the
        # right once the main piece is spawned
        self.tiles_left = tiles_left
        self.tiles_up = tiles_up
        self.gate = gate  # if object is gate, value is True

        self.cycles = {}
        self.cur_cycle = cycle

        if self.name != 'Obj class':
            self.all_obj[name] = self
        if rand_pos:  # for now only objects, no enemies
            self.rand_pos.append(name)
        if enemy:
            self.enemy_obj.append(name)
        if cont is not None:  # cont = [object_to_continue(name), pos, layer] - pos means (x, y) in relation to original
            self.cont_objs[self.name] = cont
        if collectible:
            self.collectibles.append(name)

    def add_cycle(self, name, frames):   # for animation
        # name is cycle name, frames is list of frames (in order)
        self.cycles[name] = [0, frames]

    def work_cycle(self, name, timer=game.timer):  # 'name' is the name of the cycle like 'LEFT'
        # individual objects of a larger object class will have their own work cycle functions, because the
        # current frame variable should be unique to each of them of them

        if timer:   # if timer hit, move frame counter onwards - or back to the start.
            if self.cycles[name][0] < len(self.cycles[name][1]) - 1:
                self.cycles[name][0] += 1
            else:
                self.cycles[name][0] = 0

        # finally, set the current frame
        self.cur_sprite = sprites.big_sprites[self.cycles[name][1][self.cycles[name][0]]]

    def draw_collected_items(self):
        for k in game.keys.keys():
            if False in game.keys.values():
                if game.keys[k]:
                    screen.blit(self.all_obj['Keypiece '+str(k)].cur_sprite, (k*30, 5))
                font_1.text('Find keypieces!', (25, 45))
            else:
                screen.blit(sprites.sprites['item7'], (60, 10))
                font_1.text('Find the gate!', (25, 45))


class Player(object):
    health_modes = {'max': 30, 'low': 15, 'very low': 5, 'dead': 0, 'sprint max': 30, 'sprint wait': 5}
    health_colors = {'max': (103, 189, 66), 'low': (227, 227, 77), 'very low': (219, 115, 50), 'dead': (0, 0, 0),
                     'sprint': (245, 78, 189)}
    all_players = {}
    char_frames = {'Pig': sprites.big_sprites['frame0'], 'Lizard': sprites.big_sprites['frame1'],
                   'Cat': sprites.big_sprites['frame3']}
    inventory = []

    def __init__(self, character, number):
        self.char = character  # of Obj -type
        self.number = number   # - is this player 1 or 2
        self.items = {}

        # health
        self.health = self.health_modes['max']
        self.health_bar = pygame.Surface((3*self.health, 15))
        h_bg = pygame.Surface((3*self.health, 15))  # black bg
        h_bg.fill((0, 0, 0))
        h_bg2 = pygame.Surface((3*self.health + 4, 19))  # frames
        h_bg2.fill((220, 220, 220))
        h_bg2.blit(h_bg, (2, 2))
        self.health_bg = h_bg2
        self.health_bar.fill(self.health_colors['max'])

        self.ready_to_leave = False

        # sprint & speed
        self.speed = 4
        self.sprint_in_use = False
        self.sprint = self.health_modes['sprint max']
        self.sprint_wait = self.health_modes['sprint wait']
        self.sprint_bar = pygame.Surface((3 * self.sprint, 15))
        s_bg = pygame.Surface((3 * self.sprint, 15))  # black bg
        s_bg.fill((0, 0, 0))
        s_bg2 = pygame.Surface((3 * self.sprint + 4, 19))  # frames
        s_bg2.fill((220, 220, 220))
        s_bg2.blit(s_bg, (2, 2))
        self.sprint_bg = s_bg2
        self.sprint_bar.fill(self.health_colors['sprint'])

        # position & collision
        if self.number == 1:
            self.placement = (game.camera_x1 - (250 - game.sprite_size/2), game.camera_y1 - (250 - game.sprite_size/2))
        else:
            self.placement = (game.camera_x2 - (250 - game.sprite_size/2), game.camera_y2 - (250 - game.sprite_size/2))
        self.on_tile = (-self.placement[0]/sprites.new_size, -self.placement[1]/sprites.new_size)

        # collision
        self.collision = pygame.Rect(250 - sprites.new_size / 2 + 20, 250,
                                     sprites.new_size - 40, sprites.new_size/2-10)

        # save player to class dictionary and game
        self.all_players[number] = self
        if self.number == 1:
            game.player_1 = self
        else:
            game.player_2 = self

    def reset(self):
        self.health = self.health_modes['max']
        self.sprint = self.health_modes['sprint max']

        # position & collision
        if self.number == 1:
            self.placement = (
                game.camera_x1 - (250 - game.sprite_size / 2), game.camera_y1 - (250 - game.sprite_size / 2))
        else:
            self.placement = (
                game.camera_x2 - (250 - game.sprite_size / 2), game.camera_y2 - (250 - game.sprite_size / 2))
        self.on_tile = (-self.placement[0] / sprites.new_size, -self.placement[1] / sprites.new_size)

    def determine_health(self):
        if self.health > self.health_modes['low']:
            return 'max'
        elif self.health > self.health_modes['very low']:
            return 'low'
        elif self.health > self.health_modes['dead']:
            return 'very low'
        else:
            if self.number == 1:
                game.p1_dead = True
            else:
                game.p2_dead = True
            return 'dead'

    def update(self):
        # updates if time is not stopped
        if not game.stop_time and not game.fade_out and not game.fade_in:

            # speed / sprint
            if self.sprint_in_use:
                self.speed = 8
            else:
                self.speed = 4
            if game.timer and self.sprint < self.health_modes['sprint max'] and not self.sprint_in_use:
                self.sprint += 1

            # position/placement
            if self.number == 1 and not game.p1_dead:
                self.placement = (game.camera_x1 - (250 - game.sprite_size/2), game.camera_y1 - (250 - game.sprite_size/2))
            elif self.number == 2 and not game.p2_dead:
                self.placement = (game.camera_x2 - (250 - game.sprite_size/2), game.camera_y2 - (250 - game.sprite_size/2))
            self.on_tile = (-self.placement[0] / sprites.new_size, -self.placement[1] / sprites.new_size)

            # Animation cycles and direction
            if self.number == 1:
                dirct = game.p1_move
            else:
                dirct = game.p2_move
            if dirct is not None and dirct in self.char.cycles.keys():
                self.char.cur_cycle = dirct
                if self.sprint_in_use:  # if character is sprinting, animate faster
                    self.char.work_cycle(dirct, game.timer_2)
                else:
                    self.char.work_cycle(dirct, game.timer)
            else:
                self.char.cur_sprite = sprites.big_sprites[self.char.cycles[self.char.cur_cycle][1][0]]

            # Enemy collision
            for i in Enemy.all_enemies.values():
                if self.number == 1:
                    if self.collision.colliderect(i.collision1) and self.health > 0:
                        if game.timer:
                            self.health -= 1
                else:
                    if self.collision.colliderect(i.collision2) and self.health > 0:
                        if game.timer:
                            self.health -= 1

            # Collectible collision
            for i in Collectible.all_collectibles:
                if self.number == 1:
                    if self.collision.colliderect(i.collision1):
                        i.collected()
                else:
                    if self.collision.colliderect(i.collision2):
                        i.collected()

            # Gate collision
            gate = Obj.gate
            if gate is not None:
                if game.switch['play_mode'] == 'single':
                    if self.collision.colliderect(gate.enter1):
                        self.ready_to_leave = True
                    else:
                        self.ready_to_leave = False
                else:
                    if self.number == 1:
                        if self.collision.colliderect(gate.enter1):
                            self.ready_to_leave = True
                        else:
                            self.ready_to_leave = False
                    else:
                        if self.collision.colliderect(gate.enter2):
                            self.ready_to_leave = True
                        else:
                            self.ready_to_leave = False
            else:
                self.ready_to_leave = False

            # update to GAME
            if self.number == 1:
                game.player_1 = self
            else:
                game.player_2 = self

    def draw_bars(self):
        # Draws bars, frames and darkening associated with the player
        # DARKENING & FRAMES
        if self.number == 1:
            game.map_screen1.blit(sprites.big_sprites['shade0'], (0, 0))
            if game.switch['play_mode'] != 'single':
                game.map_screen1.blit(self.char_frames[self.char.name], (0, 0))
        else:
            game.map_screen2.blit(sprites.big_sprites['shade0'], (0, 0))
            if game.switch['play_mode'] != 'single':
                game.map_screen2.blit(self.char_frames[self.char.name], (0, 0))

        # BARS
        # Determine current health/sprint bar
        if self.health >= 0:
            self.health_bar = pygame.Surface((3 * self.health, 15))
        else:
            self.health_bar = pygame.Surface((0, 0))
        self.health_bar.fill(self.health_colors[self.determine_health()])
        if self.sprint >= 0:
            self.sprint_bar = pygame.Surface((3 * self.sprint, 15))
        else:
            self.sprint_bar = pygame.Surface((0, 0))
        self.sprint_bar.fill(self.health_colors['sprint'])

        # draw health and sprint bars
        if self.number == 1:
            # bg
            game.map_screen1.blit(self.health_bg, (250 - self.health_bg.get_size()[0] / 2-2, 20-2))
            game.map_screen1.blit(self.sprint_bg, (250 - self.sprint_bg.get_size()[0] / 2-2, 45-2))
            # bar
            game.map_screen1.blit(self.health_bar, (250 - self.health_bg.get_size()[0] / 2, 20))
            game.map_screen1.blit(self.sprint_bar, (250 - self.sprint_bg.get_size()[0] / 2, 45))
            # text
            font_1.text('HP', (240, 20), where=game.map_screen1)
            font_1.text('SPR', (235, 45), where=game.map_screen1)
        else:
            # bg
            game.map_screen2.blit(self.health_bg, (250 - self.health_bg.get_size()[0] / 2-2, 20-2))
            game.map_screen2.blit(self.sprint_bg, (250 - self.sprint_bg.get_size()[0] / 2-2, 45-2))
            # bar
            game.map_screen2.blit(self.health_bar, (250 - self.health_bg.get_size()[0] / 2, 20))
            game.map_screen2.blit(self.sprint_bar, (250 - self.sprint_bg.get_size()[0] / 2, 45))
            # text
            font_1.text('HP', (240, 20), where=game.map_screen2)
            font_1.text('SPR', (235, 45), where=game.map_screen2)


class Enemy(object):
    all_enemies = {}

    def __init__(self, character, goal=None, placement=(0, 0)):
        self.char = character  # is in Obj -object

        # sprites and animation
        self.cur_sprite = self.char.cur_sprite
        self.cur_cycle = self.char.cur_cycle
        self.cycles = self.char.cycles

        self.goal = goal  # position in form of [x, y]. None if enemy has no goal
        self.placement = placement
        self.moving = False
        self.speed = self.char.speed
        self.collision1 = pygame.Rect(game.camera_x1 - self.placement[0],
                                      game.camera_y1 - self.placement[1],
                                      sprites.new_size, sprites.new_size)
        self.collision2 = pygame.Rect(500 + game.camera_x2 - self.placement[0],
                                      game.camera_y2 - self.placement[1],
                                      sprites.new_size, sprites.new_size)

        # register enemy in class dictionary
        self.all_enemies[len(self.all_enemies)] = self

    def work_cycle(self, name):  # 'name' is the name of the cycle like 'LEFT'
        if game.timer:   # if timer hit, move frame counter onwards - or back to the start.
            if self.cycles[name][0] < len(self.cycles[name][1]) - 1:
                self.cycles[name][0] += 1
            else:
                self.cycles[name][0] = 0

        # finally, set the current frame
        self.cur_sprite = sprites.big_sprites[self.cycles[name][1][self.cycles[name][0]]]

    def movement(self, speed=None):
        if not game.stop_time:
            if speed is None:
                speed = self.speed
            dirct = None
            if self.goal is not None:
                # if enemy is moving diagonally, the movement should be made slower
                diagonal = False
                if self.placement[0] != self.goal[0] and self.placement[1] != self.goal[1]:
                    diagonal = True

                if self.placement[1] > self.goal[1]:  # enemy is below the goal
                    # set direction for animation
                    dirct = 'DOWN'

                    if diagonal:
                        if self.placement[1] - self.goal[1] < speed:
                            self.placement[1] -= 1
                        else:
                            self.placement[1] -= speed - 1
                    else:
                        if self.placement[1] - self.goal[1] < speed:
                            self.placement[1] -= 1
                        else:
                            self.placement[1] -= speed

                if self.placement[1] < self.goal[1]:  # enemy is higher than the goal
                    # set direction for animation
                    dirct = 'UP'

                    if diagonal:
                        if self.goal[1] - self.placement[1] < speed:
                            self.placement[1] += 1
                        else:
                            self.placement[1] += speed - 1
                    else:
                        if self.goal[1] - self.placement[1] < speed:
                            self.placement[1] += 1
                        else:
                            self.placement[1] += speed

                # calculate movement in directions
                if self.placement[0] > self.goal[0]:  # enemy is to the right of the goal
                    # set direction for animation
                    dirct = 'RIGHT'

                    # move enemy diagonally or not
                    if diagonal:
                        if self.placement[0] - self.goal[0] < speed:
                            self.placement[0] -= 1
                        else:
                            self.placement[0] -= speed - 1
                    else:
                        if self.placement[0] - self.goal[0] < speed:
                            self.placement[0] -= 1
                        else:
                            self.placement[0] -= speed

                elif self.placement[0] < self.goal[0]:  # enemy is to the left of the goal
                    # set direction for animation
                    dirct = 'LEFT'

                    # move enemy diagonally or not
                    if diagonal:
                        if self.goal[0] - self.placement[0] < speed:
                            self.placement[0] += 1
                        else:
                            self.placement[0] += speed - 1
                    else:
                        if self.goal[0] - self.placement[0] < speed:
                            self.placement[0] += 1
                        else:
                            self.placement[0] += speed

            # animation cycle
            if dirct is not None and dirct in self.char.cycles.keys():
                self.cur_cycle = dirct
                self.work_cycle(dirct)
            else:
                self.cur_sprite = sprites.big_sprites[self.cycles[self.cur_cycle][1][0]]

    def update(self, goal='players'):

        # set collision
        self.collision1 = pygame.Rect(game.camera_x1 - self.placement[0],
                                      game.camera_y1 - self.placement[1],
                                      sprites.new_size, sprites.new_size)
        self.collision2 = pygame.Rect(game.camera_x2 - self.placement[0],
                                      game.camera_y2 - self.placement[1],
                                      sprites.new_size, sprites.new_size)
        # pygame.draw.rect(game.map_screen1, (0, 0, 0), self.collision1)
        # pygame.draw.rect(game.map_screen2, (0, 0, 0), self.collision2)

        # set goal
        if goal == 'players':
            distance = (0, 0)
            for p in Player.all_players.values():
                if abs(p.placement[0] - self.placement[0]) < 150 and abs(p.placement[1] - self.placement[1]) < 150:
                    self.goal = p.placement
                    distance = (abs(p.placement[0] - self.placement[0]), abs(p.placement[1] - self.placement[1]))
            if distance is (0, 0):
                self.goal = None
        self.movement()

    def draw(self):
        game.map_screen1.blit(self.cur_sprite,
                              (game.camera_x1 - self.placement[0], game.camera_y1 - self.placement[1]))
        game.map_screen2.blit(self.cur_sprite,
                              (game.camera_x2 - self.placement[0], game.camera_y2 - self.placement[1]))


class HardObj(object):
    # an item that doesn't change position, (usually) cant be walked over
    all_hardobj = {}  # of form index: obj

    def __init__(self, obj, placement=(0, 0)):
        self.obj = obj  # of class / type Obj
        self.placement = placement
        if self.obj.collision is not None:
            self.collision1 = pygame.Rect(game.camera_x1 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y1 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])
            self.collision2 = pygame.Rect(game.camera_x2 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y2 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])
        else:
            self.collision1 = None
            self.collision2 = None

        # save obj in class dict
        self.all_hardobj[len(self.all_hardobj)] = self

    def update(self):
        # collision; same code as in init
        if self.collision1 is not None:
            self.collision1 = pygame.Rect(game.camera_x1 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y1 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])
            self.collision2 = pygame.Rect(game.camera_x2 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y2 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])

    def draw(self):
        # draw on screen
        game.map_screen1.blit(self.obj.sprite,
                              (game.camera_x1 - self.placement[0], game.camera_y1 - self.placement[1]))
        game.map_screen2.blit(self.obj.sprite,
                              (game.camera_x2 - self.placement[0], game.camera_y2 - self.placement[1]))


class Collectible(object):
    # an item that doesn't change position, (usually) cant be walked over
    all_collectibles = []  # of form index: obj

    def __init__(self, obj, placement=(0, 0), key=None):
        self.obj = obj  # of class / type Obj
        self.placement = placement
        if self.obj.collision is not None:
            self.collision1 = pygame.Rect(game.camera_x1 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y1 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])
            self.collision2 = pygame.Rect(game.camera_x2 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y2 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])
        else:
            self.collision1 = None
            self.collision2 = None

        self.key = key  # either None if item is not a key piece; else a number 1 to 3

        # save obj in class dict
        self.all_collectibles.append(self)

    def update(self):
        # collision; same code as in init
        if self.collision1 is not None:
            self.collision1 = pygame.Rect(game.camera_x1 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y1 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])
            self.collision2 = pygame.Rect(game.camera_x2 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y2 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])

    def draw(self):
        # draw on screen
        game.map_screen1.blit(self.obj.sprite,
                              (game.camera_x1 - self.placement[0], game.camera_y1 - self.placement[1]))
        game.map_screen2.blit(self.obj.sprite,
                              (game.camera_x2 - self.placement[0], game.camera_y2 - self.placement[1]))

    def collected(self):
        if self.key is not None and self.key in game.keys.keys() and not game.keys[self.key]:
            game.keys[self.key] = True
            game.keys_total += 1
            pygame.mixer.Sound.play(game.sounds['key'])
        else:
            Player.inventory.append(self)
            pygame.mixer.Sound.play(game.sounds['item'])
        self.all_collectibles.remove(self)


class Gate(object):
    final_gate = None

    def __init__(self, obj, placement=(0, 0)):
        self.obj = obj  # of class / type Obj
        self.placement = placement
        if self.obj.collision is not None:
            self.collision1 = pygame.Rect(game.camera_x1 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y1 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])
            self.collision2 = pygame.Rect(game.camera_x2 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y2 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])
        else:
            self.collision1 = None
            self.collision2 = None

        self.enter_tile = (0, sprites.new_size, sprites.new_size*3, sprites.new_size*2)
        self.enter1 = pygame.Rect(game.camera_x1 - self.placement[0] + self.enter_tile[0],
                                  game.camera_y1 - self.placement[1] + self.enter_tile[1],
                                  self.enter_tile[2], self.enter_tile[3])
        self.enter2 = pygame.Rect(game.camera_x2 - self.placement[0] + self.enter_tile[0],
                                  game.camera_y2 - self.placement[1] + self.enter_tile[1],
                                  self.enter_tile[2], self.enter_tile[3])

        self.final_gate = self
        Obj.gate = self

    def update(self):
        # collision; same code as in init
        if self.collision1 is not None:
            self.collision1 = pygame.Rect(game.camera_x1 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y1 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])
            self.collision2 = pygame.Rect(game.camera_x2 - self.placement[0] + self.obj.collision[0],
                                          game.camera_y2 - self.placement[1] + self.obj.collision[1],
                                          self.obj.collision[2], self.obj.collision[3])
        # entering the gate
        self.enter_tile = (0, 0, sprites.new_size * 3, sprites.new_size)
        self.enter1 = pygame.Rect(game.camera_x1 - self.placement[0] + self.enter_tile[0],
                                  game.camera_y1 - self.placement[1] + self.enter_tile[1],
                                  self.enter_tile[2], self.enter_tile[3])
        self.enter2 = pygame.Rect(game.camera_x2 - self.placement[0] + self.enter_tile[0],
                                  game.camera_y2 - self.placement[1] + self.enter_tile[1],
                                  self.enter_tile[2], self.enter_tile[3])

        # save gate
        Obj.gate = self

    def draw(self):
        # draw on screen
        game.map_screen1.blit(self.obj.sprite,
                              (game.camera_x1 - self.placement[0], game.camera_y1 - self.placement[1]))
        game.map_screen2.blit(self.obj.sprite,
                              (game.camera_x2 - self.placement[0], game.camera_y2 - self.placement[1]))


# OBJECTS
obj_class = Obj('Obj class')

# player objects
player_objs = {'pig': Obj('Pig', 'pig0', cycle='LEFT'),
               'lizard': Obj('Lizard', 'lizard0', cycle='LEFT'),
               'cat': Obj('Cat', 'cat0', cycle='LEFT')}

# enemy objects
enemy_objs = {'ghost': Obj('Ghost', 'ghost0', enemy=True, cycle='LEFT', speed=4),
              'hatleg': Obj('Leghim', 'hatleg0', enemy=True, cycle='LEFT', speed=4),
              'crawler': Obj('Crawler', 'crawler0', enemy=True, cycle='LEFT', speed=3),
              'bat': Obj('Bat', 'bat0', enemy=True, cycle='LEFT', speed=4)}

# ITEMS/OBJECTS
# randomized positions
rand_obj = {}
norm_collision = (10, 10, sprites.new_size-20, sprites.new_size-10)
pumpkin_collision = (10, 5, sprites.new_size-20, sprites.new_size-5)

# collectibles
mushroom = Obj('Mushroom', 'item0', collision=norm_collision, collectible=True)
eyenion = Obj('Eyenion', 'item1', collision=norm_collision, collectible=True)
monkey_paw = Obj('Monkey Paw', 'item2', collision=norm_collision, collectible=True)
key_1 = Obj('Keypiece 1', 'item3', collision=norm_collision, collectible=True)
key_2 = Obj('Keypiece 2', 'item4', collision=norm_collision, collectible=True)
key_3 = Obj('Keypiece 3', 'item5', collision=norm_collision, collectible=True)

# OTHER objects
# misc dictionary= name: [collision, sprite name]
# ONE TILE OBJECTS
one_tile = []
no_col = [6, 7, 15, 24, 25, 31, 33]
dont_exist = [8, 17, 36, 13]
snow = [26, 31, 33]
no_snow = [30, 28, 22]
misc = {}
for i in sprites.sprites.keys():  # find all one tile size objects
    if "onetile" in i:
        one_tile.append(i)
for x in one_tile:
    if int(x[7:]) not in dont_exist:
        if int(x[7:]) in no_col:
            if int(x[7:]) in snow:  # if appears only in snow maps
                misc[x + " (snow)"] = [None, x]
            elif int(x[7:]) in no_snow:  # if appears only in no snow maps
                misc[x + " (no snow)"] = [None, x]
        else:
            if int(x[7:]) in snow:  # if appears only in snow maps
                misc[x + " (snow)"] = [norm_collision, x]
            elif int(x[7:]) in no_snow:  # if appears only in no snow maps
                misc[x + " (no snow)"] = [norm_collision, x]

for o in misc.keys():
    rand_obj[o] = Obj(o, misc[o][1], rand_pos=True, collision=misc[o][0])

# TWO TILE OBJECTS
lamp_d = Obj('twotileUP3', 'twotileUP3', rand_pos=True, collision=(10, -10, sprites.new_size-20, sprites.new_size+10))
shedA_d = Obj('twotileUP4', 'twotileUP4', rand_pos=True, collision=(10, -10, sprites.new_size-20, sprites.new_size-20))
shedB_d = Obj('twotileUP5', 'twotileUP5', rand_pos=True, collision=(10, -10, sprites.new_size-20, sprites.new_size-20))
statue_d = Obj('twotileUP9', 'twotileUP9', rand_pos=True, collision=(0, -10, sprites.new_size, sprites.new_size+10))
statue2_d = Obj('twotileUP10', 'twotileUP10', rand_pos=True, collision=(0, -10, sprites.new_size, sprites.new_size+10))
s_tree_d = Obj('twotileUP15 (no snow)', 'twotileUP15', rand_pos=True,
               collision=(10, -10, sprites.new_size-20, sprites.new_size-20))
ss_tree_d = Obj('twotileUP16 (snow)', 'twotileUP16', rand_pos=True,
                collision=(10, -10, sprites.new_size-20, sprites.new_size-20))
stick_d = Obj('twotileUP17 (no snow)', 'twotileUP17', rand_pos=True,
              collision=(10, -10, sprites.new_size-20, sprites.new_size-20))

m_gate_0 = Obj('Main Gate 0', 'mgate3', collision=(10, -10, sprites.new_size-20, sprites.new_size-20),
               cont_tiles_to_right=2)

# BIG objects (trees)
treeA_1 = Obj('treeA12 (no snow)', 'treeA12', rand_pos=True,
              collision=(10, -10, sprites.new_size-20, sprites.new_size-20))
treeA_1s = Obj('treeA14 (snow)', 'treeA14', rand_pos=True,
               collision=(10, -10, sprites.new_size-20, sprites.new_size-20))
treeB_1 = Obj('treeB4 (no snow)', 'treeB4', rand_pos=True, collision=(0, -10, sprites.new_size, sprites.new_size+10))
treeB_1s = Obj('treeB5 (snow)', 'treeB5', rand_pos=True, collision=(0, -10, sprites.new_size, sprites.new_size+10))
treeC_1 = Obj('treeC8 (no snow)', 'treeC8', rand_pos=True, collision=(10, -10, sprites.new_size-20, sprites.new_size-20))
treeC_1s = Obj('treeC10 (snow)', 'treeC10', rand_pos=True, collision=(10, -10, sprites.new_size-20, sprites.new_size-20))
treeD_1 = Obj('treeD8 (no snow)', 'treeD8', rand_pos=True, collision=None)
treeD_1s = Obj('treeD10 (snow)', 'treeD10', rand_pos=True, collision=None)

# CONTINUING objects
scnd_layer_obj = {}
# scnd_misc dictionary= name: [sprite name, cont-argument]
cont = {'twotileUP0': ['twotileUP0', ["twotileUP3", (0, 1), 2]],
        'twotileUP1': ['twotileUP1', ["twotileUP4", (0, 1), 2]],
        'twotileUP2': ['twotileUP2', ["twotileUP5", (0, 1), 2]],
        'twotileUP6': ['twotileUP6', ["twotileUP9", (0, 1), 2]],
        'twotileUP7': ['twotileUP7', ["twotileUP10", (0, 1), 2]],
        'twotileUP12': ['twotileUP12', ["twotileUP15 (no snow)", (0, 1), 2]],
        'twotileUP13': ['twotileUP13', ["twotileUP16 (snow)", (0, 1), 2]],
        'twotileUP14': ['twotileUP14', ["twotileUP17 (no snow)", (0, 1), 2]],

        'treeA0': ['treeA0', ["treeA12 (no snow)", (0, 3), 2]], 'treeA1': ['treeA1', ["treeA12 (no snow)", (-1, 3), 2]],
        'treeA4': ['treeA4', ["treeA12 (no snow)", (0, 2), 2]], 'treeA5': ['treeA5', ["treeA12 (no snow)", (-1, 2), 2]],
        'treeA8': ['treeA8', ["treeA12 (no snow)", (0, 1), 2]], 'treeA9': ['treeA9', ["treeA12 (no snow)", (-1, 1), 2]],
        'treeA2s': ['treeA2', ["treeA14 (snow)", (0, 3), 2]], 'treeA3s': ['treeA3', ["treeA14 (snow)", (-1, 3), 2]],
        'treeA6s': ['treeA6', ["treeA14 (snow)", (0, 2), 2]], 'treeA7s': ['treeA7', ["treeA14 (snow)", (-1, 2), 2]],
        'treeA10s': ['treeA10', ["treeA14 (snow)", (0, 1), 2]], 'treeA11s': ['treeA11', ["treeA14 (snow)", (-1, 1), 2]],

        'treeB0': ['treeB0', ["treeB4 (no snow)", (0, 2), 2]], 'treeB2': ['treeB2', ["treeB4 (no snow)", (0, 1), 2]],
        'treeB1s': ['treeB1', ["treeB5 (snow)", (0, 2), 2]], 'treeB3s': ['treeB3', ["treeB5 (snow)", (0, 1), 2]],

        'treeC0': ['treeC0', ["treeC8 (no snow)", (0, 2), 2]], 'treeC1': ['treeC1', ["treeC8 (no snow)", (-1, 2), 2]],
        'treeC4': ['treeC4', ["treeC8 (no snow)", (0, 1), 2]], 'treeC5': ['treeC5', ["treeC8 (no snow)", (-1, 1), 2]],
        'treeC2s': ['treeC2', ["treeC10 (snow)", (0, 2), 2]], 'treeC3s': ['treeC3', ["treeC10 (snow)", (-1, 2), 2]],
        'treeC6s': ['treeC6', ["treeC10 (snow)", (0, 1), 2]], 'treeC7s': ['treeC7', ["treeC10 (snow)", (-1, 1), 2]],

        'treeD0': ['treeD0', ["treeD8 (no snow)", (0, 2), 2]], 'treeD1': ['treeD1', ["treeD8 (no snow)", (-1, 2), 2]],
        'treeD4': ['treeD4', ["treeD8 (no snow)", (0, 1), 2]], 'treeD5': ['treeD5', ["treeD8 (no snow)", (-1, 1), 2]],
        'treeD2s': ['treeD2', ["treeD10 (snow)", (0, 2), 2]], 'treeD3s': ['treeD3', ["treeD10 (snow)", (-1, 2), 2]],
        'treeD6s': ['treeD6', ["treeD10 (snow)", (0, 1), 2]], 'treeD7s': ['treeD7', ["treeD10 (snow)", (-1, 1), 2]]
        }
for o in cont.keys():
    scnd_layer_obj[o] = Obj(o, cont[o][0], collision=None, cont=cont[o][1])
bush_r = Obj('Bush R', 'bush1', collision=(10, -10, sprites.new_size-20, sprites.new_size-20),
             cont=["Bush L (no snow)", (-1, 0), 1])

treeA_2 = Obj('treeA13', 'treeA13', collision=(10, -10, sprites.new_size-20, sprites.new_size-20),
              cont=["treeA12 (no snow)", (-1, 0), 1])
treeA_2s = Obj('treeA15', 'treeA15', collision=(10, -10, sprites.new_size-20, sprites.new_size-20),
               cont=["treeA14 (snow)", (-1, 0), 1])
treeC_2 = Obj('treeC9', 'treeC9', collision=(10, -10, sprites.new_size-20, sprites.new_size-20),
              cont=["treeC8 (no snow)", (-1, 0), 1])
treeC_2s = Obj('treeC11', 'treeC11', collision=(10, -10, sprites.new_size-20, sprites.new_size-20),
               cont=["treeC10 (snow)", (-1, 0), 1])
treeD_2 = Obj('treeD9', 'treeD9', collision=(10, -10, sprites.new_size-20, sprites.new_size-20),
              cont=["treeD8 (no snow)", (-1, 0), 1])
treeD_2s = Obj('treeD11', 'treeD11', collision=norm_collision,
               cont=["treeD10 (snow)", (-1, 0), 1])

# gates
m_gate_1 = Obj('Main Gate 1', 'mgate4', collision=(10, -10, sprites.new_size-20, sprites.new_size-20),
               cont=["Main Gate 0", (-1, 0), 1])
m_gate_2 = Obj('Main Gate 2', 'mgate5', collision=(10, -10, sprites.new_size-20, sprites.new_size-20),
               cont=["Main Gate 0", (-2, 0), 1])
m_gate_3 = Obj('Main Gate 3', 'mgate0', collision=None, cont=["Main Gate 0", (0, 1), 2])
m_gate_4 = Obj('Main Gate 4', 'mgate1', collision=None, cont=["Main Gate 0", (-1, 1), 2])
m_gate_5 = Obj('Main Gate 5', 'mgate2', collision=None, cont=["Main Gate 0", (-2, 1), 2])

gates = {'0A': Obj('Gate 0A', 'gate0', collision=(0, sprites.new_size-20, sprites.new_size, 20)),
         '0B': Obj('Gate 0B', 'gate8', collision=(0, sprites.new_size-20, sprites.new_size, 20)),
         '0C': Obj('Gate 0C', 'gate4', collision=(0, sprites.new_size - 20, sprites.new_size, 20)),
         '0D': Obj('Gate 0D', 'gate9', collision=(0, sprites.new_size - 20, sprites.new_size, 20))}

# PLAYERS
player_1 = Player(player_objs['pig'], 1)
player_2 = Player(player_objs['lizard'], 2)

# ENEMIES
# -- can be found in the maps file

# ANIMATION cycles
# move left
for p in player_objs.keys():
    # players
    player_objs[p].add_cycle('LEFT', [p+'0', p+'1', p+'0', p+'2'])

enemy_objs['ghost'].add_cycle('LEFT', ['ghost0', 'ghost1'])
enemy_objs['hatleg'].add_cycle('LEFT', ['hatleg0', 'hatleg1', 'hatleg2', 'hatleg3'])
enemy_objs['crawler'].add_cycle('LEFT', ['crawler0', 'crawler1', 'crawler2', 'crawler3'])
enemy_objs['bat'].add_cycle('LEFT', ['bat0', 'bat1', 'bat2', 'bat3'])

# move right
for p in player_objs.keys():
    # players
    player_objs[p].add_cycle('RIGHT', [p+'3', p+'4', p+'3', p+'5'])
enemy_objs['ghost'].add_cycle('RIGHT', ['ghost2', 'ghost3'])
enemy_objs['hatleg'].add_cycle('RIGHT', ['hatleg4', 'hatleg5', 'hatleg6', 'hatleg7'])
enemy_objs['crawler'].add_cycle('RIGHT', ['crawler4', 'crawler5', 'crawler6', 'crawler7'])
enemy_objs['bat'].add_cycle('RIGHT', ['bat4', 'bat5', 'bat6', 'bat7'])

# move up
for p in player_objs.keys():
    # players
    player_objs[p].add_cycle('UP', [p+'6', p+'7', p+'6', p+'8'])
enemy_objs['hatleg'].add_cycle('UP', ['hatleg8', 'hatleg9', 'hatleg10', 'hatleg11'])
enemy_objs['crawler'].add_cycle('UP', ['crawler8', 'crawler9', 'crawler10', 'crawler11'])

# move down
for p in player_objs.keys():
    # players
    player_objs[p].add_cycle('DOWN', [p+'9', p+'10', p+'9', p+'11'])
enemy_objs['hatleg'].add_cycle('DOWN', ['hatleg4', 'hatleg5', 'hatleg6', 'hatleg7'])
enemy_objs['crawler'].add_cycle('DOWN', ['crawler4', 'crawler5', 'crawler6', 'crawler7'])
