import time
import logging

from src.Server.Network_communication.Server import Server
from src.Server.Player.PlayerLogic import PlayerLogic
from src.Server.Player.OrangeLogic import OrangeLogic
from src.Server.Player.AppleLogic import AppleLogic
from src.Server.PlayerAI.OrangeAI import OrangeAI
from src.Server.PlayerAI.AppleAI import AppleAI
from src.Server.PlayerAI.PlayerAILogic import PlayerAILogic
from src.Server.Game.Terrain import Terrain
from src.utils.Timer import Timer
import src.Server.Network_communication.server_message_constants as sermess

import src.Client.Network_communication.client_message_constants as climess

from src.utils.BaseMessage import BaseMessage


class Game:
    def __init__(self):
        self.logger = logging.getLogger('Domi.Game')
        self.__game_started = False
        self.__chose_host = False
        self.__AI_number = 2
        self.__human_player_number = 2  # remember to adjust this default with screen's first player's selector's
        self.__first_player_id = None
        self.__player_logics = []
        self.__terrain = Terrain()
        self.running = True

    def update(self):
        self.__read_messages()
        if not self.__game_started:
            self.__collect_players()
        else:
            # TODO move this part into a separate function
            # Check if all human player is dead:
            is_there_human = False
            for pl in self.__player_logics:
                if not isinstance(pl, PlayerAILogic):
                    is_there_human = True
            if not is_there_human:
                mess = BaseMessage(sermess.MessageType.NO_ALIVE_HUMAN, sermess.Target.SCREEN)
                Server.get_instance().send_all(mess)
                print("Game killed as no human players left.")
                Timer.sch_fun(1, self.stop_running, ())  # so that clients get the message

            else:
                for i, pl_i in enumerate(self.__player_logics):
                    # HP update for each player:
                    for pl_j in self.__player_logics[i + 1:]:
                        if (abs(pl_i.pos.x - pl_j.pos.x) <= 2 * PlayerLogic.RADIUS and
                                abs(pl_i.pos.y - pl_j.pos.y) <= 2 * PlayerLogic.RADIUS):
                            pl_i.hp -= 1 if pl_i.hp != 0 else 0
                            pl_j.hp -= 1 if pl_j.hp != 0 else 0
                    pl_i.update()

                # Check for deaths:
                for pl in self.__player_logics:
                    if pl.hp == 0:
                        print("ID: ", pl._id, " Player has just died.")
                        mess = BaseMessage(sermess.MessageType.DIED, sermess.Target.SCREEN)
                        mess.player_id = pl._id
                        Server.get_instance().send_all(mess)
                        print("ID: ", pl._id, " All clients has been notified about the recent tragic death.")
                        self.__player_logics = \
                            [player_logic for player_logic in self.__player_logics if player_logic._id != pl._id]
                        print("ID: ", pl._id, " Player logic killed.")

            # Check if there's a winner (last alive)
            if len(self.__player_logics) == 1 and is_there_human:
                mess = BaseMessage(sermess.MessageType.WON, sermess.Target.SCREEN)
                mess.player_id = self.__player_logics[0]._id
                Server.get_instance().send_all(mess)
                Timer.sch_fun(1, self.stop_running, ())  # so that clients get the message

        return self.running

    def stop_running(self):
        self.running = False

    def get_players(self):
        return self.__player_logics

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
        self.logger.info("Game started, terrain sent to everyone")
        self.__game_started = True

        human_ids = Server.get_instance().get_client_ids()
        orange_human_ids = []
        apple_human_ids = []
        orange_ai_ids = []
        apple_ai_ids = []
        for player_id in human_ids:  # create server side players for humans
            if player_id % 2 != 0:  # TODO this distribution is only for testing!
                new_player_logic = AppleLogic(player_id, self.__terrain)
                apple_human_ids.append(player_id)
            else:
                new_player_logic = OrangeLogic(player_id, self.__terrain)
                orange_human_ids.append(player_id)
            self.__player_logics.append(new_player_logic)
        for i in range(self.__AI_number):  # create server side players for AIs
            player_id = Server.get_instance().get_new_id()

            if player_id % 2 == 0:  # TODO this distribution is only for testing!
                new_player_logic = AppleAI(player_id, self.__terrain, self)
                apple_ai_ids.append(player_id)
            else:
                new_player_logic = OrangeAI(player_id, self.__terrain, self)
                orange_ai_ids.append(player_id)
            self.__player_logics.append(new_player_logic)

        mess = BaseMessage(sermess.MessageType.INITIAL_DATA, sermess.Target.SCREEN)
        mess.apple_human_ids = apple_human_ids
        mess.orange_human_ids = orange_human_ids
        mess.apple_ai_ids = apple_ai_ids
        mess.orange_ai_ids = orange_ai_ids
        mess.terrain_points = self.__terrain.get_terrain_points()
        mess.terrain_points_levels = [self.__terrain.get_level(point) for point in self.__terrain.get_terrain_points()]
        Server.get_instance().send_all(mess)

    def __read_messages(self):
        messages = Server.get_instance().get_targets_messages(climess.Target.GAME)
        for mess in messages:
            if mess.type == climess.MessageType.CHANGE_PLAYER_NUMBER and mess.from_id == self.__first_player_id:
                # TODO do not allow less than currently connected if we have time...
                self.__human_player_number = mess.new_number
                self.logger.info(f"Changed player number, new is: {mess.new_number}.")
            elif mess.type == climess.MessageType.START_GAME_MANUALLY and mess.from_id == self.__first_player_id:
                self.logger.info("Received manual game start signal.")
                self.__start_game()
            elif mess.type == climess.MessageType.CONN_RELATED_DEATH:
                for pl in self.__player_logics:
                    if pl._id == mess.player_id:
                        print("ID: ", mess.player_id, " Connection related death.")
                        pl.hp = 0
