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
            self.port_number = 12145
            self.host = socket.gethostname()
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind((self.host, self.port_number))
            self.serverSocket.listen(5)
            self.id_counter = 0

            self.serverCommunicatorsList = []
            self.IDs = []

    def close(self):
        self.s.close()

    def receive_message(self, message, ID):
        print(f"Client {ID} sent:", message)
        message_split = message.split(";")
        if message_split[0] == "csoki":
            self.serverCommunicatorsList[ID].send_message("koszonom")

    def get_communicator_from_id(self, ID):
        for communicator in self.serverCommunicatorsList:
            if communicator.ID == ID:
                return communicator
        raise ValueError("Unexpected value of ID")

    def send_message(self, message, ID):
        communicator = self.get_communicator_from_id(ID)
        communicator.send(message)

    def send_all(self, message):
        for communicators in self.serverCommunicatorsList:
            communicators.send(message)

    def new_client(self, _new_client):
        newCom = ServerCommunicator.ServerCommunicator(_server=self, _client=_new_client, ID=self.id_counter)
        newCom.start()
        self.serverCommunicatorsList.append(newCom)
        self.IDs.append(self.id_counter)

        newCom.send_message("kakao")

        self.id_counter = self.id_counter + 1

    def accept_clients(self):
        new_client, addr = self.serverSocket.accept()
        print("got connection")
        self.new_client(new_client)

    def run(self):
        while True:
            self.accept_clients()


Server()
Server.get_instance().start()
