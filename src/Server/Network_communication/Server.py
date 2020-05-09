import socket
import threading
from collections import defaultdict
import logging

from src.Server.Network_communication.ServerCommunicator import ServerCommunicator
import src.Server.Network_communication.server_message_constants as sermess

import src.Client.Network_communication.client_message_constants as climess

from src.utils.BaseMessage import BaseMessage
from src.utils.Timer import Timer
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
            self.server_message_dictionary = defaultdict(list)  # stores the received messages grouped by the target
            self.__processed_important_message_ids = {}
            self.running = True

    def receive_message(self, message, ID):
        if message.important:
            if message.mes_id not in self.__processed_important_message_ids:
                self._process_message(message, ID)
                self.__processed_important_message_ids[message.mes_id] = False
            else:
                self.__processed_important_message_ids[message.mes_id] = True
            msg = BaseMessage(mess_type=sermess.MessageType.ACK, target=sermess.Target.CLIENT_COMMUNICATOR)
            msg.mes_id = message.mes_id
            self.send_message(msg, ID)
            Timer.sch_fun(3, self._del_from_message_ids, (message,))
        else:
            self._process_message(message, ID)

    def _del_from_message_ids(self, message):
        if not self.__processed_important_message_ids[message.mes_id]:
            del self.__processed_important_message_ids[message.mes_id]
        else:
            self.__processed_important_message_ids[message.mes_id] = True
            Timer.sch_fun(3, self._del_from_message_ids, (message,))

    def _process_message(self, message, ID):
        if message.target == climess.Target.SERVER:  # processes own messages
            if message.type == climess.MessageType.CONN_CLOSED:
                self.close_connection_by_id(ID)
        else:
            message.from_id = ID
            self.server_message_dictionary[message.target].append(message)  # stores messages for the other targets

    def get_targets_messages(self, target):
        """The targets can query their messages from here"""
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
        message.important = False
        communicator.send_message(message)

    def send_all(self, message):
        message.important = False
        for communicators in self.__serverCommunicatorsList:
            communicators.send_message(message)

    def send_important_message(self, message, ID):
        message.important = True
        communicator = self.__get_communicator_from_id(ID)
        communicator.send_important_message(message)

    def send_important_mes_all(self, message):
        message.important = True
        for communicators in self.__serverCommunicatorsList:
            communicators.send_important_message(message)

    def get_new_id(self):
        return next(self.__id_gen)

    def __new_client(self, _new_client):
        """When a client connects it gets a new servercommunicator and sends to the client its ID"""
        newCom = ServerCommunicator(_server=self, _client=_new_client, ID=next(self.__id_gen))
        newCom.start()
        self.__serverCommunicatorsList.append(newCom)

        # sending client id
        message = BaseMessage(mess_type=sermess.MessageType.YOUR_ID, target=sermess.Target.CLIENT)
        message.id = newCom.ID
        self.send_message(message, newCom.ID)

    def __accept_clients(self):
        try:
            new_client, addr = self.__serverSocket.accept()
        except OSError:  # if the socket was closed by interrupting it
            self.running = False
        else:
            self.__new_client(new_client)

    def close_connection_by_id(self, ID):
        """" Responsible for closing connection by client ID. """
        self.__get_communicator_from_id(ID).close()
        self.__serverCommunicatorsList = [comm for comm in self.__serverCommunicatorsList if comm.ID != ID]

        if len(self.__serverCommunicatorsList) == 0:  # if no more connection with player, shut down server socket.
            self.__serverSocket.close()
            self.logger.info("Server socket closed.")

    def stop_accepting_clients(self):
        self.running = False

    def run(self):
        while self.running:
            self.__accept_clients()
