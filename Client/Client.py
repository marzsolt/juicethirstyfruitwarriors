import socket
import ClientCommunicator


class Client:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Client.__instance is None:
            Client.__instance = Client()
        return Client.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Client.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            host = socket.gethostname()  # or 'IP address'
            port = 12145  # Random port number
            self.__communicator = ClientCommunicator.ClientCommunicator(self, host, port)

            self.__communicator.start()

    def receive_message(self, message):
        print("Server sent: ", message)
        message_split = message.split(";")
        if message_split[0] == "kakao":
            print("I sent: csoki")
            self.send_message("csoki")

    def send_message(self, message):
        self.__communicator.send_message(message)




client = Client()
