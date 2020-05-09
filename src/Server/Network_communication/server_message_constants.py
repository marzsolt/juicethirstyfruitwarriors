from enum import Enum


class MessageType(str, Enum):
    ACK = "acknowledged"
    CONN = "connection"
    YOUR_ID = "your ID is..."
    FIRST_PLAYER = "you are the host"
    INITIAL_DATA = "gl hf"
    PLAYER_POS_HP = "movement and health of players"
    ORANGE_ROLL = "roll orange..."
    DIED = "that's it... the END for someone"
    WON = "there's a winner"
    NO_ALIVE_HUMAN = "unfortunately no human player is alive"


class Target(str, Enum):
    """ Who is the target of the message. """
    SCREEN = "screen"
    PLAYER = "player"  # should use ID someway
    ORANGE_PLAYER = "orange player" # for rolling purposes, iinf of ACK of valid attack
    CLIENT = "client"  # e.g. for network connection setup, closure
    PLAYER_MANAGER = "player manager"
