from game_essentials import *


class Sprites(object):
    def __init__(self, original_size, new_size=None):
        self.size = original_size  # size of a single original sprite in a spritesheet
        if new_size is None:
            self.new_size = self.size*2
            Game.sprite_size = self.size*2
        else:
            self.new_size = new_size  # size that the sprites will be transformed to as bigger sprites
            Game.sprite_size = new_size
        self.spritesheets = {}
        self.images = {}
        self.groups = {}
        self.group_sizes = {}
        self.sprites = {}
        self.big_sprites = {}
        self.size_sprites = {}

        self.cycles = {}  # for animation; includes counter for cur. frame  'name': [counter, [frames]]

        self.collision = {}  # in form: sprite name: [(x, y, x1, x2)]

    def spritesheet(self, a_file, name):
        self.spritesheets[name] = pygame.image.load(a_file)

    def image(self, a_file, name):
        self.images[name] = pygame.image.load(a_file)

    def add_size_sprite(self, sprite_name, size_x, size_y):  # add sprites with unique proportions
        self.size_sprites[sprite_name] = pygame.transform.scale(self.sprites[sprite_name],
                                                                (size_x, size_y))

    def find_sprite(self, group_name, x, y):
        # find sprites from a group
        # pixels will be calculated automatically, so for x and y, just use 0, 1, 2, 3 etc.
        new_sprite = pygame.Surface((self.size, self.size), pygame.HWSURFACE | pygame.SRCALPHA)
        new_sprite.blit(self.groups[group_name], (0, 0),
                        (x*self.size, y*self.size, (x+1)*self.size, (y+1)*self.size))
        return new_sprite

    def add_collision(self, name, *rects):
        self.collision[name] = []
        for x in rects:
            self.collision[name].append(x)

    def make_group(self, spritesheet, pos, name, sprites_x=1, sprites_y=1, size=None):  # pos = ex. (2, 3), no single pixels
        # divide sprites on a sprite-sheet into groups of sprites that are easily accessible
        self.group_sizes[name] = sprites_x * sprites_y

        # set size
        if size is None:
            size = self.size

        # making the group
        new_group = pygame.Surface((size*sprites_x, size*sprites_y), pygame.HWSURFACE | pygame.SRCALPHA)
        new_group.blit(self.spritesheets[spritesheet], (0, 0),
                       (pos[0]*size, pos[1]*size,
                        (pos[0]+sprites_x)*size, (pos[1]+sprites_y)*size))
        self.groups[name] = new_group

        # splitting group into singular sprites and storing in self.sprites, also making bigger sprites
        x_spr = 0
        y_spr = 0
        for x in range(sprites_x * sprites_y):
            new_sprite = pygame.Surface((size, size), pygame.HWSURFACE | pygame.SRCALPHA)
            new_sprite.blit(new_group, (0, 0), (x_spr*size, y_spr*size,
                                                (x_spr+1)*size, (y_spr+1)*size))
            self.sprites[name+str(x)] = new_sprite
            if size == self.size:
                self.big_sprites[name+str(x)] = pygame.transform.scale(new_sprite, (sprites.new_size, sprites.new_size))
            else:
                self.big_sprites[name + str(x)] = pygame.transform.scale(new_sprite, (size*2, size*2))
            x_spr += 1
            if x_spr == sprites_x:
                x_spr = 0
                y_spr += 1
        # sprites can be found in self.sprites by calling their key aka group name + number

    def flip_tiles(self, group_name, tiles, flipped_how, starting_number):
        # parameters: which group name the flipped tiles will be added to (in sprites only); number is enough
        # list of tile names, and the starting number which is whatever number comes after the last
        # original group tile
        # flipped_how is a list as long as tiles, to tell in which ways you want the specific tile to be flipped
        for x in range(len(tiles)):
            new_tile = self.sprites[group_name+str(tiles[x])]
            if flipped_how[x] == 'hor':   # horizontally
                new_tile = pygame.transform.flip(new_tile, True, False)
                self.sprites[group_name+str(starting_number)] = new_tile
                self.big_sprites[group_name + str(starting_number)] = pygame.transform.scale(new_tile,
                                                                            (self.new_size, self.new_size))
                starting_number += 1

            if flipped_how[x] == 'ver':   # vertically
                new_tile = pygame.transform.flip(new_tile, False, True)
                self.sprites[group_name+str(starting_number)] = new_tile
                self.big_sprites[group_name + str(starting_number)] = pygame.transform.scale(new_tile,
                                                                            (self.new_size, self.new_size))
                starting_number += 1

            if flipped_how[x] == 'both':   # both, at the same time
                new_tile = pygame.transform.flip(new_tile, True, True)
                self.sprites[group_name+str(starting_number)] = new_tile
                self.big_sprites[group_name + str(starting_number)] = pygame.transform.scale(new_tile,
                                                                            (self.new_size, self.new_size))
                starting_number += 1

        # update group size
        self.group_sizes[group_name] += len(tiles)


