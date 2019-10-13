from objects import *
from random import choice, randint


class Maps(object):
    all_maps = {}  # Dictionary of all saved maps
    second_layer = {}   # dictionary of saved maps' second layer

    tile_groups = {}
    # tile-groups currently:
    # updown, leftright
    # crossleft, crossright, crossup, crossdown, cross
    # upleft, upright, downleft, downright
    # deadup, deaddown, deadright, deadleft  (direction means which way is still open)

    def __init__(self):
        self.cur_map = None
        self.cur_name = None
        self.cur_size = None

    def current_map(self, name):
        self.cur_map = self.all_maps[name][0]
        self.cur_name = name
        self.cur_size = self.all_maps[name][1]

    def new_tile_group(self, name, tiles, ratio=(3, 3)):
        self.tile_groups[name] = [tiles, ratio]

    def make_tile_group(self, tile_group, sprite_group):
        # take the predetermined order of things from one of the tile_groups directory and use it on any
        # group of ground tiles
        t_g = self.tile_groups[tile_group]   # [0] = list of tiles, [1] = ratio (of form (x, y))
        new_surf = pygame.Surface((t_g[1][0]*sprites.new_size, t_g[1][1]*sprites.new_size),
                                  pygame.HWSURFACE | pygame.SRCALPHA)
        row = 0
        column = 0
        for x in range(len(t_g[0])):
            # add tiles to the new surface in order
            new_surf.blit(sprites.big_sprites[sprite_group+str(t_g[0][x])],
                          (column*sprites.new_size, row*sprites.new_size))
            column += 1
            if column >= t_g[1][0]:
                row += 1
                column = 0

        # return surface
        return new_surf

    def new_map(self, name):
        size = (choice([15, 21, 27]), choice([15, 21, 27]))  # one integer means one tile

        # set cameras
        game.camera_x1 = 0 - (size[0] * sprites.new_size / 2 - (250 - sprites.new_size / 2))
        game.camera_y1 = 0 - ((size[1] - 1) * sprites.new_size - (250 - sprites.new_size / 2))

        game.camera_x2 = 0 - (size[0] * sprites.new_size / 2 - (250 - sprites.new_size / 2))
        game.camera_y2 = 0 - ((size[1] - 1) * sprites.new_size - (250 - sprites.new_size / 2))

        # map base surface + layer 2
        the_map = pygame.Surface((size[0]*sprites.new_size, size[1]*sprites.new_size),
                                 pygame.HWSURFACE | pygame.SRCALPHA)
        layer_2 = pygame.Surface((size[0]*sprites.new_size, size[1]*sprites.new_size),
                                 pygame.HWSURFACE | pygame.SRCALPHA)

        # objects
        object_amount = randint(10, 20)   # how many objects spawn in
        objects = {}
        for i in range(object_amount):
            loop = True
            pos = (0, 0)
            while loop:
                # check if another object has the same position
                found = False
                pos = (randint(0, size[0])*sprites.new_size, randint(0, size[1])*sprites.new_size)
                for s in objects.values():
                    if pos == s[1]:
                        found = True
                if not found:
                    # if position is unique, continue
                    loop = False
            group = choice(['A', 'B'])
            objects[i] = ['object' + group + str(randint(0, sprites.group_sizes['object'+group]-1)), pos]

        # enemies - test version
        enemy_test = {1: Enemy(pumpkin, placement=[sprites.new_size*randint(-size[0]+1, 0),
                                                   sprites.new_size*randint(-size[1]+1, 0)]),
                      2: Enemy(pumpkin, placement=[0, 0])}

        # ground tile groups
        ground_spr_group = 'ground' + choice(['A', 'B'])
        map_groups = None
        if len(self.tile_groups) > 0:
            map_groups = {}
            for i in range(randint(5, (size[0]/3)*(size[1]/3))-4):
                loop = True
                pos = (0, 0)
                while loop:
                    # check if another object has the same position
                    found = False
                    pos = (randint(0, (size[0]/3)-1) * sprites.new_size*3,
                           randint(0, (size[1]/3)-1) * sprites.new_size*3)
                    for s in map_groups.values():
                        if pos == s[1]:
                            found = True
                    if not found:
                        # if position is unique, continue
                        loop = False

                map_groups[i] = [choice(self.tile_groups.keys()), pos]

        # ground tiles (test version)
        for x in range(size[0]):
            for y in range(size[1]):
                # in case the ground tiles are wanted to be entirely randomized:
                """ground_tiles = 0
                for i in sprites.sprites.keys():
                    if i[:7] == 'groundA':
                        ground_tiles += 1
                rand_tile = str(randint(0, ground_tiles-1))
                the_map.blit(sprites.big_sprites['groundA'+rand_tile], (x*sprites.new_size, y*sprites.new_size))"""
                # a bas emap of pure grass tiles
                the_map.blit(sprites.big_sprites[ground_spr_group + '5'],
                             (x * sprites.new_size, y * sprites.new_size))
        if map_groups is not None:
            for x in map_groups.values():
                # print 'group blit!', x[1]
                the_map.blit(self.make_tile_group(x[0], ground_spr_group), x[1])

        # objects (test version)
        for x in objects.values():
            # print 'object blit!'
            layer_2.blit(sprites.big_sprites[x[0]], x[1])

        # save map
        self.all_maps[name] = [the_map, size, enemy_test]
        self.second_layer[name] = layer_2
        Game.all_maps[name] = [the_map, size, enemy_test]
        Game.second_layer[name] = layer_2


# MAPS CLASS OBJECT
maps = Maps()

# TILE GROUPS
maps.new_tile_group('updown', [3, 4, 13, 3, 4, 13, 3, 4, 13])
maps.new_tile_group('leftright', [1, 1, 1, 4, 4, 4, 9, 9, 9])

maps.new_tile_group('crossleft', [2, 4, 13, 4, 4, 13, 11, 4, 13])
maps.new_tile_group('crossright', [3, 4, 10, 3, 4, 4, 3, 4, 12])
maps.new_tile_group('crossup', [2, 4, 10, 4, 4, 4, 9, 9, 9])
maps.new_tile_group('crossdown', [1, 1, 1, 4, 4, 4, 11, 4, 12])
maps.new_tile_group('cross', [2, 4, 10, 4, 4, 4, 11, 4, 12])

maps.new_tile_group('upleft', [2, 4, 13, 4, 4, 13, 9, 9, 8])
maps.new_tile_group('upright', [3, 4, 10, 3, 4, 4, 7, 9, 9])
maps.new_tile_group('downleft', [1, 1, 6, 4, 4, 13, 11, 4, 13])
maps.new_tile_group('downright', [0, 1, 1, 3, 4, 4, 3, 4, 12])

maps.new_tile_group('deadup', [3, 4, 13, 7, 9, 8, 5, 5, 5])
maps.new_tile_group('deaddown', [5, 5, 5, 0, 1, 6, 3, 4, 13])
maps.new_tile_group('deadright', [5, 0, 1, 5, 3, 4, 5, 7, 9])
maps.new_tile_group('deadleft', [1, 6, 5, 4, 13, 5, 9, 8, 5])
