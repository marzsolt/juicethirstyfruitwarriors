from _thread import *
import threading


class ServerCommunicator(threading.Thread):
    def __init__(self, _server, _client, ID):
        threading.Thread.__init__(self)
        self.server = _server
        self.socket = _client
        self.ID = ID

        #start_new_thread(self.run())

    def sendMessage(self, message):
        message = str.encode(message)

        self.socket.send(message)

    def run(self):
        while True:
            message = self.socket.recv(1024)
            message = message.decode()
            self.server.receiveMessage(message, self.ID)
