import socket
from _thread import *
import threading

class ClientCommunicator(threading.Thread):
    def __init__(self, _client, host, port):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket.connect((host, port))

        self.client = _client
        #start_new_thread(self.run())


    def sendMessage(self, message):
        message = str.encode(message)
        self.client_socket.send(message)

    def run(self):
        while True:
            message = self.client_socket.recv(1024)
            message = message.decode()
            self.client.receiveMessage(message)