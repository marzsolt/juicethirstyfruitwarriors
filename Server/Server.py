import socket
import threading
import ServerCommunicator


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
            self.__host = socket.gethostname()
            self.__serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__serverSocket.bind((self.__host, self.__port_number))
            self.__serverSocket.listen(5)
            self.id_counter = 0

            self.__serverCommunicatorsList = []

    def receive_message(self, message, ID):
        print(f"Client {ID} sent:", message)
        message_split = message.split(";")
        if message_split[0] == "csoki":
            self.send_message("koszonom", ID)

    def __get_communicator_from_id(self, ID):
        for communicator in self.__serverCommunicatorsList:
            if communicator.ID == ID:
                return communicator
        raise ValueError("Invalid value of ID")

    def send_message(self, message, ID):
        communicator = self.__get_communicator_from_id(ID)
        communicator.send_message(message)

    def send_all(self, message):
        for communicators in self.__serverCommunicatorsList:
            communicators.send(message)

    def __new_client(self, _new_client):
        newCom = ServerCommunicator.ServerCommunicator(_server=self, _client=_new_client, ID=self.id_counter)
        newCom.start()
        self.__serverCommunicatorsList.append(newCom)
        self.send_message("kakao", newCom.ID)

        self.id_counter = self.id_counter + 1

    def __accept_clients(self):
        new_client, addr = self.__serverSocket.accept()
        print("got connection")
        self.__new_client(new_client)

    def run(self):
        while True:
            self.__accept_clients()


Server()
Server.get_instance().start()
