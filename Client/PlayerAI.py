import PlayerLogic
from enum import Enum
import random
import Player


class Movement(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    IDLE = "IDLE"


class PlayerAI(Player.Player):
    def __init__(self, player_id):
        super(PlayerAI, self).__init__(player_id)
        self._dir = Movement.IDLE

    def update(self, pressed_keys, events):
        if random.random() < 0.1:  # so that it won't shake too much
            self._dir = random.choice([m.value for m in Movement])
        network_messages = [self._dir]
        PlayerLogic.players[self._id].process_requests(network_messages, self)
