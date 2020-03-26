from enum import Enum


class MessageType(str, Enum):
    ACK = "acknowledged"
    CONN = "connection"


class Target(str, Enum):
    """Who is the target of the message."""
    GAME = "game"
    SERVER = "server"  # e.g. for network connection setup, closure
