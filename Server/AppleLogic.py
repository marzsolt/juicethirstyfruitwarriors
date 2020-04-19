import PlayerLogic
import client_message_constants as climess
import math
import Vector2D


class AppleLogic(PlayerLogic.PlayerLogic):
    def __init__(self, player_id, terrain):
        super(AppleLogic, self).__init__(player_id, terrain)

    def _process_requests(self, network_messages):
        super()._process_requests(network_messages)
        for mess in network_messages:
            if mess.type == climess.MessageType.APPLE_ATTACK:

                if mess.y > self._pos.y:
                    dist = math.sqrt((mess.x - self._pos.x) ** 2 + (mess.y - self._pos.y) ** 2)
                    strength = 10

                    x = (strength/dist)*(mess.x-self._pos.x)
                    y = (strength/dist)*(mess.y-self._pos.y)

                    force_of_jump = Vector2D.Vector2D(x, y)
                    self._attack(force_of_jump)

    def _attack(self, force):
        if not self._is_flying:
            self._add_force(force)
            self._impact()
            return True
        return False

    def _impact(self):
        print("bumm apple bumm")


