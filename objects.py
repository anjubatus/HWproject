from sprites import *


class Obj(object):
    def __init__(self, name, base_sprite=None, constant_anim=False, cycle=None):
        self.name = name
        self.sprite = sprites.big_sprites[base_sprite]
        self.collision = None
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

    def update(self):
        if self.number == 1:
            dirct = game.p1_move
        else:
            dirct = game.p2_move
        if dirct is not None and dirct in self.char.cycles.keys():
            self.char.cur_cycle = dirct
            self.char.work_cycle(dirct)
        else:
            self.char.cur_sprite = sprites.big_sprites[self.char.cycles[self.char.cur_cycle][1][0]]


# OBJECTS

# player objects
pig_witch = Obj('Pig', 'pig0', cycle='LEFT')
hood_lizard = Obj('Lizard', 'lizard0', cycle='LEFT')
cat_clown = Obj('Cat', 'cat0', cycle='LEFT')

# cycles
# move left
pig_witch.add_cycle('LEFT', ['pig0', 'pig1'])
hood_lizard.add_cycle('LEFT', ['lizard0', 'lizard1'])
cat_clown.add_cycle('LEFT', ['cat0', 'cat1'])

# move right
pig_witch.add_cycle('RIGHT', ['pig2', 'pig3'])
hood_lizard.add_cycle('RIGHT', ['lizard2', 'lizard3'])


# PLAYERS
player_1 = Player(pig_witch, 1)
player_2 = Player(hood_lizard, 2)
