import pygame


class Sprites(object):
    def __init__(self, original_size, new_size=None):
        self.size = original_size  # size of a single original sprite in a spritesheet
        if new_size is None:
            self.new_size = self.size*2
        else:
            self.new_size = new_size  # size that the sprites will be transformed to as bigger sprites
        self.spritesheets = {}
        self.images = {}
        self.groups = {}
        self.sprites = {}
        self.big_sprites = {}

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

        # making the group
        new_group = pygame.Surface((self.size*sprites_x, self.size*sprites_y), pygame.HWSURFACE | pygame.SRCALPHA)
        new_group.blit(self.spritesheets[spritesheet], (0, 0),
                       (pos[0]*sprites_x*self.size, pos[1]*sprites_y*self.size,
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


sprites = Sprites(32)

# PLAYER SPRITES
sprites.spritesheet('sprites/player_spr.png', 'playerSPR')      # player sprite-sheet can be called with playerSPR
sprites.make_group('playerSPR', (0, 0), 'playerSPR', sprites_x=2)


# TILES
sprites.spritesheet('sprites/viiuntiles1.png', 'tilesA')
sprites.make_group('tilesA', (0, 0), 'groundA', sprites_x=3, sprites_y=2)

ground = {0: sprites.sprites['groundA0']}
