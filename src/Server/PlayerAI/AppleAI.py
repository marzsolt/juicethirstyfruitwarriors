from src.Server.Player.AppleLogic import AppleLogic
from src.Server.PlayerAI.PlayerAILogic import PlayerAILogic
from src.utils.Vector2D import Vector2D


class AppleAI(PlayerAILogic, AppleLogic):
    def __init__(self, player_id, terrain, game):
        super(AppleAI, self).__init__(player_id, terrain, game)
        self._attack_range = 150  # TODO compute it normally

    def _attack(self):
        force_of_jump = self._calculate_attack_force(self.pos.x, self.pos.y + 100) # TODO egyelőre csak felfele ugrik egyet
        if super()._attack(force=force_of_jump):
            pass  # TODO find appropriate
        return False

