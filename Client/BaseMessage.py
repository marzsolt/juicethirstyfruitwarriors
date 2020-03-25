class BaseMessage(object):
    def __init__(self, mess_type, target):
        self.type = mess_type
        self.target = target
