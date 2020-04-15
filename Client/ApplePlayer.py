import Player


class ApplePlayer(Player.Player):
    def __init__(self, player_id):
        super(ApplePlayer, self).__init__(player_id, Player.PicFile.APPLE)
