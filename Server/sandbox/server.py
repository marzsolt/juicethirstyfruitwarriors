import socket
import threading
import ClientReceiver
import ServerCommunicator


class Server(threading.Thread):

    def __init__(self):
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

    def send_message(self, message, ID):
        self.serverCommunicatorsList[ID].send(message)

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


    def run(self):
        client_receiver = ClientReceiver.ClientReceiver(_server=self)
        client_receiver.start()



server = Server()
server.start()