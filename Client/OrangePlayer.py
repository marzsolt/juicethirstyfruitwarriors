import Player


class OrangePlayer(Player.Player):
    def __init__(self, player_id):
        super(OrangePlayer, self).__init__(player_id, Player.PicFile.ORANGE)
