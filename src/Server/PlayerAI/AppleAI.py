from src.Server.Player.AppleLogic import AppleLogic
from src.Server.PlayerAI.PlayerAILogic import PlayerAILogic


class AppleAI(PlayerAILogic, AppleLogic):
    def __init__(self, player_id, terrain):
        super(AppleAI, self).__init__(player_id, terrain)
