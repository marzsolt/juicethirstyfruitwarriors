import threading
import json
from utils.domi_utils import dict_to_object, separate_jsons


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

    def run(self):
        while True:
            message = self.socket.recv(1024)
            message = message.decode()
            
            mes_separated = separate_jsons(message)

            for m in mes_separated:
                deserialized = json.loads(m)
                deserialized = dict_to_object(deserialized)
                self.server.receive_message(deserialized, self.ID)
