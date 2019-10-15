from sprites import *
pygame.init()


class Font(object):
    def __init__(self, name, size=15, colour=(0, 0, 0)):
        self.name = name
        self.size = size
        self.colour = colour
        self.font = pygame.font.SysFont(name, size)

    def text(self, text, pos=None, where=screen):
        t = self.font.render(text, 1, self.colour)
        if pos is not None:
            # setting on or both items in tuple to 'center' centers the text to the screen.
            # negative pos value will be taken from the other end of the screen
            new_pos = list(pos)
            if pos[0] == 'center':
                new_pos[0] = screen_x/2 - t.get_width()/2
            elif pos[0] < 0:
                new_pos[0] = screen_x + pos[0] - t.get_width()
            if pos[1] == 'center':
                new_pos[1] = screen_y/2 - t.get_height()/2
            elif pos[1] < 0:
                new_pos[1] = screen_y + pos[1] - t.get_height()
            where.blit(t, new_pos)
        # returns length, if assigned to a variable
        return t.get_width()


class Button(object):

    def __init__(self, font, frame_colour=(200, 200, 200), clickable_colour=(150, 150, 150),
                 unavailable_colour=(230, 230, 230)):
        self.text = ''
        self.font = font
        self.frame_colour = frame_colour
        self.clickable_colour = clickable_colour
        self.unavailable_colour = unavailable_colour

    def draw_button(self, pos, available=True, image=None, text='', **values):
        # self.on_screen = True

        if not available:
            colour = self.unavailable_colour
        else:
            colour = self.frame_colour

        # creating visible button
        if image is None:
            new_button = pygame.Surface((self.font.text(text) + 10, self.font.size + 6))
        else:
            new_button = image

        new_pos = list(pos)
        if pos[0] == 'center':
            new_pos[0] = screen_x / 2 - new_button.get_width() / 2
        elif pos[0] < 0:
            new_pos[0] = screen_x + pos[0] - new_button.get_width()
        if pos[1] == 'center':
            new_pos[1] = screen_y / 2 - new_button.get_height() / 2
        elif pos[1] < 0:
            new_pos[1] = screen_y + pos[1] - new_button.get_height()

        # Check collision
        collision = screen.blit(new_button, new_pos)
        clickable = False
        if available and collision.collidepoint(mouse.pos):
            colour = self.clickable_colour
            clickable = True

        # fill in non-image button
        if image is None:
            new_button.fill(colour)
            self.font.text(text, (5, 0), new_button)
            screen.blit(new_button, new_pos)
        else:
            screen.blit(new_button, new_pos)

        # CLICK
        if game.clicked and clickable:
            self.activate(values)

    def activate(self, values=None):
        if values is None:
            values = {}
        add = False
        if 'add' in values.keys():
            add = values['add']
        for key, value in values.items():
            if key in game.switch.keys() and not add:
                game.switch[key] = value
            elif key in game.switch.keys() and add:
                game.switch[key].append(value)


class Menu(object):
    def __init__(self, name, background, bodytext, bodytext_pos, header1=None, header2=None, header1_pos=None,
                 header2_pos=None, bg_pos=(0, 0)):
        self.name = name
        self.background = background
        self.bg_pos = bg_pos

        # Fonts, of font class
        self.bodytext = bodytext
        if header1 is None:
            self.header1 = bodytext
        else:
            self.header1 = header1
        if header2 is None:
            self.header2 = bodytext
        else:
            self.header2 = header2
        self.header1_pos = header1_pos
        self.header2_pos = header2_pos
        self.bodytext_pos = bodytext_pos

    def on_use(self, text, header1_text=None, header2_text=None, buttons=None):
        # buttons is a list of lists; one button = [
        screen.blit(self.background, self.bg_pos)

        if header1_text is not None and self.header1_pos is not None:
            self.header1.text(header1_text, self.header1_pos)
        if header2_text is not None and self.header2_pos is not None:
            self.header2.text(header2_text, self.header2_pos)

        self.bodytext.text(text, self.bodytext_pos)

        if buttons is not None:
            for b in buttons:
                if b[0] == 'gameplay':
                    button.draw_button(b[1], text='PLAY', cur_mode='gameplay')


# FONTS
font_1 = Font('courier', colour=(230, 230, 230))
b_font = Font('courier', colour=(0, 0, 0))
header_1 = Font('courier', 25, colour=(230, 230, 230))
header_2 = Font('courier', 20, colour=(230, 230, 230))

# BUTTONS
button = Button(b_font)

# MENU
title_screen = Menu('titlescreen', sprites.images['title bg'], font_1, (50, 200), header_1, header_2,
                    (50, 70), (50, 110))
