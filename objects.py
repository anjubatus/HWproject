from sprites import *
from random import choice


class Obj(object):   # mostly sprite and animation cycle work
    all_obj = {}
    hard_obj = []

    def __init__(self, name, base_sprite=None, cycle=None, hard=False):
        self.name = name
        self.sprite = sprites.big_sprites[base_sprite]
        self.cur_sprite = self.sprite

        self.cycles = {}
        self.cur_cycle = cycle

        self.all_obj[name] = self
        if hard:
            self.hard_obj.append(name)

    def add_cycle(self, name, frames):   # for animation
        # name is cycle name, frames is list of frames (in order)
        self.cycles[name] = [0, frames]

    def work_cycle(self, name):
        if game.timer:   # if timer hit, move frame counter onwards - or back to the start.
            if self.cycles[name][0] < len(self.cycles[name][1]) - 1:
                self.cycles[name][0] += 1
            else:
                self.cycles[name][0] = 0

        # finally, set the current frame
        self.cur_sprite = sprites.big_sprites[self.cycles[name][1][self.cycles[name][0]]]


class Player(object):
    max_health = 20
    all_players = {}

    def __init__(self, character, number):
        self.char = character  # of Obj -type
        self.number = number   # - is this player 1 or 2
        self.items = {}
        self.health = self.max_health

        # position & collision
        if self.number == 1:
            self.placement = (game.camera_x1 - (250 - game.sprite_size/2), game.camera_y1 - (250 - game.sprite_size/2))
        else:
            self.placement = (game.camera_x2 - (250 - game.sprite_size/2), game.camera_y2 - (250 - game.sprite_size/2))

        # collision
        # self.collision = pygame.Rect(self.placement[0], self.placement[1],
        #                             self.placement[0] + sprites.new_size, self.placement[1] + sprites.new_size)
        self.collision = pygame.Rect(250 - sprites.new_size / 2, 250 - sprites.new_size / 2,
                                     sprites.new_size, sprites.new_size)

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

        # Enemy damage
        for i in Enemy.all_enemies.values():
            if self.number == 1:
                if self.collision.colliderect(i.collision1):
                    if game.timer:
                        print choice(['p1: ouch!', 'p1: oww!', 'p1: aiie!'])
            else:
                if self.collision.colliderect(i.collision2):
                    if game.timer:
                        print choice(['p2: ouch!', 'p2: oww!', 'p2: aiie!'])

        # hard obj collision
        for i in HardObj.all_hardobj.values():
            if self.number == 1:
                if self.collision.colliderect(i.collision1):
                    if game.timer:
                        print choice(['p1: going through walls.', 'p1: can\'t go here..', 'p1: i\'ll go anyway!'])
            else:
                if self.collision.colliderect(i.collision2):
                    if game.timer:
                        print choice(['p1: going through walls.', 'p1: can\'t go here..', 'p1: i\'ll go anyway!'])


class Enemy(object):
    all_enemies = {}

    def __init__(self, character, goal=None, placement=(0, 0)):
        self.char = character  # is in Obj -object
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

    def movement(self, speed=3):
        if self.goal is not None:
            # if enemy is moving diagonally, the movement should be made slower
            diagonal = False
            if self.placement[0] != self.goal[0] and self.placement[1] != self.goal[1]:
                diagonal = True

            # calculate movement in directions
            if self.placement[0] > self.goal[0]:  # enemy is to the right of the goal
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
        game.map_screen1.blit(self.char.sprite,
                              (game.camera_x1 - self.placement[0], game.camera_y1 - self.placement[1]))
        game.map_screen2.blit(self.char.sprite,
                              (game.camera_x2 - self.placement[0], game.camera_y2 - self.placement[1]))


class HardObj(object):
    # an item that doesn't change position, (usually) cant be walked over
    all_hardobj = {}

    def __init__(self, obj, placement=(0, 0)):
        self.obj = obj  # of class / type Obj
        self.placement = placement
        self.collision1 = pygame.Rect(game.camera_x1 - self.placement[0],
                                      game.camera_y1 - self.placement[1],
                                      sprites.new_size, sprites.new_size)
        self.collision2 = pygame.Rect(500 + game.camera_x2 - self.placement[0],
                                      game.camera_y2 - self.placement[1],
                                      sprites.new_size, sprites.new_size)
        self.all_hardobj[len(self.all_hardobj)] = self

    def update(self):
        # collision
        self.collision1 = pygame.Rect(game.camera_x1 - self.placement[0],
                                      game.camera_y1 - self.placement[1],
                                      sprites.new_size, sprites.new_size)
        self.collision2 = pygame.Rect(game.camera_x2 - self.placement[0],
                                      game.camera_y2 - self.placement[1],
                                      sprites.new_size, sprites.new_size)

        # draw on screen
        game.map_screen1.blit(self.obj.sprite,
                              (game.camera_x1 - self.placement[0], game.camera_y1 - self.placement[1]))
        game.map_screen2.blit(self.obj.sprite,
                              (game.camera_x2 - self.placement[0], game.camera_y2 - self.placement[1]))


# OBJECTS

# player objects
pig_witch = Obj('Pig', 'pig0', cycle='LEFT')
hood_lizard = Obj('Lizard', 'lizard0', cycle='LEFT')
cat_clown = Obj('Cat', 'cat0', cycle='LEFT')

# other objects
pumpkin = Obj('Pumpkin', 'objectA0')
smile_pumpkin = Obj('Smile Pumpkin', 'misc0', hard=True)

# PLAYERS
player_1 = Player(pig_witch, 1)
player_2 = Player(hood_lizard, 2)
# print Player.all_players

# ENEMIES
# -- can be found in the maps file

# ANIMATION cycles
# move left
pig_witch.add_cycle('LEFT', ['pig0', 'pig1'])
hood_lizard.add_cycle('LEFT', ['lizard0', 'lizard1'])
cat_clown.add_cycle('LEFT', ['cat0', 'cat1'])

# move right
pig_witch.add_cycle('RIGHT', ['pig2', 'pig3'])
hood_lizard.add_cycle('RIGHT', ['lizard2', 'lizard3'])
