from enum import Enum


class MessageType(Enum):
    ACK = "acknowledged"


class Target(Enum):
    """Who is the target of the message."""
    GAME = "game"
    SERVER = "server"  # e.g. for network connection setup, closure
