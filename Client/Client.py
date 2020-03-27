from collections import defaultdict
import ClientCommunicator
import client_message_constants
import Server.server_message_constants as server_constants
import BaseMessage


class Client:
    __instance = None

    @staticmethod
    def get_instance(ip, bucket):  # TODO ip and bucket shouldn't be required! It would make the usage awful!
        """ Static access method. """
        if Client.__instance is None:
            Client.__instance = Client(ip, bucket)
        return Client.__instance

    def __init__(self, ip, bucket):
        """ Virtually private constructor. """
        if Client.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.client_message_dictionary = defaultdict(list)
            self.__create_communicator(ip, bucket)

    def change_ip(self, ip, bucket):
        if Client.__instance is None:
            Client.__instance = Client(ip, bucket)
        else:
            self.__create_communicator(ip, bucket)

    def __create_communicator(self, ip, bucket):
        host = ip
        port = 12145  # Random port number
        self.__communicator = ClientCommunicator.ClientCommunicator(self, host, port, bucket)

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
