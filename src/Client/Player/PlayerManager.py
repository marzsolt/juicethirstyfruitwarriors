from src.Client.Network_communication.Client import Client
from src.Client.Player.Player import Player, PicFile
from src.Client.Player.PlayerAI import PlayerAI
from src.Client.Player.ApplePlayer import ApplePlayer
from src.Client.Player.OrangePlayer import OrangePlayer


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

    def create_players(self, apple_human_ids, orange_human_ids, apple_ai_ids, orange_ai_ids):
        for player_id in apple_human_ids:
            self.players.append(ApplePlayer(player_id))
        for player_id in orange_human_ids:
            self.players.append(OrangePlayer(player_id))
        for player_id in apple_ai_ids:
            self.players.append(PlayerAI(player_id, PicFile.APPLE))
        for player_id in orange_ai_ids:
            self.players.append(PlayerAI(player_id, PicFile.ORANGE))

    def update(self, pressed_keys, events):
        for player in self.players:
            if player._id == Client.get_instance().id:
                player_keys = pressed_keys
                player_events = events
            else:
                player_keys = []
                player_events = []
            player.update(player_keys, player_events)

    def draw_players(self, screen):
        for p in self.players:
            screen.blit(p.surf, p.rect)


