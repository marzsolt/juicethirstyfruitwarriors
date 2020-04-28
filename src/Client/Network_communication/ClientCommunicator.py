import socket
import threading
import json

from src.utils.domi_utils import dict_to_object


class ClientCommunicator(threading.Thread):
    def __init__(self, _client, _host, _port):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = _client
        self.host = _host
        self.port = _port

    def send_message(self, message):
        serialized = json.dumps(message, default=lambda o: getattr(o, '__dict__', str(o)))  # recursive
        serialized = str.encode(serialized)
        self.client_socket.send(serialized)

    def run(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except socket.error:
            print("ClientCommunicator Thread: Error connecting, returning from run()!")
            self.client.connection_alive = False
            return
        else:
            self.client.connection_alive = True

        while True:
            message = self.client_socket.recv(1024)
            message = message.decode()
            deserialized = json.loads(message)
            deserialized = dict_to_object(deserialized)
            self.client.receive_message(deserialized)
