from src.Server.Player.OrangeLogic import OrangeLogic
from src.Server.PlayerAI.PlayerAILogic import PlayerAILogic


class OrangeAI(PlayerAILogic, OrangeLogic):
    def __init__(self, player_id, terrain, game):
        super(OrangeAI, self).__init__(player_id, terrain, game)
