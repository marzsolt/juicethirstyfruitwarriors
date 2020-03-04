import socket
from _thread import *
import ClientCommunicator

class Client:
    def __init__(self):
        host = socket.gethostname()  # or 'IP address'
        port = 12145  # Random port number
        self.communicator = ClientCommunicator.ClientCommunicator(self, host, port)

        self.communicator.start()
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host = socket.gethostname()  # or 'IP address'
        # port = 12145  # Random port number
        #
        # self.client_socket.connect((host, port))

    def receiveMessage(self, message):
        print("Server sent: ", message)
        message_split = message.split(";")
        if message_split[0] == "kakao":
            print("I sent: csoki")
            self.communicator.sendMessage("csoki")

    def run(self):
        while True:
            a=3

client = Client()