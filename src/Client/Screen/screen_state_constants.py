from enum import Enum


class ScreenState(str, Enum):
    MAIN_MENU = "main menu structure"
    CONNECTION_MENU = "connection menu"
    GAME = "game"

class ConnectionMenuState(str, Enum):
    INITIAL = "intitial state"
    CONN_MSG_SHOWN = "connection message shown"

class GameOverState(str, Enum):
    ALL_HUMAN_DIED = "lost and all human died"
    LOST = "lost"
    WON = "won"