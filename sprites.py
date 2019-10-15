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

        self.cycles = {}  # for animation; includes counter for cur. frame  'name': [counter, [frames]]

    def spritesheet(self, a_file, name):
        self.spritesheets[name] = pygame.image.load(a_file)

    def image(self, a_file, name):
        self.images[name] = pygame.image.load(a_file)

    def find_sprite(self, group_name, x, y):
        # find sprites from a group
        # pixels will be calculated automatically, so for x and y, just use 0, 1, 2, 3 etc.
        new_sprite = pygame.Surface((self.size, self.size), pygame.HWSURFACE | pygame.SRCALPHA)
        new_sprite.blit(self.groups[group_name], (0, 0),
                        (x*self.size, y*self.size, (x+1)*self.size, (y+1)*self.size))
        return new_sprite

    def make_group(self, spritesheet, pos, name, sprites_x=1, sprites_y=1):  # pos = ex. (2, 3), no single pixels
        # divide sprites on a sprite-sheet into groups of sprites that are easily accessible
        self.group_sizes[name] = sprites_x * sprites_y

        # making the group
        new_group = pygame.Surface((self.size*sprites_x, self.size*sprites_y), pygame.HWSURFACE | pygame.SRCALPHA)
        new_group.blit(self.spritesheets[spritesheet], (0, 0),
                       (pos[0]*self.size, pos[1]*self.size,
                        (pos[0]+sprites_x)*self.size, (pos[1]+sprites_y)*self.size))
        self.groups[name] = new_group

        # splitting group into singular sprites and storing in self.sprites, also making bigger sprites
        x_spr = 0
        y_spr = 0
        for x in range(sprites_x * sprites_y):
            new_sprite = pygame.Surface((self.size, self.size), pygame.HWSURFACE | pygame.SRCALPHA)
            new_sprite.blit(new_group, (0, 0), (x_spr*self.size, y_spr*self.size,
                                                (x_spr+1)*self.size, (y_spr+1)*self.size))
            self.sprites[name+str(x)] = new_sprite
            self.big_sprites[name+str(x)] = pygame.transform.scale(new_sprite, (sprites.new_size, sprites.new_size))
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

# PLAYER SPRITES
sprites.spritesheet('sprites/player_spr.png', 'playerSPR')      # player sprite-sheet can be called with playerSPR
sprites.make_group('playerSPR', (0, 0), 'pig', sprites_y=4)
sprites.make_group('playerSPR', (1, 0), 'lizard', sprites_y=4)
sprites.make_group('playerSPR', (2, 0), 'cat', sprites_y=2)


# TILES
# upload spritesheets
sprites.spritesheet('sprites/tiles1.png', 'tilesA')
sprites.spritesheet('sprites/tiles2.png', 'tilesB')

# make groups
sprites.make_group('tilesA', (0, 0), 'groundA', sprites_x=3, sprites_y=2)
sprites.make_group('tilesA', (3, 0), 'groundB', sprites_x=3, sprites_y=2)
sprites.make_group('tilesB', (0, 4), 'groundC', sprites_x=3, sprites_y=2)

for l in ['A', 'B', 'C']:
    sprites.flip_tiles('ground'+l, [0, 0, 0, 1, 2, 2, 2, 3],
                       ['hor', 'ver', 'both', 'ver', 'hor', 'ver', 'both', 'hor'], 6)

# OBJECTS - second layer
sprites.make_group('tilesA', (0, 2), 'objectA', sprites_y=4)
sprites.make_group('tilesB', (0, 0), 'objectB', sprites_x=3, sprites_y=3)
sprites.make_group('tilesB', (4, 4), 'misc', sprites_x=3, sprites_y=2)


# FULL IMAGES
sprites.image('sprites/titlebg.png', 'title bg')
