import random

from src.Server.Player.OrangeLogic import OrangeLogic
from src.Server.PlayerAI.PlayerAILogic import PlayerAILogic


class OrangeAI(PlayerAILogic, OrangeLogic):
    def __init__(self, player_id, terrain, game):
        super(OrangeAI, self).__init__(player_id, terrain, game)
        self._attack_range = 100
        self._aggression_bias = 0.5


    def _update_go_towards_enemy(self):
        """ Orange AIs tend to be more aggressive as their movement determines their attack direction. """
        super()._update_go_towards_enemy()
        if not self._go_towards_enemy and random.random() < self._aggression_bias:
            self._go_towards_enemy = True
