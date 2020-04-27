import threading
import json

from src.utils.domi_utils import dict_to_object


class ServerCommunicator(threading.Thread):
    def __init__(self, _server, _client, ID):
        threading.Thread.__init__(self)
        self.server = _server
        self.socket = _client
        self.ID = ID

    def send_message(self, message):
        serialized = json.dumps(json.dumps(message, default=lambda o: getattr(o, '__dict__', str(o))))  # recursive
        serialized = str.encode(serialized)
        self.socket.send(serialized)

    def run(self):
        while True:
            message = self.socket.recv(1024)
            message = message.decode()
            deserialized = json.loads(message)
            deserialized = dict_to_object(deserialized)
            self.server.receive_message(deserialized, self.ID)
