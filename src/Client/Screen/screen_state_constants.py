from enum import Enum


class ScreenState(str, Enum):
    """" Constants for screen states. """
    MAIN_MENU = "main menu structure"
    CONNECTION_MENU = "connection menu"
    GAME = "game"

class ConnectionMenuState(str, Enum):
    """" Constants for connectionMenu states. """
    INITIAL = "intitial state"
    CONN_MSG_SHOWN = "connection message shown"

class GameOverState(str, Enum):
    """" Constants for game over states. """
    ALL_HUMAN_DIED = "lost and all human died"
    LOST = "lost"
    WON = "won"