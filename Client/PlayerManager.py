from Player import Player
from PlayerAI import PlayerAI
from Client import Client


class PlayerManager:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if PlayerManager.__instance is None:
            PlayerManager.__instance = PlayerManager()
        return PlayerManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if PlayerManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.players = []

    def create_players(self, player_ids, ai_ids):
        for player_id in player_ids:
            self.players.append(Player(player_id=player_id))
        for player_id in ai_ids:
            self.players.append(PlayerAI(player_id=player_id))

    def update(self, pressed_keys):
        for player in self.players:
            if player._id == Client.get_instance().id:
                player_keys = pressed_keys
            else:
                player_keys = []
            player.update(player_keys)

    def draw_players(self, screen):
        for p in self.players:
            screen.blit(p.surf, p.rect)


