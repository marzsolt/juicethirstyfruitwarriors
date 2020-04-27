from enum import Enum
import random

from juicethirstyfruitwarriors.Server.Player.PlayerLogic import PlayerLogic


class Movement(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    IDLE = "IDLE"


class PlayerAILogic(PlayerLogic):
    def __init__(self, player_id, __terrain):
        super(PlayerAILogic, self).__init__(player_id, __terrain)
        self._dir = Movement.RIGHT

    def update(self):
        self.decide_direction()
        if self._dir == Movement.LEFT:
            self._move_left()
        elif self._dir == Movement.RIGHT:
            self._move_right()
        super().update()

    def decide_direction(self):
        if random.random() < 0.03:  # so that it won't shake too much
            self._dir = random.choice([Movement.LEFT, Movement.RIGHT, Movement.IDLE])
