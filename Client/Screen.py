import pygame as pg
import pygameMenu as pgM

import Client


class Screen:
    screen = None
    h = None
    w = None
    screenState = 0  # 0: main menu structure; 1: connecting menu

    # main menu structure menus:
    mainMenu = None
    playMenu = None
    aboutMenu = None

    # connecting menu:
    connectingMenu = None

    serverIP = None

    def __init__(self, screen_height=0, screen_width=0):
        self.screen = pg.display.set_mode([screen_width, screen_height], pg.FULLSCREEN)
        [self.h, self.w] = [pg.display.Info().current_h, pg.display.Info().current_w]  # get screen h and w

        # -----------------------------
        # defining main menu structure
        # -----------------------------

        # defining main menu
        self.mainMenu = pgM.Menu(
            self.screen,
            self.w,
            self.h,
            pgM.font.FONT_OPEN_SANS,
            'Main Menu',
            bgfun=self.main_bgfun,
            menu_color=(0, 0, 0),
            menu_color_title=(0, 0, 0),
            menu_alpha=100,
            back_box=False
        )

        # defining main menu - play menu
        self.playMenu = pgM.TextMenu(
            self.screen,
            self.w,
            self.h,
            pgM.font.FONT_OPEN_SANS,
            'Play Menu',
            bgfun=self.main_bgfun,
            menu_color=(0, 0, 0),
            menu_color_title=(0, 0, 0),
            menu_alpha=100
        )

        play_menu_lines = [  # lines to display in main menu -- play menu
            'In order to connect to a server, please enter',
            'its IP address below, followed by enter:',
            ''
        ]
        for txt in play_menu_lines:
            self.playMenu.add_line(txt)

        self.playMenu.add_text_input(  # text input for IP
            title='IP: ',
            textinput_id='playMenu_input_IP',
            maxchar=4 * 3 + 3,
            onchange=self.onchange_play_menu_input_ip,
            onreturn=self.onreturn_play_menu_input_ip
        )
        self.playMenu.add_option('Back', pgM.events.BACK)

        # defining main menu -- about menu
        self.aboutMenu = pgM.TextMenu(
            self.screen,
            self.w,
            self.h,
            pgM.font.FONT_OPEN_SANS,
            'About Menu',
            bgfun=self.main_bgfun,
            menu_color=(0, 0, 0),
            menu_color_title=(0, 0, 0),
            menu_alpha=100
        )

        about_menu_lines = [
            'This is a game developed in pygame,',
            'proudly delivered to you by:',
            '',
            'Farkas Domonkos László',
            'Molnár Petra',
            'Márkos Zsolt'
        ]
        for txt in about_menu_lines:
            self.aboutMenu.add_line(txt)

        self.aboutMenu.add_option('Back', pgM.events.BACK)

        # extending mai menu with the newly defined play & about menus
        self.mainMenu.add_option('Play', self.playMenu)
        self.mainMenu.add_option('About', self.aboutMenu)
        self.mainMenu.add_option('Exit', pgM.events.EXIT)

        # -----------------------------
        # defining connecting menu
        # -----------------------------

        self.connectingMenu = pgM.TextMenu(
            self.screen,
            self.w,
            self.h,
            pgM.font.FONT_OPEN_SANS,
            'Connecting Menu',
            bgfun=self.connecting_menu_bgfun,
            menu_color=(0, 0, 0),
            menu_color_title=(0, 0, 0),
            menu_alpha=100,
            back_box=False
        )

    def update(self, events):

        # draw the adequate screen (according to the state)
        if self.screenState == 0:
            self.mainMenu.mainloop(events)
        elif self.screenState == 1:
            self.connectingMenu.mainloop(events)

        running = True
        for event in events:  # event handling - look at every event in the queue

            if event.type == pg.KEYDOWN:  # did the user hit a key?

                if event.key == pg.K_ESCAPE:  # Was it the Escape key? If so, stop the loop.
                    running = False

            # Did the user click the window close button? If so, stop the loop. w/o. doesn't work
            if event.type == pg.QUIT:
                running = False

        pg.display.flip()  # flip the display

        return running

    def main_bgfun(self):
        self.screen.fill((255, 128, 0))  # some sort of orange for background

    def onchange_play_menu_input_ip(self, val):  # check onchange of playMenu IP input field
        inp_widget = self.playMenu.get_widget('playMenu_input_IP')

        # do not let to write anything but numbers and dots
        if len(val) > 0 and not (val[-1].isnumeric() or val[-1] == '.'):
            inp_widget.set_value(val[:-1])

        '''
        # if last 3 chars are numeric, then write automatically a dot - unless there are already 3 dots
        # BUG: cannot delete dots
        # hence of bug, maybe developed in future
        if len(val) >=3 and val[-3:].isnumeric() and val.count('.') < 3:
            print(val[-3:])
            inp_widget.set_value(val + '.')
        '''

    def onreturn_play_menu_input_ip(self, val):  # check onreturn of playMenu IP input field
        is_okay = True

        if val.count('.') != 3:
            is_okay = False
        else:
            for field in val.split('.'):
                if len(field) == 0 or int(field) > 255:
                    is_okay = False

        if not is_okay:
            self.playMenu.get_widget('playMenu_input_IP').set_value('')
        else:
            self.connectingMenu.add_line('Connecting to ' + val + ', please wait.')
            self.serverIP = val
            self.mainMenu.disable()
            self.screenState = 1

    def connecting_menu_bgfun(self):
        Client.Client.get_instance(self.serverIP)

