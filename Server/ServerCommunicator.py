import threading
import json


class ServerCommunicator(threading.Thread):
    def __init__(self, _server, _client, ID):
        threading.Thread.__init__(self)
        self.server = _server
        self.socket = _client
        self.ID = ID

    def send_message(self, message):
        serialized = json.dumps(message.__dict__)
        serialized = str.encode(serialized)
        self.socket.send(serialized)

    def __dict_to_object(self, dictionary):
        obj = type('new', (object,), dictionary)
        for key in dictionary:
            setattr(obj, key, dictionary[key])
        return obj

    def run(self):
        while True:
            message = self.socket.recv(1024)
            message = message.decode()
            deserialized = json.loads(message)
            deserialized = self.__dict_to_object(deserialized)
            self.server.receive_message(deserialized, self.ID)
