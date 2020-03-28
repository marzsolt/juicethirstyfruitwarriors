from enum import Enum


class MessageType(str, Enum):
    ACK = "acknowledged"
    CONN = "connection"
    YOUR_ID = "your ID is..."
    FIRST_PLAYER = "you are the host"
    GAME_STARTED = "gl hf"


class Target(str, Enum):
    """Who is the target of the message."""
    SCREEN = "screen"
    PLAYER = "player"  # should use ID someway 
    CLIENT = "client"  # e.g. for network connection setup, closure
