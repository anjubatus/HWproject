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
        game.cur_map = name
        self.cur_name = name
        self.cur_size = self.all_maps[name][1]

    def new_tile_group(self, name, tiles, ratio=(3, 3), directions=None):
        if directions is not None:
            self.tile_groups[name] = [tiles, ratio, directions]
        else:
            self.tile_groups[name] = [tiles, ratio, [None]]

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

    def randomize_path(self, map_groups, positions):
        for i in positions:
            must_dir = []  # direction must be included
            no_dir = []  # direction can't be included

            # Checking nearby tiles
            if str(i[0]) + ':' + str(i[1] - 1) in map_groups.keys():
                # one tile above directions
                tile_up = self.tile_groups[map_groups[str(i[0]) + ':' + str(i[1] - 1)][0]][2]
                if 'down' in tile_up:
                    must_dir.append('up')
                else:
                    no_dir.append('up')
            if str(i[0]) + ':' + str(i[1] + 1) in map_groups.keys():
                # one tile below directions
                tile_down = self.tile_groups[map_groups[str(i[0]) + ':' + str(i[1] + 1)][0]][2]
                if 'up' in tile_down:
                    must_dir.append('down')
                else:
                    no_dir.append('down')
            if str(i[0] - 1) + ':' + str(i[1]) in map_groups.keys():
                # one tile to the left directions
                tile_left = self.tile_groups[map_groups[str(i[0] - 1) + ':' + str(i[1])][0]][2]
                if 'right' in tile_left:
                    must_dir.append('left')
                else:
                    no_dir.append('left')
            if str(i[0] + 1) + ':' + str(i[1]) in map_groups.keys():
                # one tile to the right directions
                tile_right = self.tile_groups[map_groups[str(i[0] + 1) + ':' + str(i[1])][0]][2]
                if 'left' in tile_right:
                    must_dir.append('right')
                else:
                    no_dir.append('right')

            # deciding options
            avail = []
            for x in self.tile_groups.keys():
                if set(must_dir).issubset(self.tile_groups[x][2]) and len(
                        set(no_dir).intersection(self.tile_groups[x][2])) == 0:
                    avail.append(x)

            # choosing
            path = choice(avail)
            map_groups[str(i[0]) + ':' + str(i[1])] = [path, (i[0] * sprites.new_size * 3,
                                                              i[1] * sprites.new_size * 3)]

    def new_map(self, name, starting_spot):
        # size of the map
        size = (choice([21, 27]), choice([21, 27]))

        # the place where the players start on the map
        if starting_spot == 'down':
            start_pos = (size[0]/2, size[1] - 2)
        elif starting_spot == 'up':
            start_pos = (size[0]/2, 1)
        elif starting_spot == 'left':
            start_pos = (1, size[1]/2)
        else:
            start_pos = (size[0] - 2, size[1]/2)

        # set cameras
        game.camera_x1 = 0 - (start_pos[0] * sprites.new_size - (250 - sprites.new_size / 2))
        game.camera_y1 = 0 - (start_pos[1] * sprites.new_size - (250 - sprites.new_size / 2))

        game.camera_x2 = 0 - (start_pos[0] * sprites.new_size - (250 - sprites.new_size / 2))
        game.camera_y2 = 0 - (start_pos[1] * sprites.new_size - (250 - sprites.new_size / 2))

        # map base surface + layer 2
        the_map = pygame.Surface((size[0]*sprites.new_size, size[1]*sprites.new_size),
                                 pygame.HWSURFACE | pygame.SRCALPHA)
        layer_2 = pygame.Surface((size[0]*sprites.new_size, size[1]*sprites.new_size),
                                 pygame.HWSURFACE | pygame.SRCALPHA)

        # OBJECTS
        object_amount = randint(10, 20)   # how many objects spawn in
        objects = {}
        for i in range(object_amount):
            loop = True
            pos = (0, 0)
            while loop:
                # check if another object has the same position
                found = False
                pos = [sprites.new_size*randint(-size[0]+1, 0), sprites.new_size*randint(-size[1]+1, 0)]
                for s in objects.values():
                    if pos == s.placement:
                        found = True
                if not found:
                    # if position is unique, continue
                    loop = False
            # group = choice(['objectB', 'misc'])
            obj = choice(Obj.hard_obj)
            # objects[i] = [group + str(randint(0, sprites.group_sizes[group]-1)), pos]
            objects[i] = HardObj(Obj.all_obj[obj], placement=pos)

        # ENEMIES - test version TODO real enemies
        Enemy.all_enemies.clear()
        enemy_test = {1: Enemy(pumpkin, placement=[sprites.new_size*randint(-size[0]+1, 0),
                                                   sprites.new_size*randint(-size[1]+1, 0)]),
                      2: Enemy(pumpkin, placement=[sprites.new_size*randint(-size[0]+1, 0),
                                                   sprites.new_size*randint(-size[1]+1, 0)])}

        # GROUNDS
        ground_spr_group = 'ground' + choice(['A', 'B', 'C'])
        map_groups = {}

        # pre-determined borders of the map
        for x in range(size[0] / 3):
            for y in range(size[1] / 3):
                if y == 0 or y == size[1] / 3 - 1:  # length-wise
                    if x != size[0] / 3 / 2:
                        map_groups[str(x)+':'+str(y)] = ['grass', (x * sprites.new_size * 3, y * sprites.new_size * 3)]
                        # num += 1
                    else:
                        map_groups[str(x)+':'+str(y)] = ['updown', (x * sprites.new_size * 3, y * sprites.new_size * 3)]
                        # num += 1
                if x == 0 or x == size[0] / 3 - 1:  # height-wise
                    if y != size[1] / 3 / 2:
                        map_groups[str(x)+':'+str(y)] = ['grass', (x * sprites.new_size * 3, y * sprites.new_size * 3)]
                        # num += 1
                    else:
                        map_groups[str(x)+':'+str(y)] = ['leftright', (x * sprites.new_size * 3,
                                                                       y * sprites.new_size * 3)]
                        # num += 1

        # RANDOMIZED PATHWAYS
        if len(self.tile_groups) > 0:
            """map_groups = {}
            # path ways
            for i in range(randint(3, (size[0]/3)*(size[1]/3))/3):
                loop = True
                pos = (0, 0)
                while loop:
                    # check if another object has the same position
                    found = False
                    pos = (randint(1, (size[0]/3)-2) * sprites.new_size*3,
                           randint(1, (size[1]/3)-2) * sprites.new_size*3)
                    for s in map_groups.values():
                        if pos == s[1]:
                            found = True
                    if not found:
                        # if position is unique, continue
                        loop = False

                map_groups[i] = [choice(self.tile_groups.keys()), pos]"""  # old randomized pathways

            # new randomized pathways - first round
            for i in [(size[0]/3/2, 1), (size[0]/3/2, size[1]/3-2), (1, size[1]/3/2), (size[0]/3-2, size[1]/3/2)]:
                path = ''
                if str(i[0])+':'+str(i[1]-1) in map_groups.keys():
                    path = choice(['updown', 'crossup', 'deadup', 'crossleft', 'crossright', 'cross',
                                   'upleft', 'upright'])
                elif str(i[0]-1)+':'+str(i[1]) in map_groups.keys():
                    path = choice(['leftright', 'crossup', 'crossdown', 'crossleft', 'deadleft', 'cross',
                                   'upleft', 'downleft'])
                elif str(i[0])+':'+str(i[1]+1) in map_groups.keys():
                    path = choice(['updown', 'crossdown', 'crossleft', 'crossright', 'deaddown', 'cross',
                                   'downleft', 'downright'])
                elif str(i[0]+1)+':'+str(i[1]) in map_groups.keys():
                    path = choice(['leftright', 'crossdown', 'crossup', 'crossright', 'deadright', 'cross',
                                   'downright', 'upright'])
                map_groups[str(i[0]) + ':' + str(i[1])] = [path, (i[0] * sprites.new_size * 3,
                                                                  i[1] * sprites.new_size * 3)]

            # second round in randomized pathways
            secondary = [(size[0]/3/2-1, 1), (size[0]/3/2, 2), (size[0]/3/2+1, 1), (size[0]/3/2-1, size[1]/3-2),
                         (size[0]/3/2, size[1]/3-3), (size[0]/3/2+1, size[1]/3-2), (1, size[1]/3/2-1),
                         (1, size[1]/3/2+1), (2, size[1]/3/2), (size[0]/3-3, size[1]/3/2),
                         (size[0]/3-2, size[1]/3/2-1), (size[0]/3-2, size[1]/3/2+1)]
            self.randomize_path(map_groups, secondary)

            # third and last round
            last = []
            for x in range(1, (size[0]/3)-1):
                for y in range(1, (size[1]/3)-1):
                    if str(x)+':'+str(y) not in map_groups.keys():
                        last.append((x, y))
            self.randomize_path(map_groups, last)

            # grass
            for x in range(1, (size[0]/3)-1):
                for y in range(1, (size[1]/3)-1):
                    found = False
                    # check if a pathway has the same position
                    pos = (x*sprites.new_size*3, y*sprites.new_size*3)
                    for s in map_groups.values():
                        if pos == s[1]:
                            found = True
                    if not found:
                        map_groups[str(x)+':'+str(y)] = ['grass', pos]

        if map_groups is not None:  # test version
            for x in map_groups.values():
                the_map.blit(self.make_tile_group(x[0], ground_spr_group), x[1])

        # objects (test version)
        """for x in objects.values():
            layer_2.blit(sprites.big_sprites[x[0]], x[1])"""

        # save map
        self.all_maps[name] = [the_map, size, enemy_test, objects]
        self.second_layer[name] = layer_2
        Game.all_maps[name] = [the_map, size, enemy_test, objects]
        Game.second_layer[name] = layer_2

    def load_map(self, name, starting_spot):
        pass  # TODO load maps

    def map_update(self):
        # GAME BOUNDS / MOVING ONTO NEXT MAP
        if game.camera_x1 > 250 - game.sprite_size / 2:
            # game.camera_x1 = 250 - game.sprite_size / 2
            n = randint(1, 10)
            self.new_map(n, 'right')
            self.current_map(n)
        elif game.camera_x1 < (self.all_maps[game.cur_map][1][0] * game.sprite_size)*(-1) + 250 + game.sprite_size / 2:
            # game.camera_x1 = (self.all_maps[game.cur_map][1][0] * game.sprite_size)*(-1) + 250 + game.sprite_size / 2
            n = randint(1, 10)
            self.new_map(n, 'left')
            self.current_map(n)
        if game.camera_y1 > 250 - game.sprite_size / 2:
            # game.camera_y1 = 250 - game.sprite_size / 2
            n = randint(1, 10)
            self.new_map(n, 'down')
            self.current_map(n)
        elif game.camera_y1 < (self.all_maps[game.cur_map][1][1] * game.sprite_size)*(-1) + 250 + game.sprite_size / 2:
            # game.camera_y1 = (self.all_maps[game.cur_map][1][1] * game.sprite_size)*(-1) + 250 + game.sprite_size / 2
            n = randint(1, 10)
            self.new_map(n, 'up')
            self.current_map(n)

        if game.camera_x2 > 250 - game.sprite_size / 2:
            game.camera_x2 = 250 - game.sprite_size / 2
        elif game.camera_x2 < (self.all_maps[game.cur_map][1][0] * game.sprite_size)*(-1) + 250 + game.sprite_size / 2:
            game.camera_x2 = (self.all_maps[game.cur_map][1][0] * game.sprite_size) * (-1) + 250 + game.sprite_size / 2
        if game.camera_y2 > 250 - game.sprite_size / 2:
            game.camera_y2 = 250 - game.sprite_size / 2
        elif game.camera_y2 < (self.all_maps[game.cur_map][1][1] * game.sprite_size)*(-1) + 250 + game.sprite_size / 2:
            game.camera_y2 = (self.all_maps[game.cur_map][1][1] * game.sprite_size) * (-1) + 250 + game.sprite_size / 2


