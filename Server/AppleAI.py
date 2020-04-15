import AppleLogic
import PlayerAILogic


class AppleAI(PlayerAILogic.PlayerAILogic, AppleLogic.AppleLogic):
    def __init__(self, player_id, terrain):
        super(AppleAI, self).__init__(player_id, terrain)
