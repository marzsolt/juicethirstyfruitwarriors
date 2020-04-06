from PlayerLogic import PlayerLogic
from enum import Enum
import random


class Movement(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    IDLE = "IDLE"


class PlayerAILogic(PlayerLogic):
    def __init__(self, player_id):
        super(PlayerAILogic, self).__init__(player_id)
        self._dir = Movement.RIGHT

    def update(self):  # override player's update
        self.decide_direction()
        if self._dir == Movement.LEFT:
            self._move_left()
        elif self._dir == Movement.RIGHT:
            self._move_right()

        self._send_updated_pos()

    def decide_direction(self):
        if random.random() < 0.03:  # so that it won't shake too much
            self._dir = random.choice([Movement.LEFT, Movement.RIGHT, Movement.IDLE])
