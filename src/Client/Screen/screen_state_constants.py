from enum import Enum


class ScreenState(str, Enum):
    MAIN_MENU = "main menu structure"
    CONNECTION_MENU = "connection menu"
    GAME = "game"
    GAME_OVER = "game over"


class ConnectionMenuState(str, Enum):
    INITIAL = "intitial state"
    CONN_MSG_SHOWN = "connection message shown"
