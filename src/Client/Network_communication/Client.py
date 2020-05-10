from collections import defaultdict
import logging

from src.Client.Network_communication.ClientCommunicator import ClientCommunicator
import src.Server.Network_communication.server_message_constants as sermess
import src.Client.Network_communication.client_message_constants as climess
from src.utils.BaseMessage import BaseMessage
from src.utils.Timer import Timer


class Client:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Client.__instance is None:
            Client.__instance = Client()
        return Client.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Client.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.logger = logging.getLogger('Domi.Client')
            self.client_message_dictionary = defaultdict(list)
            self.__communicator = None
            self.id = None
            self.__processed_important_message_ids = {}

            # connection related information
            self.connection_alive = None

    def setup_connection(self, ip):
        host = ip
        port = 12145  # Random port number
        self.__communicator = ClientCommunicator(self, host, port)
        self.__communicator.start()

    def close_connection(self):
        """ If the connection was alive, then it closes down, i.e.:
            - notify Game, so that it can be killed if isn't already;
            - notify Server, so that it can kill its communicator.
            - finally, closing communicator. """
        if self.connection_alive:
            msg = BaseMessage(climess.MessageType.CONN_RELATED_DEATH, climess.Target.GAME)
            msg.player_id = self.id
            self.send_message(msg)

            msg = BaseMessage(climess.MessageType.CONN_CLOSED, climess.Target.SERVER)
            self.send_message(msg)

            self.__communicator.close()

    def receive_message(self, message):
        """When message is received, first the message importance is checked, then the message gets processed"""
        if message.important:
            if message.mes_id not in self.__processed_important_message_ids:
                self._process_message(message)
                self.__processed_important_message_ids[message.mes_id] = False
            else:
                # it is possible to get the same message twice if the ack gets lost
                # but in this case the client already processed it
                self.__processed_important_message_ids[message.mes_id] = True
            # client sends back the acknowledgement
            msg = BaseMessage(mess_type=climess.MessageType.ACK, target=climess.Target.SERVER_COMMUNICATOR)
            msg.mes_id = message.mes_id
            self.send_message(msg)
            Timer.sch_fun(3, self._del_from_message_ids, (message,))
        else:
            self._process_message(message)

    def _del_from_message_ids(self, message):
        # the important message ids are stored in a list, but there is no need for all of them
        # if a message was not send again in certain time, the ack arrived to the server and the message can be deleted
        if not self.__processed_important_message_ids[message.mes_id]:
            del self.__processed_important_message_ids[message.mes_id]
        else:
            self.__processed_important_message_ids[message.mes_id] = True
            Timer.sch_fun(3, self._del_from_message_ids, (message, ))

    def _process_message(self, message):
        """Groups the messages according to their purposes"""
        if message.type == sermess.MessageType.DIED:
            self.logger.debug(f"Player {message.player_id} died message received.")
        if message.target == sermess.Target.CLIENT:
            if message.type == sermess.MessageType.YOUR_ID:
                self.logger.info(f"I got my id: {message.id}")
                self.id = message.id
        else:
            self.client_message_dictionary[message.target].append(message)  # stores messages for different targets

    def get_targets_messages(self, target):
        """The different targets (players, game, server) query their messages from client through this function"""
        messages = self.client_message_dictionary.get(target) or []
        if messages is not []:
            self.client_message_dictionary[target] = []
        return messages

    def send_message(self, message):
        message.important = False  # the less important messages are sent in nearly every frame e.g. player movement
        self.__communicator.send_message(message)

    def send_important_message(self, message):
        """Some messages are particularly important not to get lost
        so when the communicator send them, it uses acknowledgement protocol"""
        message.important = True
        self.__communicator.send_important_message(message)
