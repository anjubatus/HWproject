from sprites import *
from random import choice


class Obj(object):   # mostly sprite and animation cycle work
    all_obj = {}
    rand_pos = []
    enemy_obj = []
    cont_objs = {}  # of form name: [object_to_continue, pos, layer]
    scnd_layer_obj = []

    def __init__(self, name, base_sprite=None, cycle=None, rand_pos=False, enemy=False, l2_sprites=None,
                 collision=(0, 0, sprites.new_size, sprites.new_size), cont=None, speed=None):
        self.name = name
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

        self.cycles = {}
        self.cur_cycle = cycle

        self.all_obj[name] = self
        if rand_pos:  # for now only objects, no enemies
            self.rand_pos.append(name)
        if enemy:
            self.enemy_obj.append(name)
        if cont is not None:  # cont = [object_to_continue(name), pos, layer] - pos means (x, y) in relation to original
            self.cont_objs[self.name] = cont

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


class Player(object):
    health_modes = {'max': 30, 'low': 15, 'very low': 5, 'dead': 0, 'sprint max': 20, 'sprint wait': 5}
    health_colors = {'max': (136, 236, 87), 'low': (242, 242, 99), 'very low': (246, 101, 29), 'dead': (0, 0, 0),
                     'sprint': (242, 74, 208)}
    all_players = {}

    def __init__(self, character, number):
        self.char = character  # of Obj -type
        self.number = number   # - is this player 1 or 2
        self.items = {}

        # health
        self.health = self.health_modes['max']
        self.health_bar = pygame.Surface((3*self.health, 15))
        self.health_bg = pygame.Surface((3*self.health, 15))
        self.health_bar.fill(self.health_colors['max'])
        self.health_bg.fill((0, 0, 0))

        # sprint & speed
        self.speed = 4
        self.sprint_in_use = False
        self.sprint = self.health_modes['sprint max']
        self.sprint_wait = self.health_modes['sprint wait']
        self.sprint_bar = pygame.Surface((3 * self.sprint, 15))
        self.sprint_bg = pygame.Surface((3 * self.sprint, 15))
        self.sprint_bar.fill(self.health_colors['sprint'])
        self.sprint_bg.fill((0, 0, 0))

        # position & collision
        if self.number == 1:
            self.placement = (game.camera_x1 - (250 - game.sprite_size/2), game.camera_y1 - (250 - game.sprite_size/2))
        else:
            self.placement = (game.camera_x2 - (250 - game.sprite_size/2), game.camera_y2 - (250 - game.sprite_size/2))
        self.on_tile = (-self.placement[0]/sprites.new_size, -self.placement[1]/sprites.new_size)

        # collision
        self.collision = pygame.Rect(250 - sprites.new_size / 2 + 20, 250,
                                     sprites.new_size - 40, sprites.new_size/2-10)

        # save player to class dictionary
        self.all_players[number] = self

    def determine_health(self):
        if self.health > self.health_modes['low']:
            return 'max'
        elif self.health > self.health_modes['very low']:
            return 'low'
        elif self.health > self.health_modes['dead']:
            return 'very low'
        else:
            return 'dead'

    def update(self):
        # collision
        """if self.number == 1:
            pygame.draw.rect(game.map_screen1, (0, 0, 0), self.collision)"""

        # speed / sprint
        if self.sprint_in_use:
            self.speed = 8
        else:
            self.speed = 4
        if game.timer and self.sprint < self.health_modes['sprint max'] and not self.sprint_in_use:
            self.sprint += 1

        # position/placement
        if self.number == 1:
            self.placement = (game.camera_x1 - (250 - game.sprite_size/2), game.camera_y1 - (250 - game.sprite_size/2))
        else:
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

    def draw_bars(self):
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
            game.map_screen1.blit(self.health_bg, (250 - self.health_bg.get_size()[0] / 2, 20))
            game.map_screen1.blit(self.sprint_bg, (250 - self.sprint_bg.get_size()[0] / 2, 40))
            # bar
            game.map_screen1.blit(self.health_bar, (250 - self.health_bg.get_size()[0] / 2, 20))
            game.map_screen1.blit(self.sprint_bar, (250 - self.sprint_bg.get_size()[0] / 2, 40))
        else:
            # bg
            game.map_screen2.blit(self.health_bg, (250 - self.health_bg.get_size()[0] / 2, 20))
            game.map_screen2.blit(self.sprint_bg, (250 - self.sprint_bg.get_size()[0] / 2, 40))
            # bar
            game.map_screen2.blit(self.health_bar, (250 - self.health_bg.get_size()[0] / 2, 20))
            game.map_screen2.blit(self.sprint_bar, (250 - self.sprint_bg.get_size()[0] / 2, 40))


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


# OBJECTS

# player objects
player_objs = {'pig': Obj('Pig', 'pig0', cycle='LEFT'),
               'lizard': Obj('Lizard', 'lizard0', cycle='LEFT'),
               'cat': Obj('Cat', 'cat0', cycle='LEFT')}

