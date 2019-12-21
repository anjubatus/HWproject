from sprites import *
pygame.init()


class Button(object):
    def __init__(self, font, frame_colour=(227, 208, 168), clickable_colour=(227, 177, 116),
                 unavailable_colour=(230, 230, 230)):
        self.text = ''
        self.font = font
        self.frame_colour = frame_colour
        self.clickable_colour = clickable_colour
        self.unavailable_colour = unavailable_colour

    def draw_button(self, pos, available=True, image=None, text='', hower=None,  **values):
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
            if image is not None:
                new_button = hower

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
                if key == 'music' and game.switch['music'] is not None:
                    pygame.mixer.music.fadeout(600)
                if key == 'music' and value is not None:
                    pygame.mixer.music.load(value)
                    pygame.mixer.music.play(-1)
                if key == 'cur_mode':
                    game.fade_out = True
                    game.waiting_commands[key] = value  # game waits for fade to finish in order to execute command
                else:
                    game.switch[key] = value
            elif key in game.switch.keys() and add:
                game.switch[key].append(value)

        # select sound
        if game.switch['sounds_on']:
            pygame.mixer.Sound.play(game.sounds['select'])


class Menu(object):
    music = {'title': 'sounds/title_music.mp3', 'ingame': 'sounds/ingame_music.mp3'}

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

    def main_menu(self):
        # buttons is a list of lists; one button = []
        screen.blit(self.background, self.bg_pos)
        screen.blit(sprites.images['name'], (20, 40))

        # buttons
        button.draw_button((50, 290), text='PLAY', menu='switch menu')
        button.draw_button((50, 320), text='INFO & CONTROLS', menu='info screen')
        if game.switch['music_on']:
            button.draw_button((50, 350), text='MUSIC OFF', music=None, music_on=False)
        else:
            button.draw_button((50, 350), text='MUSIC ON', music=self.music['title'], music_on=True)
        if game.switch['sounds_on']:
            button.draw_button((50, 380), text='SOUNDS OFF', sounds_on=False)
        else:
            button.draw_button((50, 380), text='SOUNDS ON', sounds_on=True)

    def switch_menu(self):
        screen.blit(sprites.images['menu bg'], (0, 0))

        # choose between single and two-player
        if game.switch['play_mode'] is None:
            self.header1.text('Single player (WASD) or Two-Player (WASD + arrow keys)?', ('center', 100))
            button.draw_button((100, 250), text='SINGLE', play_mode='single')
            button.draw_button((-100, 250), text='TWO', play_mode='two')
            button.draw_button((50, 50), text='< BACK', menu='main menu')
        elif game.switch['play_mode'] == 'single':
            if game.switch['player_1'] is None:
                # choose character - SINGLE PLAYER
                self.header1.text('Choose your character:', ('center', 100))

                # IMAGES
                screen.blit(sprites.size_sprites['pig0'], (100, 220))
                screen.blit(sprites.size_sprites['lizard0'], (420, 220))
                screen.blit(sprites.size_sprites['cat0'], (730, 220))

                # BUTTONS
                button.draw_button((150, 400), text='CHOOSE', player_1='pig')
                button.draw_button(('center', 400), text='CHOOSE', player_1='lizard')
                button.draw_button((-150, 400), text='CHOOSE', player_1='cat')
                button.draw_button((50, 50), text='< BACK', menu='main menu')
            else:
                # characters and play mode has been selected
                self.header2.text("Use W + A + S + D to move", ('center', 100))
                screen.blit(sprites.size_sprites[game.switch['player_1']+'0'], (420, 150))
                self.header2.text("Use 'M' to SPRINT", ('center', 350))

                # PLAY button
                if game.switch['music_on']:
                    button.draw_button(('center', 400), text='PLAY', menu='story screen', music=None)
                else:
                    button.draw_button(('center', 400), text='PLAY', menu='story screen')
                button.draw_button((50, 50), text='< BACK', menu='main menu')

        elif game.switch['play_mode'] == 'two':
            # choose character - TWO PLAYER
            if game.switch['player_1'] is None:
                self.header1.text('Choose your character:', ('center', 70))
                self.header2.text('PLAYER 1', ('center', 110))

                # IMAGES
                screen.blit(sprites.size_sprites['pig0'], (100, 220))
                screen.blit(sprites.size_sprites['lizard0'], (420, 220))
                screen.blit(sprites.size_sprites['cat0'], (730, 220))

                # BUTTONS
                button.draw_button((150, 400), text='CHOOSE', player_1='pig')
                button.draw_button(('center', 400), text='CHOOSE', player_1='lizard')
                button.draw_button((-150, 400), text='CHOOSE', player_1='cat')
                button.draw_button((50, 50), text='< BACK', menu='main menu')
            elif game.switch['player_2'] is None:
                self.header1.text('Choose your character:', ('center', 70))
                self.header2.text('PLAYER 2', ('center', 110))

                # IMAGES
                screen.blit(sprites.size_sprites['pig0'], (100, 220))
                screen.blit(sprites.size_sprites['lizard0'], (420, 220))
                screen.blit(sprites.size_sprites['cat0'], (730, 220))

                # BUTTONS
                if game.switch['player_1'] != 'pig':
                    button.draw_button((150, 400), text='CHOOSE', player_2='pig')
                if game.switch['player_1'] != 'lizard':
                    button.draw_button(('center', 400), text='CHOOSE', player_2='lizard')
                if game.switch['player_1'] != 'cat':
                    button.draw_button((-150, 400), text='CHOOSE', player_2='cat')
                button.draw_button((50, 50), text='< BACK', menu='main menu')
            else:
                # characters and play mode has been selected, give play button
                self.header2.text('PLAYER 1', (200, 50))
                self.header2.text('PLAYER 2', (-200, 50))
                self.header2.text("W + A + S + D", (180, 100))
                self.header2.text("ARROW KEYS", (-190, 100))
                screen.blit(sprites.size_sprites[game.switch['player_1']+'0'], (160, 150))
                screen.blit(sprites.size_sprites[game.switch['player_2'] + '0'], (680, 150))
                self.header2.text("'V' to SPRINT", (180, 350))
                self.header2.text("'M' to SPRINT", (-180, 350))
                if game.switch['music_on']:
                    button.draw_button(('center', 400), text='PLAY', menu='story screen', music=None)
                else:
                    button.draw_button(('center', 400), text='PLAY', menu='story screen')
                button.draw_button((50, 50), text='< BACK', menu='main menu')

    def story_screen(self):
        screen.blit(sprites.images['story bg'], (0, 0))

        self.bodytext.text("How unlucky - you\'ve gotten lost!", (500, 125))
        self.bodytext.text("You\'re stranded in the dangerous Cranberry Woodlands.", (500, 155))
        self.bodytext.text("Those who enter rarely make it out alive... ", (500, 175))
        self.bodytext.text("All is not lost, however!", (500, 195))
        self.bodytext.text("There is an old gateway which leads out of the woods.", (500, 215))
        self.bodytext.text("The gates are locked, though, and the key pieces", (500, 235))
        self.bodytext.text("strewn around the grounds...", (500, 255))
        self.bodytext.text("Accept your untimely death or find your way out...", (500, 290))

        if game.switch['music_on']:
            button.draw_button((550, 350), text='CONTINUE', cur_mode='gameplay', music=self.music['ingame'])
        else:
            button.draw_button((550, 350), text='CONTINUE', cur_mode='gameplay')

    def info_screen(self):
        screen.blit(sprites.images['menu bg'], (0, 0))

        self.header1.text('INFO', ('center', 50))
        self.header2.text('- Controls -', ('center', 90))

        self.bodytext.text('SINGLEPLAYER:', ('center', 140))
        self.bodytext.text('control character with WASD', ('center', 160))
        self.bodytext.text("sprint with 'M'", ('center', 180))
        self.bodytext.text('MULTIPLAYER:', ('center', 230))
        self.bodytext.text('PLAYER 1:              PLAYER 2:', ('center', 250))
        self.bodytext.text("WASD                  ARROWKEYS", ('center', 270))
        self.bodytext.text("sprint: 'V'            sprint: 'M'", ('center', 290))

        # buttons
        button.draw_button((50, 50), text='< BACK', menu='main menu')
        button.draw_button(('center', 350), text='CREDITS', menu='credits', music=None)

    def credits(self):
        # background
        screen.blit(sprites.images['credits'], (0, 0))

        # hetkellinen fonntien vaihto
        self.bodytext = b_font
        self.header1 = header_1_b
        self.header2 = header_2_b

        self.header1.text('CREDITS', ('center', 50))
        self.header2.text('-', ('center', 90))

        self.bodytext.text('Game by Cardiac cat', ('center', 120))

        self.bodytext.text('Programming and character design by', ('center', 160))
        self.bodytext.text('Anja Talvitie (just-some-cat.tumblr.com)', ('center', 180))
        self.bodytext.text('Project managing and graphics by', ('center', 210))
        self.bodytext.text('Olivia Talvitie (asamanni)', ('center', 230))
        self.bodytext.text('Music and trailer provided by', ('center', 260))
        self.bodytext.text('leevi_undead', ('center', 280))
        self.bodytext.text('Sound-effects from', ('center', 310))
        self.bodytext.text('freesound.org', ('center', 330))

        self.bodytext.text("Contact us at:", ('center', 360))
        self.bodytext.text("cardiacccat@gmail.com", ('center', 380))

        self.bodytext.text('Thank you for playing!', ('center', 410))

        # turn base fonts back
        self.bodytext = font_1
        self.header1 = header_1
        self.header2 = header_2

        # buttons
        if game.switch['music_on']:
            button.draw_button(('center', 450), text='CONTINUE', menu='main menu', music=self.music['title'])
        else:
            button.draw_button(('center', 450), text='CONTINUE', menu='main menu', reset=True)

    def win_screen(self):
        self.header1.text('YOU WON', ('center', 70))
        self.header2.text('you got out of the woods!', ('center', 110))
        if game.switch['music_on']:
            button.draw_button(('center', 350), text='CONTINUE', menu='credits')
        else:
            button.draw_button(('center', 350), text='CONTINUE', menu='credits')

    def death_screen(self):
        self.header1.text('GAME OVER', ('center', 70))
        self.header2.text('your ghost will wander the forests from now on...', ('center', 110))
        if game.switch['music_on']:
            button.draw_button(('center', 350), text='CONTINUE', menu='main menu', reset=True,
                               music=self.music['title'])
        else:
            button.draw_button(('center', 350), text='CONTINUE', menu='main menu', reset=True)


# BUTTONS
button = Button(b_font)

# MENU
title_screen = Menu('titlescreen', sprites.images['title bg'], font_1, (50, 200), header_1, header_2,
                    (50, 70), (50, 110))
