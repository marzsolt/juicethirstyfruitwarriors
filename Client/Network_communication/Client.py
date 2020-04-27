from collections import defaultdict

from juicethirstyfruitwarriors.Client.Network_communication.ClientCommunicator import ClientCommunicator
import juicethirstyfruitwarriors.Server.Network_communication.server_message_constants as sermess


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
            self.id = None

            # connection related information
            self.connection_alive = None

    def setup_connection(self, ip):
        host = ip
        port = 12145  # Random port number
        self.__communicator = ClientCommunicator(self, host, port)
        self.__communicator.start()

    def receive_message(self, message):
        if message.target == sermess.Target.CLIENT:
            if message.type == sermess.MessageType.YOUR_ID:
                print("My id is:", message.id)
                self.id = message.id
        else:
            self.client_message_dictionary[message.target].append(message)

    def get_targets_messages(self, target):
        messages = self.client_message_dictionary.get(target) or []
        if messages is not []:
            self.client_message_dictionary[target] = []
        return messages

    def send_message(self, message):
        self.__communicator.send_message(message)
        
