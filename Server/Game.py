from Server import Server
import client_message_constants as climess
import server_message_constants as sermess
from BaseMessage import BaseMessage


class Game:
    def __init__(self):
        self.__game_started = False
        self.__AI_number = 3
        self.__human_player_number = 2
        self.__first_player_id = None

    def update(self):
        self.__read_messages()
        if not self.__game_started:
            self.__collect_players()
        else:
            pass

    def __collect_players(self):
        connected_players = Server.get_instance().get_client_ids()
        if len(connected_players) == 1:
            self.__first_player_id = connected_players[0]
            mess = BaseMessage(sermess.MessageType.FIRST_PLAYER, sermess.Target.SCREEN)
            Server.get_instance().send_message(mess, self.__first_player_id)
        if len(connected_players) == self.__human_player_number:
            self.__start_game()

    def __start_game(self):
        print("Game started")
        self.__game_started = True
        mess = BaseMessage(sermess.MessageType.GAME_STARTED, sermess.Target.SCREEN)
        Server.get_instance().send_all(mess)
        # TODO:
        # Create PlayerLogics -> Players, PlayerManager on client side
        # Player positions to everyone - players position message generator

    def __read_messages(self):
        messages = Server.get_instance().get_targets_messages(climess.Target.GAME)
        for mess in messages:
            if mess.type == climess.MessageType.CHANGE_PLAYER_NUMBER and mess.from_id == self.__first_player_id:
                # TODO do not allow less than currently connected if we have time...
                self.__human_player_number = mess.new_number
