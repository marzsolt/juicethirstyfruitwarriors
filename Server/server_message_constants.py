from enum import Enum


class MessageType(Enum):
    ACK = "acknowledged"


class Target(Enum):
    """Who is the target of the message."""
    SCREEN = "screen"
    PLAYER = "player"  # should use ID someway 
    CLIENT = "client"  # e.g. for network connection setup, closure
