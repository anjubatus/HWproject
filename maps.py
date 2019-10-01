from sprites import *
from random import choice, randint


class Maps(object):
    all_maps = {}  # Dictionary of all saved maps
    map_tilesets = {}

    def __init__(self):
        self.cur_map = None
        self.cur_name = None
        self.cur_size = None

    def current_map(self, name):
        self.cur_map = self.all_maps[name][0]
        self.cur_name = name
        self.cur_size = self.all_maps[name][1]

    def new_tileset(self):
        pass

    def new_map(self, name):
        size = (randint(10, 25), randint(10, 25))  # one integer means one tile
        the_map = pygame.Surface((size[0]*sprites.new_size, size[1]*sprites.new_size),
                                 pygame.HWSURFACE | pygame.SRCALPHA)

        # test tiles here
        for x in range(size[0]):
            for y in range(size[1]):
                rand_tile = choice(['0', '1', '2', '3', '4', '4', '4', '5', '5'])
                the_map.blit(sprites.big_sprites['groundA'+rand_tile], (x*sprites.new_size, y*sprites.new_size))

        # save map
        self.all_maps[name] = [the_map, size]


# MAPS CLASS OBJECT
maps = Maps()