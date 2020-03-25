import threading
import json


class ServerCommunicator(threading.Thread):
    def __init__(self, _server, _client, ID):
        threading.Thread.__init__(self)
        self.server = _server
        self.socket = _client
        self.ID = ID

    def send_message(self, message):
        #message = str.encode(message)
        #self.socket.send(message)
        serialized = json.dumps(message.__dict__)
        serialized = str.encode(serialized)
        #self.socket.send(bytes(len(serialized)))
        self.socket.send(serialized)

    def run(self):
        while True:
            message = self.socket.recv(1024)
            message = message.decode()
            deserialized = json.loads(message)
            self.server.receive_message(deserialized, self.ID)
