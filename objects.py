from sprites import *


class Obj(object):
    def __init__(self, name, base_sprite=None, constant_anim=False, cycle=None):
        self.name = name
        self.sprite = sprites.big_sprites[base_sprite]
        self.cur_sprite = self.sprite

        self.cycles = {}
        self.constant_anim = constant_anim
        self.cur_cycle = cycle

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
    def __init__(self, character, number):
        self.char = character  # of Obj -type
        self.number = number   # - is this player 1 or 2
        self.items = {}
        self.placement = None

    def update(self):
        # position/placement
        if self.number == 1:
            self.placement = (game.camera_x1 - (250 - game.sprite_size/2), game.camera_y1 - (250 - game.sprite_size/2))
        else:
            self.placement = (game.camera_x1 - (250 - game.sprite_size/2), game.camera_y1 - (250 - game.sprite_size/2))

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


class Enemy(object):
    def __init__(self, character, goal=None, placement=None):
        self.char = character  # is in Obj -object
        self.goal = goal  # position in form of [x, y]. None if enemy has no goal
        self.placement = placement
        self.moving = False

    def movement(self, speed=3):
        if self.goal is not None:
            # if enemy is moving diagonally, the movement should be made slower
            diagonal = False
            if self.placement[0] != self.goal[0] and self.placement[1] != self.goal[1]:
                diagonal = True

            # calculate movement in directions
            if self.placement[0] > self.goal[0]:  # enemy is to the right of the goal
                if diagonal:
                    self.placement[0] -= speed - 1
                else:
                    if self.placement[0] - self.goal[0] < speed:
                        self.placement[0] -= 1
                    else:
                        self.placement[0] -= speed

            elif self.placement[0] < self.goal[0]:  # enemy is to the left of the goal
                if diagonal:
                    self.placement[0] += speed - 1
                else:
                    if self.goal[0] - self.placement[0] < speed:
                        self.placement[0] += 1
                    else:
                        self.placement[0] += speed

            if self.placement[1] > self.goal[1]:  # enemy is below the goal
                if diagonal:
                    self.placement[1] -= speed - 1
                else:
                    if self.placement[1] - self.goal[1] < speed:
                        self.placement[1] -= 1
                    else:
                        self.placement[1] -= speed

            if self.placement[1] < self.goal[1]:  # enemy is higher than the goal
                if diagonal:
                    self.placement[1] += speed - 1
                else:
                    if self.goal[1] - self.placement[1] < speed:
                        self.placement[1] += 1
                    else:
                        self.placement[1] += speed

    def update(self, player):
        self.goal = player.placement
        self.movement()
        game.map_screen1.blit(self.char.sprite,
                              (game.camera_x1 - self.placement[0], game.camera_y1 - self.placement[1]))
        game.map_screen2.blit(self.char.sprite,
                              (game.camera_x2 - self.placement[0], game.camera_y2 - self.placement[1]))


# OBJECTS

# player objects
pig_witch = Obj('Pig', 'pig0', cycle='LEFT')
hood_lizard = Obj('Lizard', 'lizard0', cycle='LEFT')
cat_clown = Obj('Cat', 'cat0', cycle='LEFT')

# other objects
pumpkin = Obj('Pumpkin', 'objectA0')

# PLAYERS
player_1 = Player(pig_witch, 1)
player_2 = Player(hood_lizard, 2)

# ENEMIES
enemy_test = Enemy(pumpkin, placement=[0, 0])

# ANIMATION cycles
# move left
pig_witch.add_cycle('LEFT', ['pig0', 'pig1'])
hood_lizard.add_cycle('LEFT', ['lizard0', 'lizard1'])
cat_clown.add_cycle('LEFT', ['cat0', 'cat1'])

# move right
pig_witch.add_cycle('RIGHT', ['pig2', 'pig3'])
hood_lizard.add_cycle('RIGHT', ['lizard2', 'lizard3'])
