import OrangeLogic
import PlayerAILogic


class OrangeAI(PlayerAILogic.PlayerAILogic, OrangeLogic.OrangeLogic):
    def __init__(self, player_id, terrain):
        super(OrangeAI, self).__init__(player_id, terrain)
