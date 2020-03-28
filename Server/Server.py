import socket
import threading
from collections import defaultdict
import ServerCommunicator
from utils.domi_utils import id_generator
import server_message_constants
import client_message_constants as client_constants
import BaseMessage


class Server(threading.Thread):
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Server.__instance is None:
            Server.__instance = Server()
        return Server.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Server.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            threading.Thread.__init__(self)
            self.__port_number = 12145
            self.__host = socket.gethostbyname(socket.gethostname())
            print(self.__host)
            self.__serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__serverSocket.bind((self.__host, self.__port_number))
            self.__serverSocket.listen(5)
            self.__id_gen = id_generator()
            self.__serverCommunicatorsList = []
            self.server_message_dictionary = defaultdict(list)

    def receive_message(self, message, ID):
        if message.target == client_constants.Target.SERVER:
            pass
        else:
            message.from_id = ID
            self.server_message_dictionary[message.target].append(message)

    def get_targets_messages(self, target):
        messages = self.server_message_dictionary.get(target) or []
        if messages is not []:
            self.server_message_dictionary[target] = []
        return messages

    def get_client_ids(self):
        return [com.ID for com in self.__serverCommunicatorsList]

    def __get_communicator_from_id(self, ID):
        for communicator in self.__serverCommunicatorsList:
            if communicator.ID == ID:
                return communicator
        raise ValueError("Invalid value of ID", ID)

    def send_message(self, message, ID):
        communicator = self.__get_communicator_from_id(ID)
        communicator.send_message(message)

    def send_all(self, message):
        for communicators in self.__serverCommunicatorsList:
            communicators.send_message(message)

    def __new_client(self, _new_client):
        newCom = ServerCommunicator.ServerCommunicator(_server=self, _client=_new_client, ID=next(self.__id_gen))
        newCom.start()
        self.__serverCommunicatorsList.append(newCom)

        # sending client id
        message = BaseMessage.BaseMessage(mess_type=server_message_constants.MessageType.YOUR_ID,
                                          target=server_message_constants.Target.CLIENT)
        message.id = newCom.ID
        self.send_message(message, newCom.ID)

    def __accept_clients(self):
        new_client, addr = self.__serverSocket.accept()
        self.__new_client(new_client)

    def run(self):
        while True:
            self.__accept_clients()
