from _thread import *
import threading


class ClientReceiver(threading.Thread):
    def __init__(self, _server):
        threading.Thread.__init__(self)
        self.server = _server

        #start_new_thread(self.run())

    def run(self):
        while (True):
            newClient, addr = self.server.serverSocket.accept()
            print("got connection")
            self.server.newClient(newClient)
