from sprites import *


class Obj(object):
    def __init__(self, name, base_sprite=None, constant_anim=False, cycle=None):
        self.name = name
        self.sprite = sprites.big_sprites[base_sprite]
        self.cur_sprite = self.sprite
        self.collision = None

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
    def __init__(self, character):
        self.char = character  # of Obj -type
        self.items = {}

    def update(self):
        pass


# OBJECTS

# players
pig_witch = Obj('Pig', 'playerSPR0')
hood_lizard = Obj('Lizard', 'playerSPR1')
cat_clown = Obj('Cat', 'playerSPR2')

# cycles
pig_witch.add_cycle('LEFT', ['playerSPR0', 'playerSPR3'])
hood_lizard.add_cycle('LEFT', ['playerSPR1', 'playerSPR4'])
cat_clown.add_cycle('LEFT', ['playerSPR2', 'playerSPR5'])
