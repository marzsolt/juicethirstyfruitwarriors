import socket
import ClientCommunicator


class Client:
    def __init__(self):
        host = socket.gethostname()  # or 'IP address'
        port = 12145  # Random port number
        self.communicator = ClientCommunicator.ClientCommunicator(self, host, port)

        self.communicator.start()

    def receive_message(self, message):
        print("Server sent: ", message)
        message_split = message.split(";")
        if message_split[0] == "kakao":
            print("I sent: csoki")
            self.communicator.send_message("csoki")

    def send_message(self, message):
        self.communicator.send_message(message)

    def run(self):
        while True:
            pass


client = Client()
