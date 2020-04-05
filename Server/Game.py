import time

from Server import Server
import client_message_constants as climess
import server_message_constants as sermess
from BaseMessage import BaseMessage
from PlayerLogic import PlayerLogic
from PlayerAILogic import PlayerAILogic


class Game:
    def __init__(self):
        self.__game_started = False
        self.__chose_host = False
        self.__AI_number = 2
        self.__human_player_number = 2  # remember to adjust this default with screen's first player's selector's
        self.__first_player_id = None
        self.__player_logics = []

    def update(self):
        self.__read_messages()
        if not self.__game_started:
            self.__collect_players()
        else:
            for pl in self.__player_logics:
                pl.update()
                time.sleep(0.001)  # TODO remove this!

    def __collect_players(self):
        connected_players = Server.get_instance().get_client_ids()
        if len(connected_players) == 1 and not self.__chose_host:
            self.__chose_host = True
            self.__first_player_id = connected_players[0]
            mess = BaseMessage(sermess.MessageType.FIRST_PLAYER, sermess.Target.SCREEN)
            Server.get_instance().send_message(mess, self.__first_player_id)
        if len(connected_players) == self.__human_player_number:
            self.__start_game()

    def __start_game(self):
        print("Game started")
        self.__game_started = True

        human_ids = Server.get_instance().get_client_ids()
        ai_ids = []
        for player_id in human_ids:  # create server side players for humans
            self.__player_logics.append(PlayerLogic(player_id))
        for i in range(self.__AI_number):  # create server side players for AIs
            new_id = Server.get_instance().get_new_id()
            self.__player_logics.append(PlayerAILogic(new_id))
            ai_ids.append(new_id)

        mess = BaseMessage(sermess.MessageType.GAME_STARTED, sermess.Target.SCREEN)
        mess.human_ids = human_ids
        mess.ai_ids = ai_ids
        Server.get_instance().send_all(mess)

    def __read_messages(self):
        messages = Server.get_instance().get_targets_messages(climess.Target.GAME)
        for mess in messages:
            if mess.type == climess.MessageType.CHANGE_PLAYER_NUMBER and mess.from_id == self.__first_player_id:
                # TODO do not allow less than currently connected if we have time...
                self.__human_player_number = mess.new_number
                print("Changed player number, new is: ", mess.new_number)
            elif mess.type == climess.MessageType.START_GAME_MANUALLY and mess.from_id == self.__first_player_id:
                print("Received manual game start signal.")
                self.__start_game()