sprites = Sprites(32)

# upload spritesheets
sprites.spritesheet('sprites/tiles1.png', 'tilesA')
sprites.spritesheet('sprites/tilesfinal3.png', 'tilesB')
sprites.spritesheet('sprites/tilesfinal4.png', 'tilesC')
sprites.spritesheet('sprites/player_spr.png', 'playerSPR')  # player sprite-sheet can be called with playerSPR
sprites.spritesheet('sprites/frames(1).png', 'frames')
sprites.spritesheet('sprites/enemies.png', 'enemies0')
sprites.spritesheet('sprites/enemies1.png', 'enemies1')

# PLAYER SPRITES
sprites.make_group('playerSPR', (0, 0), 'pig', sprites_y=12)
sprites.make_group('playerSPR', (1, 0), 'lizard', sprites_y=12)
sprites.make_group('playerSPR', (2, 0), 'cat', sprites_y=12)
sprites.make_group('playerSPR', (3, 0), 'shadow')
# big player sprites
sprites.add_size_sprite('pig0', sprites.size*5, sprites.size*5)
sprites.add_size_sprite('cat0', sprites.size*5, sprites.size*5)
sprites.add_size_sprite('lizard0', sprites.size*5, sprites.size*5)

# ENEMIES
sprites.make_group('enemies0', (0, 0), 'ghost', sprites_y=4)
sprites.make_group('enemies1', (0, 0), 'hatleg', sprites_y=12)
sprites.make_group('enemies1', (1, 0), 'crawler', sprites_y=12)
sprites.make_group('enemies1', (2, 0), 'bat', sprites_y=8)

# TILES

# GATES
sprites.make_group('tilesC', (12, 0), 'gate', sprites_x=4, sprites_y=2)
sprites.flip_tiles('gate', [0, 4], ['hor', 'hor'], 8)

# GROUNDS
sprites.make_group('tilesA', (0, 0), 'groundA', sprites_x=3, sprites_y=2)
sprites.make_group('tilesA', (3, 0), 'groundB', sprites_x=3, sprites_y=2)
sprites.make_group('tilesC', (0, 0), 'groundC', sprites_x=3, sprites_y=2)
sprites.make_group('tilesC', (0, 2), 'groundD', sprites_x=3, sprites_y=2)

for l in ['A', 'B', 'C', 'D']:
    sprites.flip_tiles('ground'+l, [0, 0, 0, 1, 2, 2, 2, 3],
                       ['hor', 'ver', 'both', 'ver', 'hor', 'ver', 'both', 'hor'], 6)

# ground collision
sprites.add_collision(0, (0, 0, sprites.new_size, 10), (0, 10, 10, sprites.new_size-10))
sprites.add_collision(1, (0, 0, sprites.new_size, 10))
sprites.add_collision(2, (0, 0, 10, 10))
sprites.add_collision(3, (0, 0, 10, sprites.new_size))
sprites.add_collision(4)
sprites.add_collision(5, (0, 0, sprites.new_size, sprites.new_size))
sprites.add_collision(6, (0, 0, sprites.new_size, 10),
                      (sprites.new_size - 10, 10, 10, sprites.new_size-10))
