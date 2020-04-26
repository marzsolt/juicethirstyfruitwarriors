from juicethirstyfruitwarriors.Server.AppleLogic import AppleLogic
from juicethirstyfruitwarriors.Server.PlayerAILogic import PlayerAILogic


class AppleAI(PlayerAILogic, AppleLogic):
    def __init__(self, player_id, terrain):
        super(AppleAI, self).__init__(player_id, terrain)
