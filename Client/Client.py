import ClientCommunicator


class Client:
    __instance = None

    @staticmethod
    def get_instance(ip):
        """ Static access method. """
        if Client.__instance is None:
            Client.__instance = Client(ip)
        return Client.__instance

    def __init__(self, ip):
        """ Virtually private constructor. """
        if Client.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            host = ip
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
