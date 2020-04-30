import socket
import threading
import json
import logging

from src.utils.domi_utils import dict_to_object, separate_jsons


class ClientCommunicator(threading.Thread):
    def __init__(self, _client, _host, _port):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = _client
        self.host = _host
        self.port = _port
        self.logger = logging.getLogger('Domi.ClientCommunicator')

    def send_message(self, message):
        serialized = json.dumps(message, default=lambda o: getattr(o, '__dict__', str(o)))  # recursive
        serialized = str.encode(serialized)
        self.client_socket.send(serialized)

    def close(self):
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()
        print("Client socket closed.")

    def run(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except socket.error:
            self.logger.exception("Error during connecting, returning from run!")
            self.client.connection_alive = False
            return
        else:
            self.client.connection_alive = True
            self.logger.info("Successful connection!")

        while True:
            try:
                message = self.client_socket.recv(1024)
            except OSError:  # if socket was shut down by interrupting recv()
                break

            message = message.decode()
            mes_separated = separate_jsons(message)

            for m in mes_separated:
                deserialized = json.loads(m)
                deserialized = dict_to_object(deserialized)
                self.client.receive_message(deserialized)
