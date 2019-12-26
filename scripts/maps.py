from objects import *
from random import choice, randint, sample


class Maps(object):
    all_maps = {}  # Dictionary of all saved maps
    second_layer = {}   # dictionary of saved maps' second layer

    tile_groups = {}

    def __init__(self):
        self.cur_map = None
        self.cur_name = None
        self.cur_size = None
        game.map_class = self

    def current_map(self, name):
        self.cur_map = self.all_maps[name][0]
        self.cur_name = name
        self.cur_size = self.all_maps[name][1]

    def new_tile_group(self, name, tiles, ratio=(3, 3), directions=None):
        if directions is not None:
            self.tile_groups[name] = [tiles, ratio, directions]
        else:
            self.tile_groups[name] = [tiles, ratio, [None]]

    def make_tile_group(self, tile_group, sprite_group):
        """take the predetermined order of things from one of the tile_groups directory and use it on any
        group of ground tiles"""
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

            # in general map_groups, the size (str(i[0/1])) is divided by 3 (or whatever the group ratio is)
            map_groups[str(i[0]) + ':' + str(i[1])] = [path, (i[0] * sprites.new_size * 3,
                                                              i[1] * sprites.new_size * 3)]

    def new_map(self, name, starting_spot):
        # size of the map
        size = (27, 27)
        ground_spr_group = 'ground' + choice(['A', 'B', 'C', 'D'])  # which ground tiles are used for this map

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

        # save exact positions to the game, so the characters can reset there
        game.start['x1'] = 0 - (start_pos[0] * sprites.new_size - (250 - sprites.new_size / 2))
        game.start['y1'] = 0 - (start_pos[1] * sprites.new_size - (250 - sprites.new_size / 2))
        game.start['x2'] = 0 - (start_pos[0] * sprites.new_size - (250 - sprites.new_size / 2))
        game.start['y2'] = 0 - (start_pos[1] * sprites.new_size - (250 - sprites.new_size / 2))

        # map base surface + layer 2
        the_map = pygame.Surface((size[0]*sprites.new_size, size[1]*sprites.new_size),
                                 pygame.HWSURFACE | pygame.SRCALPHA)
        layer_2 = pygame.Surface((size[0]*sprites.new_size, size[1]*sprites.new_size),
                                 pygame.HWSURFACE | pygame.SRCALPHA)

        # OBJECTS
        HardObj.all_hardobj.clear()
        object_amount = randint(45, 55)   # how many objects spawn in
        all_rand = [x for x in Obj.rand_pos]
        for o in all_rand:  # pick out snow map objects, and add or remove depending on if map is snow map
            if len(o) > 9:
                if o[-6:] == '(snow)' and ground_spr_group != 'groundC':
                    all_rand.remove(o)
                    # print 'removing snow item: '+o
                elif o[-9:] == '(no snow)' and ground_spr_group == 'groundC':
                    all_rand.remove(o)
                    # print 'removing non-snow item: '+o
        obj_to_choose_from = sample(set(all_rand), len(all_rand)/2)  # choose map-specific objects
        objects = {}
        second_layer = {}
        # determine position
        for i in range(object_amount):
            obj = Obj.all_obj[choice(obj_to_choose_from)]  # chosen object
            loop = True
            pos = (0, 0)
            while loop:
                # check if another object has the same position
                found = False
                pos = (sprites.new_size*randint(-size[0]+3+obj.tiles_right, -2),
                       sprites.new_size*randint(-size[1]+3, -2))
                for s in objects.values():
                    if pos == s.placement:
                        found = True
                if not found:
                    # if position is unique, continue
                    loop = False
            objects[pos] = HardObj(obj, placement=pos)

        # COLLECTIBLES
        item_amount = randint(5, 15)
        Collectible.all_collectibles = []

        # items to choose from
        choices = ['Eyenion', 'Eyenion', 'Mushroom', 'Mushroom', 'Mushroom', 'Monkey Paw', 'Eyenion', 'Mushroom',
                   'Monkey Paw']
        for key in game.keys.keys():
            if not game.keys[key]:
                choices.append('Keypiece ' + str(key))

        for i in range(item_amount):
            loop = True
            pos = (0, 0)
            while loop:
                # check if another object has the same position
                found = False
                pos = (sprites.new_size*randint(-size[0]+3, -2), sprites.new_size*randint(-size[1]+3, -2))
                for s in objects.values():
                    if pos == s.placement:
                        found = True
                if not found:
                    # if position is unique, continue
                    loop = False

            obj = choice(choices)
            if obj in ['Keypiece 1', 'Keypiece 2', 'Keypiece 3']:
                objects[pos] = Collectible(Obj.all_obj[obj], placement=pos, key=int(obj[-1]))
            else:
                objects[pos] = Collectible(Obj.all_obj[obj], placement=pos)

        # FINAL GATE  - only appears after key pieces have been collected
        if game.keys[1] and game.keys[2] and game.keys[3]:
            gate = Obj.all_obj['Main Gate 0']  # chosen object
            loop = True
            pos = (0, 0)
            while loop:
                # check if another object has the same position
                found = False
                pos = (sprites.new_size*randint(-size[0]+3+gate.tiles_right, -2),
                       sprites.new_size*randint(-size[1]+3, -2))
                for s in objects.values():
                    if pos == s.placement:
                        found = True
                if not found:
                    # if position is unique, continue
                    loop = False
            objects[pos] = Gate(gate, placement=pos)

        # CONTINUED objects
        # layer 1 and 2 objects are looped separately, so that layer 1 continuing objects can first cancel out any
        # other crossing objects layer 1.
        for c in Obj.cont_objs.keys():  # LOOP for layer 1 objects
            for h in objects.values():
                if Obj.cont_objs[c][0] == h.obj.name and Obj.cont_objs[c][2] == 1:
                    dirct = Obj.cont_objs[c][1]
                    pos = (h.placement[0] + dirct[0]*sprites.new_size,
                           h.placement[1] + dirct[1]*sprites.new_size)

                    objects[pos] = HardObj(Obj.all_obj[c], placement=pos)

        for c in Obj.cont_objs.keys():  # LOOP for layer 2 objects
            for h in objects.values():
                if Obj.cont_objs[c][0] == h.obj.name and Obj.cont_objs[c][2] == 2:
                    dirct = Obj.cont_objs[c][1]
                    pos = (h.placement[0] + dirct[0] * sprites.new_size,
                           h.placement[1] + dirct[1] * sprites.new_size)
                    second_layer[len(second_layer)] = [Obj.all_obj[c], (-pos[0], -pos[1])]

        # ENEMIES
        Enemy.all_enemies.clear()
        map_enemies = {}
        # make enemies appear more frequently if more keys are found
        if game.keys_total == 0:
            enemy_amount = randint(0, 3)
        elif game.keys_total == 1:
            enemy_amount = randint(3, 5)
        elif game.keys_total == 2:
            enemy_amount = randint(5, 7)
        else:
            enemy_amount = randint(7, 10)
        enemy_char = choice(enemy_objs.values())
        for e in range(enemy_amount):
            if starting_spot == 'down':
                pos = [sprites.new_size*randint(-size[0]+2, -1), sprites.new_size*randint(-size[1]+5, -1)]
            elif starting_spot == 'up':
                pos = [sprites.new_size * randint(-size[0] + 2, -1), sprites.new_size * randint(-size[1] + 2, -4)]
            elif starting_spot == 'left':
                pos = [sprites.new_size * randint(-size[0] + 2, -4), sprites.new_size * randint(-size[1] + 2, -1)]
            else:
                pos = [sprites.new_size * randint(-size[0] + 5, -1), sprites.new_size * randint(-size[1] + 2, -1)]
            map_enemies[e] = Enemy(enemy_char, placement=pos)

        # GROUNDS
        # the chosen ground tiles are moved to above
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

        if map_groups is not None:  # drawing map groups
            for x in map_groups.values():
                the_map.blit(self.make_tile_group(x[0], ground_spr_group), x[1])

        # draw second layer objects
        layer_order = sorted(second_layer.values(), key=lambda x: x[1][1])
        for i in layer_order:
            layer_2.blit(i[0].cur_sprite, i[1])

        # save map
        self.all_maps[name] = [the_map, size, map_enemies, objects, map_groups]
        self.second_layer[name] = layer_2
        Game.all_maps[name] = [the_map, size, map_enemies, objects, map_groups]
        Game.second_layer[name] = layer_2

    def load_map(self, name, starting_spot):
        print 'loading map...', name
        size = self.all_maps[name][1]
        self.current_map(name)

        # the place where the players start on the map
        if starting_spot == 'down':
            start_pos = (size[0] / 2, size[1] - 2)
        elif starting_spot == 'up':
            start_pos = (size[0] / 2, 1)
        elif starting_spot == 'left':
            start_pos = (1, size[1] / 2)
        else:
            start_pos = (size[0] - 2, size[1] / 2)

        # set cameras
        game.camera_x1 = 0 - (start_pos[0] * sprites.new_size - (250 - sprites.new_size / 2))
        game.camera_y1 = 0 - (start_pos[1] * sprites.new_size - (250 - sprites.new_size / 2))

        game.camera_x2 = 0 - (start_pos[0] * sprites.new_size - (250 - sprites.new_size / 2))
        game.camera_y2 = 0 - (start_pos[1] * sprites.new_size - (250 - sprites.new_size / 2))

    def map_update(self):
        # updating current map
        if self.cur_name != game.switch['cur_map']:
            self.new_map(game.switch['cur_map'], game.switch['start_point'])
            self.current_map(game.switch['cur_map'])
            pygame.mixer.Sound.play(game.sounds['exit'])

        # removing collected items
        for x in self.all_maps[game.switch["cur_map"]][3].keys():
            value = self.all_maps[game.switch["cur_map"]][3][x]
            if value.obj.name in Obj.collectibles and value not in Collectible.all_collectibles:
                self.all_maps[game.switch["cur_map"]][3].pop(x)

        # GAME BOUNDS / MOVING ONTO NEXT MAP
        if game.camera_x1 > 250 - game.sprite_size / 2 - game.sprite_size and\
                game.camera_x2 > 250 - game.sprite_size / 2 - game.sprite_size:
            n = randint(1, 7)
            game.fade_out = True
            game.waiting_commands['cur_map'] = n
            game.waiting_commands['start_point'] = 'right'

        elif game.camera_x1 < (self.all_maps[game.switch["cur_map"]][1][0] * game.sprite_size)*(-1) + 250\
                + game.sprite_size / 2 + game.sprite_size and game.camera_x2 < \
                (self.all_maps[game.switch["cur_map"]][1][0] * game.sprite_size)*(-1) + 250 + game.sprite_size / 2 \
                + game.sprite_size:
            n = randint(1, 10)
            game.fade_out = True
            game.waiting_commands['cur_map'] = n
            game.waiting_commands['start_point'] = 'left'
        if game.camera_y1 > 250 - game.sprite_size / 2 - game.sprite_size and \
                game.camera_y2 > 250 - game.sprite_size / 2 - game.sprite_size:
            n = randint(1, 10)
            game.fade_out = True
            game.waiting_commands['cur_map'] = n
            game.waiting_commands['start_point'] = 'down'
        elif game.camera_y1 < (self.all_maps[game.switch["cur_map"]][1][1] * game.sprite_size)*(-1) + 250\
                + game.sprite_size / 2 + game.sprite_size and game.camera_y1 < \
                (self.all_maps[game.switch["cur_map"]][1][1] * game.sprite_size)*(-1) + 250\
                + game.sprite_size / 2 + game.sprite_size:
            n = randint(1, 10)
            game.fade_out = True
            game.waiting_commands['cur_map'] = n
            game.waiting_commands['start_point'] = 'up'

        # Out of bounds
        # PLAYER 1
        if game.camera_x1 > 250 - game.sprite_size / 2:
            game.camera_x1 = 250 - game.sprite_size / 2
            if game.switch['play_mode'] == 'single':
                n = randint(1, 7)
                game.fade_out = True
                game.waiting_commands['cur_map'] = n
                game.waiting_commands['start_point'] = 'right'
            else:
                game.wait_for_player2 = True
        elif game.camera_x1 < (self.all_maps[game.switch["cur_map"]][1][0] * game.sprite_size)*(-1) + 250\
                + game.sprite_size / 2:
            game.camera_x1 = (self.all_maps[game.switch["cur_map"]][1][0] * game.sprite_size) * (-1) + 250\
                             + game.sprite_size / 2
            if game.switch['play_mode'] == 'single':
                n = randint(1, 7)
                game.fade_out = True
                game.waiting_commands['cur_map'] = n
                game.waiting_commands['start_point'] = 'left'
            else:
                game.wait_for_player2 = True
        if game.camera_y1 > 250 - game.sprite_size / 2:
            game.camera_y1 = 250 - game.sprite_size / 2
            if game.switch['play_mode'] == 'single':
                n = randint(1, 7)
                game.fade_out = True
                game.waiting_commands['cur_map'] = n
                game.waiting_commands['start_point'] = 'down'
            else:
                game.wait_for_player2 = True
        elif game.camera_y1 < (self.all_maps[game.switch["cur_map"]][1][1] * game.sprite_size)*(-1) + 250\
                + game.sprite_size / 2:
            game.camera_y1 = (self.all_maps[game.switch["cur_map"]][1][1] * game.sprite_size) * (-1) + 250\
                             + game.sprite_size / 2
            if game.switch['play_mode'] == 'single':
                n = randint(1, 7)
                game.fade_out = True
                game.waiting_commands['cur_map'] = n
                game.waiting_commands['start_point'] = 'up'
            else:
                game.wait_for_player2 = True
        # PLAYER 2
        if game.camera_x2 > 250 - game.sprite_size / 2:
            game.camera_x2 = 250 - game.sprite_size / 2
            game.wait_for_player1 = True
        elif game.camera_x2 < (self.all_maps[game.switch["cur_map"]][1][0] * game.sprite_size)*(-1) + 250\
                + game.sprite_size / 2:
            game.camera_x2 = (self.all_maps[game.switch["cur_map"]][1][0] * game.sprite_size) * (-1) + 250\
                             + game.sprite_size / 2
            game.wait_for_player1 = True
        if game.camera_y2 > 250 - game.sprite_size / 2:
            game.camera_y2 = 250 - game.sprite_size / 2
            game.wait_for_player1 = True
        elif game.camera_y2 < (self.all_maps[game.switch["cur_map"]][1][1] * game.sprite_size)*(-1) + 250\
                + game.sprite_size / 2:
            game.camera_y2 = (self.all_maps[game.switch["cur_map"]][1][1] * game.sprite_size) * (-1) + 250\
                             + game.sprite_size / 2
            game.wait_for_player1 = True

        # COLLISION with ground tiles and hard objects
        grounds = self.all_maps[game.switch["cur_map"]][4]  # the 'map groups' dictionary from the making of the map
        map_cols_1 = []  # in form = (x, y): [rect1, rect2...]
        map_cols_2 = []  # for player 2

        # Gate collision
        if Obj.gate is not None:
            map_cols_1.append(Obj.gate.collision1)
            map_cols_2.append(Obj.gate.collision2)

        # loop through tile groups, check which ones are nearby, then add individual tile's collision rects
        # into map_cols
        for i in HardObj.all_hardobj.values():
            map_cols_1.append(i.collision1)
            map_cols_2.append(i.collision2)

        for x in grounds.keys():
            pos = x.split(':')
            pos = [int(pos[0]), int(pos[1])]

            # PLAYER 1
            if abs(player_1.on_tile[0] - pos[0]*3) < 4 and abs(player_1.on_tile[1] - pos[1]*3) < 4:
                t_group = self.tile_groups[grounds[x][0]]
                tiles = t_group[0]
                ratio = t_group[1]
                a = 0  # tile index from tiles
                for row in range(ratio[1]):
                    for column in range(ratio[0]):
                        cur_tile = ((pos[0]*3+column)*sprites.new_size*-1, (pos[1]*3+row)*sprites.new_size*-1)
                        # map_cols_1[cur_tile] = []
                        for t in sprites.collision[tiles[a]]:
                            if t is not None:
                                map_cols_1.append(
                                    pygame.Rect(game.camera_x1 - (cur_tile[0] - t[0]),
                                                game.camera_y1 - (cur_tile[1] - t[1]), t[2], t[3]))
                        a += 1
            # PLAYER 2
            if abs(player_2.on_tile[0] - pos[0] * 3) < 4 and abs(player_2.on_tile[1] - pos[1] * 3) < 4:
                t_group = self.tile_groups[grounds[x][0]]
                tiles = t_group[0]
                ratio = t_group[1]
                a = 0  # tile index from tiles
                for row in range(ratio[1]):
                    for column in range(ratio[0]):
                        cur_tile = (
                            (pos[0] * 3 + column) * sprites.new_size * -1, (pos[1] * 3 + row) * sprites.new_size * -1)
                        # map_cols_2[cur_tile] = []
                        for t in sprites.collision[tiles[a]]:
                            if t is not None:
                                map_cols_2.append(
                                    pygame.Rect(game.camera_x2 - (cur_tile[0] - t[0]),
                                                game.camera_y2 - (cur_tile[1] - t[1]), t[2], t[3]))
                        a += 1

        # check if PLAYER 1 collides
        for i in map_cols_1:
            # to draw collision blocks:
            # pygame.draw.rect(game.map_screen1, (0, 0, 0), i)
            if i is not None:
                if player_1.collision.colliderect(i):
                    if game.camera_1_move[0] != 0:  # moving to left or right
                        game.camera_x1 -= game.camera_1_move[0]
                        game.camera_1_move[0] = 0
                    if game.camera_1_move[1] != 0:  # moving up or down
                        game.camera_y1 -= game.camera_1_move[1]
                        game.camera_1_move[1] = 0

        # check if PLAYER 2 collides
        for i in map_cols_2:
            # to draw collision blocks:
            # pygame.draw.rect(game.map_screen1, (0, 0, 0), i)
            if i is not None:
                if player_2.collision.colliderect(i):
                    if game.camera_2_move[0] != 0:  # moving to left or right
                        game.camera_x2 -= game.camera_2_move[0]
                        game.camera_2_move[0] = 0
                    if game.camera_2_move[1] != 0:  # moving up or down
                        game.camera_y2 -= game.camera_2_move[1]
                        game.camera_2_move[1] = 0


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
