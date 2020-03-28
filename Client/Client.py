from collections import defaultdict
import ClientCommunicator
import client_message_constants
import Server.server_message_constants as server_constants
import BaseMessage


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
            self.client_message_dictionary = defaultdict(list)
            self.__communicator = None

            # connection related information
            self.connection_alive = None

    def setup_connection(self, ip):
        host = ip
        port = 12145  # Random port number
        self.__communicator = ClientCommunicator.ClientCommunicator(self, host, port)
        self.__communicator.start()

    def receive_message(self, message):
        self.client_message_dictionary[message.target].append(message)
        if message.type == server_constants.MessageType.CONN:
            print("Server sent:", message.text)
            mess = BaseMessage.BaseMessage(mess_type=client_message_constants.MessageType.CONN, target=client_message_constants.Target.SERVER)
            mess.text = "Connection is ok"
            self.send_message(mess)

    def get_targets_messages(self, target):
        messages = self.client_message_dictionary.get(target) or []
        if messages is not []:
            self.client_message_dictionary[target] = []
        return messages

    def send_message(self, message):
        self.__communicator.send_message(message)
