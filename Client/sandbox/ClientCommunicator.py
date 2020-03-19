import socket
import threading


class ClientCommunicator(threading.Thread):
    def __init__(self, _client, host, port):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = _client
        self.client_socket.connect((host, port))

    def send_message(self, message):
        message = str.encode(message)
        self.client_socket.send(message)

    def run(self):
        while True:
            message = self.client_socket.recv(1024)
            message = message.decode()
            self.client.receive_message(message)
