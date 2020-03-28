import pygame as pg
import pygameMenu as pgM
import socket
import Client
import client_message_constants as climess
import server_message_constants as sermess
import BaseMessage


class Screen:
    def __init__(self, screen_height=0, screen_width=0):
        self.screen = pg.display.set_mode([screen_width, screen_height], pg.FULLSCREEN)
        [self.h, self.w] = [pg.display.Info().current_h, pg.display.Info().current_w]  # get screen h and w

        self.screenState = 0  # 0: main menu structure; 1: connecting menu

        self.init_main_menu_play_menu()
        self.init_main_menu_about_menu()
        self.init_main_menu()
        self.init_connecting_menu()

        self.is_conn_msg_shown = False
        self.is_first_player = None

    def init_main_menu(self): # first needs sub menus to be initialized!
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

        self.mainMenu.add_option('Play', self.playMenu)
        self.mainMenu.add_option('About', self.aboutMenu)
        self.mainMenu.add_option('Exit', pgM.events.EXIT)

    def init_main_menu_play_menu(self):
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
            default=socket.gethostbyname(socket.gethostname()),
            onchange=self.onchange_play_menu_input_ip,
            onreturn=self.onreturn_play_menu_input_ip
        )
        self.playMenu.add_option('Back', pgM.events.BACK)

    def init_main_menu_about_menu(self):
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

    def init_connecting_menu(self):
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

    #  More useful functions below!!!
    def update(self, events):

        # draw the adequate screen (according to the state)
        if self.screenState == 0:
            if not self.mainMenu.is_enabled():
                self.mainMenu.enable()
            self.mainMenu.mainloop(events)
        elif self.screenState == 1:
            if not self.connectingMenu.is_enabled():
                self.connectingMenu.enable()
            self.connectingMenu.mainloop(events)
        elif self.screenState == 3:
            self.game_screen()

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
        self.screen.fill((0, 0, 0))  # black bg

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
            Client.Client.get_instance().setup_connection(val)
            self.mainMenu.disable()
            self.screenState = 1

    def connecting_menu_bgfun(self):

        if self.is_conn_msg_shown:
            if Client.Client.get_instance().connection_alive: # read messages
                msgs = Client.Client.get_instance().get_targets_messages(sermess.Target.SCREEN)
                # WARNING: this perhaps flushes the message queue - make sure no one needs for a gentle amount of time

                for msg in msgs:
                    if self.is_first_player is None and msg.type == sermess.MessageType.FIRST_PLAYER:
                        print("I am the host.")
                        self.is_first_player = True

                        self.connectingMenu.add_selector(
                            title='Player count: ',
                            values=[('2', 2), ('3', 3), ('4', 4), ('5', 5)],
                            default=0,
                            onchange=self.connecting_menu_player_count_selector_onchange
                        )

                        self.connectingMenu.add_option('Play', self.connecting_menu_start_pressed)
                    elif msg.type == sermess.MessageType.GAME_STARTED:
                        print("Game started")
                        self.connectingMenu.disable()
                        self.screenState = 3
            else:
                self.screenState = 0
                self.playMenu.get_widget('playMenu_input_IP').set_value('')  # TODO: this may be done onreturn

                self.connectingMenu.disable()
                self.init_connecting_menu()  # reinitialize connectingMenu so that it flushes its msgs

                # acknowledged the connection error status, and now set back the flag to None
                Client.Client.get_instance().connection_alive = None
                self.is_conn_msg_shown = False

                pg.time.wait(2500)

        elif Client.Client.get_instance().connection_alive is not None:
            self.connectingMenu.add_line('')

            if Client.Client.get_instance().connection_alive:
                self.connectingMenu.disable()
                self.init_connecting_menu()
                self.connectingMenu.add_line('Successfully connected.')
            else:
                self.connectingMenu.add_line('Connection error, please try again!')

            self.is_conn_msg_shown = True

    def connecting_menu_player_count_selector_onchange(self, txt_value, value):
        msg = BaseMessage.BaseMessage(mess_type=climess.MessageType.CHANGE_PLAYER_NUMBER,
                                          target=climess.Target.GAME)
        msg.new_number = value
        Client.Client.get_instance().send_message(msg)

    def connecting_menu_start_pressed(self):
        msg = BaseMessage.BaseMessage(mess_type=climess.MessageType.START_GAME_MANUALLY,
                                      target=climess.Target.GAME)
        Client.Client.get_instance().send_message(msg)

    def game_screen(self):
        self.screen.fill((0, 0, 0))  # black bg
