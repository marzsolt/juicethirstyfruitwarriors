from Server import Server
import server_message_constants as sermess
import client_message_constants as climess
from BaseMessage import BaseMessage


class PlayerLogic:
    X_MIN = 0
    X_MAX = 800  # TODO use screen sizes
    Y_MIN = 0
    Y_MAX = 600

    def __init__(self, player_id):
        self._id = player_id
        self._speed = 5
        self._x = 100+player_id*100  # for testing
        self._y = 100+player_id*100

    def process_requests(self, network_messages):
        for m in network_messages:
            for mess in m.list:
                if mess == "LEFT":
                    self._x = self._x - self._speed
                elif mess == "RIGHT":
                    self._x = self._x + self._speed

            # keep the player in screen
            self._x = min(max(self._x, self.X_MIN), self.X_MAX)
            self._y = min(max(self._y, self.Y_MIN), self.Y_MAX)

        msg = BaseMessage(mess_type=sermess.MessageType.PLAYER_POS, target=sermess.Target.PLAYER)
        msg.player_id = self._id
        msg.x = self._x
        msg.y = self._y
        Server.get_instance().send_all(msg)

    def update(self):  # pressed_keys, events?
        messages = Server.get_instance().get_targets_messages(climess.Target.PLAYER_LOGIC+str(self._id))
        position_messages = []
        for message in messages:
            if message.type == climess.MessageType.PLAYER_POS:
                position_messages.append(message)

        self.process_requests(position_messages)
