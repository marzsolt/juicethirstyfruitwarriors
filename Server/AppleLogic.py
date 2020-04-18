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
                # mouse_pos = mess.mouse_pos
                dist = math.sqrt((mess.x - self._pos.x) ** 2 + (mess.y - self._pos.y) ** 2)
                #side = abs(mess.y - self._pos.y)
                #angle = math. asin(side/dist)
                x = (10/dist)*(mess.x-self._pos.x)
                y =  (10 / dist) *(mess.y-self._pos.y)

                print(x,y)
                angle = Vector2D.Vector2D(x, y)
                self._attack(angle)

    def _attack(self, angle):
        if super()._attack():
            self._add_force(angle)
            self._impact()
            return True
        return False

    def _impact(self):
        print("bumm bumm nyaff")


