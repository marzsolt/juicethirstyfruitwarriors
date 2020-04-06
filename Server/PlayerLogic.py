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
        self._speed = 2
        self._x = 100+player_id*100  # for testing
        self._y = 100+player_id*100

        self.initial_pos_sending = True

    def _process_requests(self, network_messages):
        for m in network_messages:
            for mess in m.movement_list:
                if mess == climess.ActionRequest.MOVE_LEFT:
                    self._move_left()
                elif mess == climess.ActionRequest.MOVE_RIGHT:
                    self._move_right()

    def _move_left(self):
        self._x = self._x - self._speed

        self._x = min(max(self._x, self.X_MIN), self.X_MAX)
        self._y = min(max(self._y, self.Y_MIN), self.Y_MAX)

    def _move_right(self):
        self._x = self._x + self._speed

        self._x = min(max(self._x, self.X_MIN), self.X_MAX)
        self._y = min(max(self._y, self.Y_MIN), self.Y_MAX)

    def _send_updated_pos(self):
        msg = BaseMessage(mess_type=sermess.MessageType.PLAYER_POSITION, target=sermess.Target.PLAYER + str(self._id))
        msg.player_id = self._id
        msg.x = self._x
        msg.y = self._y
        Server.get_instance().send_all(msg)

    def update(self):
        messages = Server.get_instance().get_targets_messages(climess.Target.PLAYER_LOGIC+str(self._id))
        position_messages = list(filter(lambda x: x.type == climess.MessageType.PLAYER_MOVEMENT, messages))
        if position_messages:
            self._process_requests(position_messages)
            self._send_updated_pos()
        if self.initial_pos_sending:
            self._send_updated_pos()
            self.initial_pos_sending = False

    def get_id(self):
        return self._id
