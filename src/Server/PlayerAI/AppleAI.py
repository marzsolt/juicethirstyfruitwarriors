from src.Server.Player.AppleLogic import AppleLogic
from src.Server.PlayerAI.PlayerAILogic import PlayerAILogic


class AppleAI(PlayerAILogic, AppleLogic):
    def __init__(self, player_id, terrain, game):
        super(AppleAI, self).__init__(player_id, terrain, game)

    def _attack(self):
        if super()._attack():
            pass  # TODO find appropriate
        return False

    def _enemy_in_range(self):
        return False
