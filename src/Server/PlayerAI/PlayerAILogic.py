from enum import Enum
import random

from src.Server.Player.PlayerLogic import PlayerLogic
from src.utils.Vector2D import Vector2D


class Movement(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    IDLE = "IDLE"


class PlayerAILogic(PlayerLogic):
    def __init__(self, player_id, __terrain, game):
        super(PlayerAILogic, self).__init__(player_id, __terrain)
        self._game = game
        self._dir = Movement.RIGHT
        # Attacks if the closest enemy is within this distance, derived classes shall overwrite!
        self._attack_range = 100

    def update(self):
        if self.__enemy_in_range():
            self._attack()
        else:
            self._movement()
        super().update()

    def _movement(self):
        """ Moves the AI. """
        self._decide_direction()
        if self._dir == Movement.LEFT:
            self._move_left()
        elif self._dir == Movement.RIGHT:
            self._move_right()

    def _decide_direction(self):
        """ Sets dir so that it will move towards the nearest other player. """
        cp = self._get_closest_enemy()
        if cp.pos.x < self.pos.x:
            self._dir = Movement.LEFT
        else:
            self._dir = Movement.RIGHT

    def __random_movement(self):
        if random.random() < 0.03:  # so that it won't shake too much
            self._dir = random.choice([Movement.LEFT, Movement.RIGHT, Movement.IDLE])

    def __enemy_in_range(self):
        closest_enemy = self._get_closest_enemy()
        dist_square = Vector2D.dist_square(self.pos, closest_enemy.pos)
        return dist_square < self._attack_range**2

    def _get_closest_enemy(self):
        """ Returns the closest other player. If alone, it returns None. """
        players = self._game.get_players()
        if len(players) == 1:  # no other player...
            return None
        min_dist_square = 10**8  # big enough to not be min
        disted_players = [(Vector2D.dist_square(p.pos, self.pos), p) if p.get_id() != self._id else (min_dist_square, p)
                          for p in players]  # distance2 - player tuple list
        closest_p = min(disted_players, key=lambda dp: dp[0])  # find min by distance2
        return closest_p[1]
