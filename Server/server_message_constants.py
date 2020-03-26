from enum import Enum


class MessageType(str, Enum):
    ACK = "acknowledged"
    CONN = "connection"
    ID = "ID"


class Target(str, Enum):
    """Who is the target of the message."""
    SCREEN = "screen"
    PLAYER = "player"  # should use ID someway 
    CLIENT = "client"  # e.g. for network connection setup, closure
