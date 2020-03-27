import socket
import threading
import json
import sys
from utils.domi_utils import dict_to_object


class ClientCommunicator(threading.Thread):
    def __init__(self, _client, _host, _port, _bucket):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = _client
        self.host = _host
        self.port = _port
        self.bucket = _bucket

    def send_message(self, message):
        serialized = json.dumps(message.__dict__)
        serialized = str.encode(serialized)
        self.client_socket.send(serialized)

    def run(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except socket.error:
            print("ClientCommunicator Thread: Error connecting, returning from run()!")
            self.bucket.put(sys.exc_info())
            return

        while True:
            message = self.client_socket.recv(1024)
            message = message.decode()
            deserialized = json.loads(message)
            deserialized = dict_to_object(deserialized)
            self.client.receive_message(deserialized)
