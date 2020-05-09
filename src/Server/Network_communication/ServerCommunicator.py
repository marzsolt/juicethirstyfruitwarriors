import threading
import json
import socket
import logging

from src.utils.domi_utils import dict_to_object, separate_jsons, id_generator
from src.utils.Timer import Timer
import src.Server.Network_communication.server_message_constants as sermess
import src.Client.Network_communication.client_message_constants as climess

# This class is responsible for the communication on the server side.
# It receives and sends messages from/to the client.


class ServerCommunicator(threading.Thread):
    def __init__(self, _server, _client, ID):
        threading.Thread.__init__(self)
        self.server = _server
        self.socket = _client
        self.ID = ID
        self.logger = logging.getLogger('Domi.ServerCommunicator')
        self._important_message_id = 0
        self._acknowledged_important = {}
        self.mes_id = id_generator()

    def send_message(self, message):
        if message.type == sermess.MessageType.DIED:
            self.logger.debug(f"Player {message.player_id} died message sent to {self.ID} client.")
        serialized = json.dumps(message, default=lambda o: getattr(o, '__dict__', str(o)))  # recursive
        serialized = str.encode(serialized)

        try:
            self.socket.send(serialized)
        except OSError:  # if the socket was closed interrupting this
            pass

    def send_important_message(self, message):
        message.mes_id = next(self.mes_id)
        self._acknowledged_important[message.mes_id] = False
        self.send_message(message)

        Timer.sch_fun(1, self.delayed_resend, (message,))

    def delayed_resend(self, message):
        if not self._acknowledged_important[message.mes_id]:
            self.send_message(message)
            Timer.sch_fun(1, self.delayed_resend, (message,))
        else:
            del self._acknowledged_important[message.mes_id]

    def close(self):
        """" Responsible for closing down communicator with client on request. """
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.logger.info(f"ID: {self.ID} Player socket closed.")

    def run(self):
        while True:
            try:
                message = self.socket.recv(1024)
            except OSError:  # if the socket was closed interrupting this
                break

            message = message.decode()

            mes_separated = separate_jsons(message)  # prevents extra data errors from multiple jsons

            for m in mes_separated:
                deserialized = json.loads(m)
                deserialized = dict_to_object(deserialized)

                if deserialized.type == climess.MessageType.ACK:
                    self._acknowledged_important[deserialized.mes_id] = True
                else:
                    self.server.receive_message(deserialized, self.ID)
