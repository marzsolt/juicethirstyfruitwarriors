from Player import Player
from PlayerAI import PlayerAI


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

    def create_player(self, player_ids, ai_ids):
        for player_id in player_ids:
            self.players.append(Player(player_id=player_id))
        for player_id in ai_ids:
            self.players.append(PlayerAI(player_id=player_id))

    def update(self, events, pressed_keys, client_id):
        for player in self.players:
            if player._id == client_id:
                player_events = events
                player_keys = pressed_keys
            else:
                player_events = []
                player_keys = []
            player.update(player_events, player_keys)

    def draw_players(self, screen):
        for p in self.players:
            screen.blit(p.surf, p.rect)


