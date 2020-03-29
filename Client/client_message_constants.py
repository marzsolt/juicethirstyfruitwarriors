from enum import Enum


class MessageType(str, Enum):
    ACK = "acknowledged"  # received the message
    CONN = "connection"  # connection related
    CHANGE_PLAYER_NUMBER = "change player number"
    START_GAME_MANUALLY = "start game manually"
    PLAYER_POS = "position of players"


class Target(str, Enum):
    """Who is the target of the message."""
    GAME = "game"  # the Game-related stuff on the server side
    SERVER = "server"  # e.g. for network connection setup, closure
    PLAYER_LOGIC = "playerlogic"
