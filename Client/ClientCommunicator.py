import socket
import threading
import json
from utils.domi_utils import dict_to_object


class ClientCommunicator(threading.Thread):
    def __init__(self, _client, host, port):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = _client
        self.client_socket.connect((host, port))

    def send_message(self, message):
        serialized = json.dumps(message.__dict__)
        serialized = str.encode(serialized)
        self.client_socket.send(serialized)

    def run(self):
        while True:
            message = self.client_socket.recv(1024)
            message = message.decode()
            deserialized = json.loads(message)
            deserialized = dict_to_object(deserialized)
            self.client.receive_message(deserialized)
