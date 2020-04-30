import threading
import json

from src.utils.domi_utils import dict_to_object, separate_jsons


class ServerCommunicator(threading.Thread):
    def __init__(self, _server, _client, ID):
        threading.Thread.__init__(self)
        self.server = _server
        self.socket = _client
        self.ID = ID
        self.communicator_alive = True

    def send_message(self, message):
        serialized = json.dumps(message, default=lambda o: getattr(o, '__dict__', str(o)))  # recursive
        serialized = str.encode(serialized)
        self.socket.send(serialized)

    def close(self):
        self.socket.close()
        print("Socket for player connection closed.")

    def run(self):
        while self.communicator_alive:
            message = self.socket.recv(1024)
            message = message.decode()

            mes_separated = separate_jsons(message)

            for m in mes_separated:
                deserialized = json.loads(m)
                deserialized = dict_to_object(deserialized)
                self.server.receive_message(deserialized, self.ID)
