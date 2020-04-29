import socket
import threading
from collections import defaultdict
import logging

from src.Server.Network_communication.ServerCommunicator import ServerCommunicator
import src.Server.Network_communication.server_message_constants as sermess

import src.Client.Network_communication.client_message_constants as client_constants

from src.utils.BaseMessage import BaseMessage

from src.utils.domi_utils import id_generator


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
            self.logger = logging.getLogger('Domi.Server')
            self.__port_number = 12145
            self.__host = socket.gethostbyname(socket.gethostname())
            self.logger.info(f"Server IP address: {self.__host}.")
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

    def get_new_id(self):
        return next(self.__id_gen)

    def __new_client(self, _new_client):
        newCom = ServerCommunicator(_server=self, _client=_new_client, ID=next(self.__id_gen))
        newCom.start()
        self.__serverCommunicatorsList.append(newCom)

        # sending client id
        message = BaseMessage(mess_type=sermess.MessageType.YOUR_ID,
                                          target=sermess.Target.CLIENT)
        message.id = newCom.ID
        self.send_message(message, newCom.ID)

    def __accept_clients(self):
        new_client, addr = self.__serverSocket.accept()
        self.__new_client(new_client)

    def close_all_connection(self):
        for communicator in self.__serverCommunicatorsList:
            communicator.close()
            communicator.join()

    def run(self):
        while True:
            self.__accept_clients()
