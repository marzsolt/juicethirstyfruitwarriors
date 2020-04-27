from juicethirstyfruitwarriors.Server.Player.AppleLogic import AppleLogic
from juicethirstyfruitwarriors.Server.PlayerAI.PlayerAILogic import PlayerAILogic


class AppleAI(PlayerAILogic, AppleLogic):
    def __init__(self, player_id, terrain):
        super(AppleAI, self).__init__(player_id, terrain)
