import threading
from _thread import*


class ClientReceiver(threading.Thread):
    def __init__(self, _server):
        #threading.Thread.__init__(self)
        self.server = _server

    def run_clientreceiver(self):
        while True:
            new_client, addr = self.server.serverSocket.accept()
            print("got connection")
            self.server.new_client(new_client)
