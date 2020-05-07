from enum import Enum
import random
import abc

from src.Server.Player.PlayerLogic import PlayerLogic
from src.utils.Vector2D import Vector2D


class Movement(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    IDLE = "IDLE"


class PlayerAILogic(PlayerLogic, abc.ABC):
    def __init__(self, player_id, __terrain, game):
        super(PlayerAILogic, self).__init__(player_id, __terrain, game)
        self._dir = Movement.RIGHT
        self._fear_level = random.random()
        self._go_towards_enemy = True
        # Attacks if the closest enemy is within this distance, derived classes shall overwrite!
        self._attack_range = 100

    def update(self):
        self._update_fear_level()
        if random.random() < 0.05:  # don't change mind all the time
            self._update_go_towards_enemy()
        if self.__enemy_in_range() and random.random() < 0.75:  # some unpredictability to attack
            self._attack_if_can()
        else:
            self._movement()
        super().update()

    def _update_fear_level(self):
        self._fear_level += random.random() * 0.01 - 0.005
        self._fear_level = max(0, self._fear_level)
        self._fear_level = min(1, self._fear_level)

    def _update_go_towards_enemy(self):
        self._go_towards_enemy = (random.random() > self._fear_level)

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
        enemy_to_right = (cp.pos.x > self.pos.x)
        if enemy_to_right == self._go_towards_enemy:
            self._dir = Movement.RIGHT
        else:
            self._dir = Movement.LEFT

    def _attack_if_can(self):
        if self.can_attack():
            self._attack()

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
