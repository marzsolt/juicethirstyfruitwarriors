import threading
import json
import socket

from src.utils.domi_utils import dict_to_object, separate_jsons


class ServerCommunicator(threading.Thread):
    def __init__(self, _server, _client, ID):
        threading.Thread.__init__(self)
        self.server = _server
        self.socket = _client
        self.ID = ID

    def send_message(self, message):
        serialized = json.dumps(message, default=lambda o: getattr(o, '__dict__', str(o)))  # recursive
        serialized = str.encode(serialized)

        try:
            self.socket.send(serialized)
        except OSError:  # if the socket was closed interrupting this
            pass

    def close(self):
        """" Responsible for closing down communicator with client on request. """
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print("ID: ", self.ID, " Player socket closed.")

    def run(self):
        while True:
            try:
                message = self.socket.recv(1024)
            except OSError:  # if the socket was closed interrupting this
                break

            message = message.decode()

            mes_separated = separate_jsons(message)

            for m in mes_separated:
                deserialized = json.loads(m)
                deserialized = dict_to_object(deserialized)
                self.server.receive_message(deserialized, self.ID)