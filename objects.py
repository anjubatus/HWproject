from sprites import *
from random import choice


class Obj(object):   # mostly sprite and animation cycle work
    all_obj = {}
    rand_pos = []
    enemy_obj = []
    cont_objs = {}  # of form name: [object_to_continue, pos, layer]
    scnd_layer_obj = []

    def __init__(self, name, base_sprite=None, cycle=None, rand_pos=False, enemy=False, l2_sprites=None,
                 collision=(0, 0, sprites.new_size, sprites.new_size), cont=None):
        self.name = name
        self.sprite = sprites.big_sprites[base_sprite]
        self.cur_sprite = self.sprite
        if type(l2_sprites) is dict:
            self.l2_sprites = l2_sprites  # layer 2 sprites for multi-tile objects in  dict mode: (pos): sprite
        else:
            self.l2_sprites = None

        self.collision = collision  # rect arguments inside a single tile-sized surface

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

    def work_cycle(self, name): # 'name' is the name of the cycle like 'LEFT'
        # individual objects of a larger object class will have their own work cycle functions, because the
        # current frame variable should be unique to each of them of them

        if game.timer:   # if timer hit, move frame counter onwards - or back to the start.
            if self.cycles[name][0] < len(self.cycles[name][1]) - 1:
                self.cycles[name][0] += 1
            else:
                self.cycles[name][0] = 0

        # finally, set the current frame
        self.cur_sprite = sprites.big_sprites[self.cycles[name][1][self.cycles[name][0]]]


class Player(object):
    health_modes = {'max': 20, 'low': 10, 'very low': 3, 'dead': 0}
    all_players = {}

    def __init__(self, character, number):
        self.char = character  # of Obj -type
        self.number = number   # - is this player 1 or 2
        self.items = {}

        # health
        self.health = self.health_modes['max']
        self.health_bar = pygame.Surface((5*self.health, 15))
        self.health_bg = pygame.Surface((5*self.health, 15))
        self.health_bar.fill((0, 255, 0))
        self.health_bg.fill((0, 0, 0))

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

    def update(self):
        # collision
        """if self.number == 1:
            pygame.draw.rect(game.map_screen1, (0, 0, 0), self.collision)"""

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
            self.char.work_cycle(dirct)
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

        # Health bar
        self.health_bar = pygame.Surface((5 * self.health, 15))
        self.health_bar.fill((0, 255, 0))


