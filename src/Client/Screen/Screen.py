import pygame as pg
import pygameMenu as pgM

import src.Client.Screen.screen_state_constants as sstatecons

# networking
from src.Client.Network_communication.Client import Client

import socket  # to be able to set default IP on connection screen to OUR IP

# messaging
from src.Client.Player.PlayerManager import PlayerManager
import src.Client.Network_communication.client_message_constants as climess
import src.Server.Network_communication.server_message_constants as sermess
from src.utils.BaseMessage import BaseMessage


class Screen:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, screen_height=SCREEN_HEIGHT, screen_width=SCREEN_WIDTH):
        self.__screen = pg.display.set_mode([screen_width, screen_height])
        self.__h, self.__w = [pg.display.Info().current_h, pg.display.Info().current_w]  # get screen h and w

        self.__screenState = sstatecons.ScreenState.MAIN_MENU

        # initializing the menus, the order is important! (i.e. the sub menus of main menu - about & play menus first)
        self.__playMenu = self._init_play_menu()
        self.__aboutMenu = self._init_about_menu()
        self.__mainMenu = self._init_main_menu()

        self.__connectionMenu, self.__connectionMenuState = self._init_connection_menu()

        self.__is_first_player = None

    def update(self, events, pressed_keys):
        self._draw_adequate_screen(events, pressed_keys)

        pg.display.flip()  # flip the display

        return self._check_keyboard_exit_request(events)

    def _game_screen(self, pressed_keys, events):
        self._draw_background_and_terrain()
        PlayerManager.get_instance().update(pressed_keys, events)
        PlayerManager.get_instance().draw_players(screen=self.__screen)

    @staticmethod
    def _check_keyboard_exit_request(events):
        running = True
        for event in events:  # event handling - look at every event in the queue
            if event.type == pg.KEYDOWN:  # did the user hit a key?

                if event.key == pg.K_ESCAPE:  # Was it the Escape key? If so, stop the loop.
                    running = False

            # Did the user click the window close button? If so, stop the loop. w/o. doesn't work
            if event.type == pg.QUIT:
                running = False

        return running

    def _draw_adequate_screen(self, events, pressed_keys):
        # draw the adequate screen (according to the state)
        if self.__screenState == sstatecons.ScreenState.MAIN_MENU:
            self.__mainMenu.mainloop(events)
        elif self.__screenState == sstatecons.ScreenState.CONNECTION_MENU:
            self.__connectionMenu.mainloop(events)
        elif self.__screenState == sstatecons.ScreenState.GAME:
            self._game_screen(pressed_keys, events)

    def _init_main_menu(self):  # first needs sub menus to be initialized!
        main_menu = pgM.Menu(
            self.__screen,
            self.__w,
            self.__h,
            pgM.font.FONT_OPEN_SANS,
            'Main Menu',
            bgfun=self._default_bgfun,
            menu_color=self.BLACK,
            menu_color_title=self.BLACK,
            menu_alpha=100,
            back_box=False
        )

        main_menu.add_option('Play', self.__playMenu)
        main_menu.add_option('About', self.__aboutMenu)
        main_menu.add_option('Exit', pgM.events.EXIT)

        return main_menu

    def _init_play_menu(self):
        play_menu = pgM.TextMenu(
            self.__screen,
            self.__w,
            self.__h,
            pgM.font.FONT_OPEN_SANS,
            'Play Menu',
            bgfun=self._default_bgfun,
            menu_color=self.BLACK,
            menu_color_title=self.BLACK,
            menu_alpha=100
        )

        play_menu_lines = [  # lines to display in main menu -- play menu
            'In order to connect to a server, please enter',
            'its IP address below, followed by enter:',
            ''
        ]
        for txt in play_menu_lines:
            play_menu.add_line(txt)

        play_menu.add_text_input(  # text input for IP
            title='IP: ',
            textinput_id='playMenu_input_IP',
            maxchar=4 * 3 + 3,
            default=socket.gethostbyname(socket.gethostname()),
            onchange=self._onchange_play_menu_input_ip,
            onreturn=self._onreturn_play_menu_input_ip
        )
        play_menu.add_option('Back', pgM.events.BACK)

        return play_menu

    def _init_about_menu(self):
        about_menu = pgM.TextMenu(
            self.__screen,
            self.__w,
            self.__h,
            pgM.font.FONT_OPEN_SANS,
            'About Menu',
            bgfun=self._default_bgfun,
            menu_color=self.BLACK,
            menu_color_title=self.BLACK,
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
            about_menu.add_line(txt)

        about_menu.add_option('Back', pgM.events.BACK)

        return about_menu

    def _init_connection_menu(self):
        connection_menu = pgM.TextMenu(
            self.__screen,
            self.__w,
            self.__h,
            pgM.font.FONT_OPEN_SANS,
            'Connecting Menu',
            bgfun=self._connection_menu_bgfun,
            menu_color=self.BLACK,
            menu_color_title=self.BLACK,
            menu_alpha=100,
            back_box=False
        )

        return connection_menu, sstatecons.ConnectionMenuState.INITIAL

    def _default_bgfun(self):
        self.__screen.fill(self.BLACK)

    def _onchange_play_menu_input_ip(self, val):  # check onchange of playMenu IP input field
        inp_widget = self.__playMenu.get_widget('playMenu_input_IP')

        # do not let to write anything but numbers and dots
        if len(val) > 0 and not (val[-1].isnumeric() or val[-1] == '.'):
            inp_widget.set_value(val[:-1])

    def _onreturn_play_menu_input_ip(self, val):  # check onreturn of playMenu IP input field
        is_okay = True

        if val.count('.') != 3:
            is_okay = False
        else:
            for field in val.split('.'):
                if len(field) == 0 or int(field) > 255:
                    is_okay = False

        if not is_okay:  # if not ok, delete input field content
            self.__playMenu.get_widget('playMenu_input_IP').set_value('')
        else:
            self.__connectionMenu.add_line('Connecting to ' + val + ', please wait.')
            Client.get_instance().setup_connection(val)
            self.__screenState = sstatecons.ScreenState.CONNECTION_MENU
            self.__mainMenu.disable()
            self.__connectionMenu.enable()

    def _connection_menu_bgfun(self):
        # when in INITIAL state and client connection got a status
        if self.__connectionMenuState == sstatecons.ConnectionMenuState.INITIAL and\
                Client.get_instance().connection_alive is not None:

            self.__connectionMenu.add_line('')

            if Client.get_instance().connection_alive:
                self.__connectionMenu.disable()
                self.__connectionMenu, _ = self._init_connection_menu()
                self.__connectionMenu.enable()
                self.__connectionMenu.add_line('Successfully connected.')
            else:
                self.__connectionMenu.add_line('Connection error, please try again!')

            self.__connectionMenuState = sstatecons.ConnectionMenuState.CONN_MSG_SHOWN

        elif self.__connectionMenuState == sstatecons.ConnectionMenuState.CONN_MSG_SHOWN:
            if Client.get_instance().connection_alive:
                msgs = Client.get_instance().get_targets_messages(sermess.Target.SCREEN)

                for msg in msgs:
                    # if this is the first time got FIRST PLAYER msg, then set it accordingly to true
                    if self.__is_first_player is None and msg.type == sermess.MessageType.FIRST_PLAYER:
                        print("I am the host.")
                        self.__is_first_player = True

                        self.__connectionMenu.add_selector(
                            title='Player count: ',
                            values=[('2', 2), ('3', 3), ('4', 4), ('5', 5)],
                            default=0,
                            onchange=self._connection_menu_player_count_selector_onchange
                        )

                        self.__connectionMenu.add_option('Play', self._connection_menu_start_pressed)
                    elif msg.type == sermess.MessageType.INITIAL_DATA:
                        print("Game started, terrain loaded")
                        self.__terrain_points = msg.terrain_points
                        self.__terrain_points_levels = msg.terrain_points_levels
                        self.__screenState = sstatecons.ScreenState.GAME
                        self.__connectionMenu.disable()
                        PlayerManager.get_instance().create_players(msg.apple_human_ids, msg.orange_human_ids,
                                                                    msg.apple_ai_ids, msg.orange_ai_ids)

            else:
                self.__screenState = sstatecons.ScreenState.MAIN_MENU
                self.__connectionMenu.disable()
                self.__mainMenu.enable()

                # reinitialize. connectionMenu so that it flushes msgs
                self.__connectionMenu, self.__connectionMenuState = self._init_connection_menu()

                # acknowledged the connection error status, and now set back the flag to None
                Client.get_instance().connection_alive = None

                pg.time.wait(2500)

    @staticmethod
    def _connection_menu_player_count_selector_onchange(_, value):
        msg = BaseMessage(mess_type=climess.MessageType.CHANGE_PLAYER_NUMBER, target=climess.Target.GAME)
        msg.new_number = value
        Client.get_instance().send_message(msg)

    @staticmethod
    def _connection_menu_start_pressed():
        msg = BaseMessage(mess_type=climess.MessageType.START_GAME_MANUALLY, target=climess.Target.GAME)
        Client.get_instance().send_message(msg)

    def _draw_background_and_terrain(self):
        self.__screen.fill(self.BLACK)  # black bg
        for i in range(1, len(self.__terrain_points)):
            pg.draw.line(
                self.__screen,
                self.WHITE,
                (self.__terrain_points[i - 1], self.__h - self.__terrain_points_levels[i - 1]),
                (self.__terrain_points[i], self.__h - self.__terrain_points_levels[i])
            )
