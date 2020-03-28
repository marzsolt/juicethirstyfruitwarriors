import socket
import threading
from collections import defaultdict
import ServerCommunicator
from utils.domi_utils import id_generator
import server_message_constants
import Client.client_message_constants as client_constants
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
        self.server_message_dictionary[message.target].append(message)
        if message.type == client_constants.MessageType.CONN:
            print(message.text)

    def get_targets_messages(self, target):
        messages = self.client_message_dictionary.get(target) or []
        if messages is not []:
            self.server[target] = []
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
            communicators.send(message)

    def __new_client(self, _new_client):
        newCom = ServerCommunicator.ServerCommunicator(_server=self, _client=_new_client, ID=next(self.__id_gen))
        newCom.start()
        self.__serverCommunicatorsList.append(newCom)
        message = BaseMessage.BaseMessage(mess_type=server_message_constants.MessageType.CONN, target=server_message_constants.Target.CLIENT)
        message.text = "Connected to server"
        self.send_message(message, newCom.ID)

    def __accept_clients(self):
        new_client, addr = self.__serverSocket.accept()
        print("got connection")
        self.__new_client(new_client)

    def run(self):
        while True:
            self.__accept_clients()
