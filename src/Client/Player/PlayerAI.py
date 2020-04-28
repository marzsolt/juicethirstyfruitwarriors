from src.Client.Player.Player import Player


class PlayerAI(Player):
    def __init__(self, player_id, pic_file):
        super(PlayerAI, self).__init__(player_id, pic_file)

    def update(self, pressed_keys, events):  # override player's update
        self.pos_hp_update()
