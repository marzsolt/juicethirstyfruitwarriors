import random

from src.Server.Player.AppleLogic import AppleLogic
from src.Server.PlayerAI.PlayerAILogic import PlayerAILogic


class AppleAI(PlayerAILogic, AppleLogic):
    def __init__(self, player_id, terrain, game):
        super(AppleAI, self).__init__(player_id, terrain, game)
        self._attack_range = 150

    def _attack(self):
        cp = self._get_closest_enemy()
        dx = cp.pos.x - self.pos.x
        force_of_jump = self._calculate_attack_force(self.pos.x + dx*3/4, self.pos.y + 300)
        super()._attack(force=force_of_jump)

    def _update_go_towards_enemy(self):
        """ Apple AIs tend to be more and more fearful as their hp decreases. """
        super()._update_go_towards_enemy()
        if self._go_towards_enemy and self.hp/self.max_hp < random.random():
            self._go_towards_enemy = True