# enemy objects
enemy_objs = {'ghost': Obj('Ghost', 'ghost0', enemy=True, cycle='LEFT'),
              'hatleg': Obj('Leghim', 'hatleg0', enemy=True, cycle='LEFT'),
              'crawler': Obj('Crawler', 'crawler0', enemy=True, cycle='LEFT', speed=2)}

# OTHER objects
# randomized positions
rand_obj = {}
norm_collision = (10, 10, sprites.new_size-20, sprites.new_size-10)
pumpkin_collision = (10, 5, sprites.new_size-20, sprites.new_size-5)
# misc dictionary= name: [collision, sprite name]
misc = {'Plant 1': [norm_collision, 'misc3'], 'Plant 2': [None, 'misc4'], 'Plant 3': [norm_collision, 'misc5'],
        'Santa Skull': [norm_collision, 'misc2'], 'Lights': [None, 'misc0'], 'Hole': [norm_collision, 'misc1'],
        'Pumpkin 1': [pumpkin_collision, 'hw0'], 'Pumpkin 2': [pumpkin_collision, 'hw4'],
        'Tombstone': [norm_collision, 'hw3'], 'Skull': [norm_collision, 'hw7'], 'R. Skull': [norm_collision, 'xmas0'],
        'Ribs': [norm_collision, 'xmas1'], 'Footprints': [None, 'xmas2'], 'Candies': [None, 'xmas3'],
        'Santa Hat': [norm_collision, 'xmas4'], 'Rocks': [norm_collision, 'xmas7']}
for o in misc.keys():
    rand_obj[o] = Obj(o, misc[o][1], rand_pos=True, collision=misc[o][0])

# objects that others will continue from
statue_l = Obj('Statue D', 'hw6', rand_pos=True, collision=(0, -10, sprites.new_size, sprites.new_size+10))
small_tree_l = Obj('S Tree D', 'treeA1', rand_pos=True, collision=(10, -10, sprites.new_size-20, sprites.new_size-20))
p_tree_l = Obj('P Tree D', 'treeB5', rand_pos=True, collision=(10, -10, sprites.new_size-20, sprites.new_size+10))
b_tree_l = Obj('B Tree D', 'treeC7', rand_pos=True, collision=(10, -10, sprites.new_size-20, sprites.new_size-20))
bush_l = Obj('Bush L', 'bush0', rand_pos=True)

# CONTINUING objects
scnd_layer_obj = {}
# scnd_misc dictionary= name: [sprite name, cont-argument]
scnd_misc = {'Statue U': ['hw2', ["Statue D", (0, 1), 2]], 'S Tree U': ['treeA0', ["S Tree D", (0, 1), 2]],
             'Bush R': ['bush1', ["Bush L", (-1, 0), 1]], 'P Tree 1': ['treeB3', ["P Tree D", (0, 1), 2]],
             'P Tree 2': ['treeB2', ["P Tree D", (1, 1), 2]], 'P Tree 3': ['treeB1', ["P Tree D", (0, 2), 2]],
             'P Tree 4': ['treeB0', ["P Tree D", (1, 2), 2]]}
for o in scnd_misc.keys():
    scnd_layer_obj[o] = Obj(o, scnd_misc[o][0], collision=None, cont=scnd_misc[o][1])

b_tree_1 = Obj('B Tree 1', 'treeC6', collision=(10, -10, sprites.new_size-20, sprites.new_size-20),
               cont=["B Tree D", (1, 0), 1])
b_tree_2 = Obj('B Tree 2', 'treeC5', collision=None, cont=["B Tree D", (0, 1), 2])
b_tree_3 = Obj('B Tree 3', 'treeC4', collision=None, cont=["B Tree D", (1, 1), 2])
b_tree_4 = Obj('B Tree 4', 'treeC3', collision=None, cont=["B Tree D", (0, 2), 2])
b_tree_5 = Obj('B Tree 5', 'treeC2', collision=None, cont=["B Tree D", (1, 2), 2])
b_tree_6 = Obj('B Tree 6', 'treeC1', collision=None, cont=["B Tree D", (0, 3), 2])
b_tree_7 = Obj('B Tree 7', 'treeC0', collision=None, cont=["B Tree D", (1, 3), 2])

# gates
gates = {'0A': Obj('Gate 0A', 'gate0', collision=(0, sprites.new_size-20, sprites.new_size, 20)),
         '0B': Obj('Gate 0B', 'gate8', collision=(0, sprites.new_size-20, sprites.new_size, 20)),
         '0C': Obj('Gate 0C', 'gate4', collision=(0, sprites.new_size - 20, sprites.new_size, 20)),
         '0D': Obj('Gate 0D', 'gate9', collision=(0, sprites.new_size - 20, sprites.new_size, 20))
         }

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

# move rightd
for p in player_objs.keys():
    # players
    player_objs[p].add_cycle('RIGHT', [p+'3', p+'4', p+'3', p+'5'])
enemy_objs['ghost'].add_cycle('RIGHT', ['ghost2', 'ghost3'])
enemy_objs['hatleg'].add_cycle('RIGHT', ['hatleg4', 'hatleg5', 'hatleg6', 'hatleg7'])
enemy_objs['crawler'].add_cycle('RIGHT', ['crawler4', 'crawler5', 'crawler6', 'crawler7'])


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