# MAPS CLASS OBJECT
maps = Maps()

# TILE GROUPS - pathways
maps.new_tile_group('updown', [3, 4, 13, 3, 4, 13, 3, 4, 13], directions=['up', 'down'])
maps.new_tile_group('leftright', [1, 1, 1, 4, 4, 4, 9, 9, 9], directions=['left', 'right'])

maps.new_tile_group('crossleft', [2, 4, 13, 4, 4, 13, 11, 4, 13], directions=['up', 'down', 'left'])
maps.new_tile_group('crossright', [3, 4, 10, 3, 4, 4, 3, 4, 12], directions=['up', 'down', 'right'])
maps.new_tile_group('crossup', [2, 4, 10, 4, 4, 4, 9, 9, 9], directions=['up', 'left', 'right'])
maps.new_tile_group('crossdown', [1, 1, 1, 4, 4, 4, 11, 4, 12], directions=['left', 'right', 'down'])
maps.new_tile_group('cross', [2, 4, 10, 4, 4, 4, 11, 4, 12], directions=['up', 'down', 'left', 'right'])

maps.new_tile_group('upleft', [2, 4, 13, 4, 4, 13, 9, 9, 8], directions=['up', 'left'])
maps.new_tile_group('upright', [3, 4, 10, 3, 4, 4, 7, 9, 9], directions=['up', 'right'])
maps.new_tile_group('downleft', [1, 1, 6, 4, 4, 13, 11, 4, 13], directions=['left', 'down'])
maps.new_tile_group('downright', [0, 1, 1, 3, 4, 4, 3, 4, 12], directions=['right', 'down'])

maps.new_tile_group('deadup', [3, 4, 13, 7, 9, 8, 5, 5, 5], directions=['up'])
maps.new_tile_group('deaddown', [5, 5, 5, 0, 1, 6, 3, 4, 13], directions=['down'])
maps.new_tile_group('deadright', [5, 0, 1, 5, 3, 4, 5, 7, 9], directions=['right'])
maps.new_tile_group('deadleft', [1, 6, 5, 4, 13, 5, 9, 8, 5], directions=['left'])

# grass
maps.new_tile_group('grass', [5, 5, 5, 5, 5, 5, 5, 5, 5])
maps.new_tile_group('grass1', [5, 5, 5, 5, 5, 5, 5, 5, 5])
maps.new_tile_group('grass2', [5, 5, 5, 5, 5, 5, 5, 5, 5])
maps.new_tile_group('grass3', [5, 5, 5, 5, 5, 5, 5, 5, 5])
