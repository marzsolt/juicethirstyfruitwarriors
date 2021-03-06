import socket
import threading
import json
import logging

from src.utils.domi_utils import dict_to_object, separate_jsons, id_generator
from src.utils.Timer import Timer
import src.Server.Network_communication.server_message_constants as sermess


# This class is responsible for the  communication of the client as it sends and receives message through sockets.


class ClientCommunicator(threading.Thread):
    def __init__(self, _client, _host, _port):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = _client
        self.host = _host
        self.port = _port
        self.logger = logging.getLogger('Domi.ClientCommunicator')
        self.fidg = id_generator()
        self._acknowledged_important = {}
        self.mes_id = id_generator()

    def log_mess_to_file(self, mess):
        """
        :param mess: the message to be logged
        :return: nothing
        Logs every message into a new (binary) file. """
        def new_file_name():
            fid = next(self.fidg)
            return dir_name + file_name_base + str(fid) + ext

        dir_name = "network_messages/"
        file_name_base = "mess"
        ext = ".bin"

        f = open(new_file_name(), "wb")
        f.write(str.encode(mess))
        f.close()

    def send_message(self, message):
        serialized = json.dumps(message, default=lambda o: getattr(o, '__dict__', str(o)))  # recursive
        serialized = str.encode(serialized)
        self.client_socket.send(serialized)

    def send_important_message(self, message):
        """Sends the message and calls a delayed function to check acknowledgement"""
        message.mes_id = next(self.mes_id)
        # the dict contains the message ids and whether they get acknowledged
        self._acknowledged_important[message.mes_id] = False
        self.send_message(message)

        Timer.sch_fun(1, self.delayed_resend, (message,))

    def delayed_resend(self, message):
        # if the acknowledgement did not arrive from the server in a tick, the message is resent
        if not self._acknowledged_important[message.mes_id]:
            self.send_message(message)
            Timer.sch_fun(1, self.delayed_resend, (message,))
        # if the acknowledgement arrived there is no need to store this message id
        else:
            del self._acknowledged_important[message.mes_id]

    def close(self):
        """ Closing down client socket. """
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()
        self.logger.info("Client socket closed.")

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
            mes_separated = separate_jsons(message)  # it prevents extra data error at loading jsons

            for m in mes_separated:
                deserialized = json.loads(m)
                deserialized = dict_to_object(deserialized)
                # if a message is for acknowledgement purposes it does not need to be received by the client
                if deserialized.type == sermess.MessageType.ACK:
                    self._acknowledged_important[deserialized.mes_id] = True
                else:
                    self.client.receive_message(deserialized)
