import socket
from _thread import *
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

        #start_new_thread(self.run(), (self,))

    def close(self):
        self.s.close()

    def receiveMessage(self, message, ID):
        print(f"Client {ID} sent:", message)
        message_split = message.split(";")
        if message_split[0] == "csoki":
            self.serverCommunicatorsList[ID].sendMessage("koszonom")

    def newClient(self, _newClient):
        newCom = ServerCommunicator.ServerCommunicator(_server=self, _client=_newClient, ID=self.id_counter)
        newCom.start()
        self.serverCommunicatorsList.append(newCom)
        self.IDs.append(self.id_counter)

        newCom.sendMessage("kakao")

        self.id_counter = self.id_counter + 1

    def settings(self):
        clientReceiver = ClientReceiver.ClientReceiver(_server=self)
        clientReceiver.start()

    def run(self):
        self.settings()



server = Server()
server.start()