sprites.add_collision(7, (0, 0, 10, sprites.new_size), (10, sprites.new_size-10, sprites.new_size-10, 10))
sprites.add_collision(8, (sprites.new_size - 10, 0, 10, sprites.new_size),
                      (0, sprites.new_size-10, sprites.new_size-10, 10))
sprites.add_collision(9, (0, sprites.new_size-10, sprites.new_size, 10))
sprites.add_collision(10, (sprites.new_size-10, 0, 10, 10))
sprites.add_collision(11, (0, sprites.new_size-10, 10, 10))
sprites.add_collision(12, (sprites.new_size-10, sprites.new_size-10, 10, 10))
sprites.add_collision(13, (sprites.new_size-10, 0, 10, sprites.new_size))

# OBJECTS
sprites.make_group('tilesA', (0, 2), 'objectA', sprites_y=4)
sprites.make_group('tilesB', (0, 0), 'objectB', sprites_x=3, sprites_y=3)
sprites.make_group('tilesB', (0, 4), 'hw', sprites_x=4, sprites_y=2)
sprites.make_group('tilesB', (3, 2), 'xmas', sprites_x=4, sprites_y=2)
sprites.make_group('tilesB', (15, 4), 'misc', sprites_x=3, sprites_y=2)
sprites.make_group('tilesC', (3, 0), 'onetile', sprites_x=9, sprites_y=4)
sprites.make_group('tilesC', (14, 0), 'twotileUP', sprites_x=3, sprites_y=6)

# ITEMS
sprites.make_group('tilesC', (0, 4), 'item', sprites_x=4, sprites_y=2)

# regular objects
sprites.make_group('tilesC', (17, 2), 'treeA', sprites_x=4, sprites_y=4)  # BIG tree
sprites.make_group('tilesC', (21, 0), 'treeB', sprites_x=2, sprites_y=3)  # small pine
sprites.make_group('tilesC', (21, 3), 'treeC', sprites_x=4, sprites_y=3)  # big pine
sprites.make_group('tilesC', (23, 0), 'treeD', sprites_x=4, sprites_y=3)  # pink tree

sprites.make_group('tilesB', (9, 3), 'bush', sprites_x=2, sprites_y=3)
sprites.make_group('tilesB', (22, 2), 'shed', sprites_x=2, sprites_y=2)
sprites.make_group('tilesB', (6, 0), 'rock', sprites_y=2)
sprites.make_group('tilesB', (15, 2), 'river', sprites_x=2)

# main gate
sprites.make_group('tilesC', (4, 4), 'mgate', sprites_x=3, sprites_y=2)

# FRAMES ('picture' frames for the outline of the screensw
sprites.make_group('frames', (0, 0), 'frame', sprites_x=2, sprites_y=2, size=250)
sprites.make_group('frames', (0, 1), 'shade', size=250)

# FULL IMAGES
sprites.image('sprites/titlescreen.png', 'title bg')
sprites.image('sprites/menubg.png', 'menu bg')
sprites.image('sprites/pause_menu.png', 'pause bg')
sprites.image('sprites/story.png', 'story bg')
sprites.image('sprites/play.png', 'play')
sprites.image('sprites/pause.png', 'pause')
sprites.image('sprites/playh.png', 'play hower')
sprites.image('sprites/pauseh.png', 'pause hower')
sprites.image('sprites/cw.png', 'name')
sprites.image('sprites/credits.png', 'credits')
sprites.image('sprites/deatchscreenbw.png', 'death')
sprites.image('sprites/part_death.png', 'part death')
sprites.image('sprites/hwplayers.png', 'cat_art')
sprites.image('sprites/hwplayers2.png', 'pig_art')
sprites.image('sprites/hwplayers3.png', 'lizard_art')

pause = pygame.Surface((20, 20))
pause.fill((255, 255, 255))
