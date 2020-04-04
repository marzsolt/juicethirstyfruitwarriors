from enum import Enum


class MessageType(str, Enum):
    ACK = "acknowledged"  # received the message
    CONN = "connection"  # connection related
    CHANGE_PLAYER_NUMBER = "change player number"
    START_GAME_MANUALLY = "start game manually"
    PLAYER_MOVEMENT = "movement of players"


class Target(str, Enum):
    """Who is the target of the message."""
    GAME = "game"  # the Game-related stuff on the server side
    SERVER = "server"  # e.g. for network connection setup, closure
    PLAYER_LOGIC = "playerlogic"


class ActionRequest(str, Enum):
    MOVE_LEFT = "move left"
    MOVE_RIGHT = "move right"
    MOVE_UP = "move up"
    MOVE_DOWN = "move down"