class Enemy(object):
    all_enemies = {}

    def __init__(self, character, goal=None, placement=(0, 0)):
        self.char = character  # is in Obj -object
        self.cur_sprite = self.char.cur_sprite
        self.goal = goal  # position in form of [x, y]. None if enemy has no goal
        self.placement = placement
        self.moving = False
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
            if self.char.cycles[name][0] < len(self.char.cycles[name][1]) - 1:
                self.char.cycles[name][0] += 1
            else:
                self.char.cycles[name][0] = 0

        # finally, set the current frame
        self.cur_sprite = sprites.big_sprites[self.char.cycles[name][1][self.char.cycles[name][0]]]

    def movement(self, speed=3):
        dirct = None
        if self.goal is not None:
            # if enemy is moving diagonally, the movement should be made slower
            diagonal = False
            if self.placement[0] != self.goal[0] and self.placement[1] != self.goal[1]:
                diagonal = True

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

            if self.placement[1] > self.goal[1]:  # enemy is below the goal
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

        # animation cycle
        if dirct is not None and dirct in self.char.cycles.keys():
            self.char.cur_cycle = dirct
            self.char.work_cycle(dirct)
        else:
            self.char.cur_sprite = sprites.big_sprites[self.char.cycles[self.char.cur_cycle][1][0]]

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
        game.map_screen1.blit(self.char.cur_sprite,
                              (game.camera_x1 - self.placement[0], game.camera_y1 - self.placement[1]))
        game.map_screen2.blit(self.char.cur_sprite,
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
pig_witch = Obj('Pig', 'pig0', cycle='LEFT')
hood_lizard = Obj('Lizard', 'lizard0', cycle='LEFT')
cat_clown = Obj('Cat', 'cat0', cycle='LEFT')

# enemy objects
ghost = Obj('Ghost', 'ghost0', enemy=True, cycle='LEFT')

# other objects
# pumpkin = Obj('Pumpkin', 'hw1', enemy=True)
smile_pumpkin = Obj('Smile Pumpkin', 'hw0', rand_pos=True, collision=(10, 5, sprites.new_size-20, sprites.new_size-5))
scream_pumpkin = Obj('Scream Pumpkin', 'hw4', rand_pos=True, collision=(10, 5, sprites.new_size-20,
                                                                         sprites.new_size-5))
tombstone = Obj('Tombstone', 'hw3', rand_pos=True, collision=(10, 10, sprites.new_size-20, sprites.new_size-10))
skull = Obj('Skull', 'hw7', rand_pos=True, collision=(10, 10, sprites.new_size-20, sprites.new_size-10))
r_skull = Obj('Reindeer Skull', 'xmas0', rand_pos=True, collision=(10, 10, sprites.new_size-20, sprites.new_size-10))
ribs = Obj('Ribs', 'xmas1', rand_pos=True, collision=(10, 10, sprites.new_size-20, sprites.new_size-10))
footprints = Obj('Footprints', 'xmas2', rand_pos=True, collision=None)

# objects that others will continue from
statue_l = Obj('Statue Lower', 'hw6', rand_pos=True, collision=(0, -10, sprites.new_size, sprites.new_size+10))
small_tree_l = Obj('Small Tree Lower', 'treeA1', rand_pos=True, collision=(10, -10, sprites.new_size-20,
                                                                           sprites.new_size+10))
p_tree_l = Obj('Pink Tree Lower', 'treeB5', rand_pos=True, collision=(10, -10, sprites.new_size-20,
                                                                      sprites.new_size+10))
b_tree_l = Obj('Big Tree Lower', 'treeC7', rand_pos=True, collision=(10, -10, sprites.new_size-20,
                                                                     sprites.new_size+10))
bush_l = Obj('Bush Left', 'bush0', rand_pos=True)

# CONTINUING objects
statue_u = Obj('Statue Upper', 'hw2', collision=None, cont=["Statue Lower", (0, 1), 2])
small_tree_u = Obj('Small Tree Upper', 'treeA0', collision=None, cont=["Small Tree Lower", (0, 1), 2])
bush_r = Obj('Bush Right', 'bush1', cont=["Bush Left", (-1, 0), 1])

p_tree_1 = Obj('Pink Tree 1', 'treeB3', collision=None, cont=["Pink Tree Lower", (0, 1), 2])
p_tree_2 = Obj('Pink Tree 2', 'treeB2', collision=None, cont=["Pink Tree Lower", (1, 1), 2])
p_tree_3 = Obj('Pink Tree 3', 'treeB1', collision=None, cont=["Pink Tree Lower", (0, 2), 2])
p_tree_4 = Obj('Pink Tree 4', 'treeB0', collision=None, cont=["Pink Tree Lower", (1, 2), 2])

b_tree_1 = Obj('Big Tree 1', 'treeC6', collision=(10, -10, sprites.new_size-20, sprites.new_size+10),
               cont=["Big Tree Lower", (1, 0), 1])
b_tree_2 = Obj('Big Tree 2', 'treeC5', collision=None, cont=["Big Tree Lower", (0, 1), 2])
b_tree_3 = Obj('Big Tree 3', 'treeC4', collision=None, cont=["Big Tree Lower", (1, 1), 2])
b_tree_4 = Obj('Big Tree 4', 'treeC3', collision=None, cont=["Big Tree Lower", (0, 2), 2])
b_tree_5 = Obj('Big Tree 5', 'treeC2', collision=None, cont=["Big Tree Lower", (1, 2), 2])
b_tree_6 = Obj('Big Tree 6', 'treeC1', collision=None, cont=["Big Tree Lower", (0, 3), 2])
b_tree_7 = Obj('Big Tree 7', 'treeC0', collision=None, cont=["Big Tree Lower", (1, 3), 2])

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
    player_objs[p].add_cycle('LEFT', [p+'0', p+'1'])

ghost.add_cycle('LEFT', ['ghost0', 'ghost1'])

# move right
for p in player_objs.keys():
    # players
    player_objs[p].add_cycle('RIGHT', [p+'2', p+'3'])
# pig_witch.add_cycle('RIGHT', ['pig2', 'pig3'])
# hood_lizard.add_cycle('RIGHT', ['lizard2', 'lizard3'])
# cat clown...
ghost.add_cycle('RIGHT', ['ghost2', 'ghost3'])
