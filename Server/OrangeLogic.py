from juicethirstyfruitwarriors.Server.Server import Server
from juicethirstyfruitwarriors.Server.PlayerLogic import PlayerLogic
from juicethirstyfruitwarriors.Server.Vector2D import Vector2D
import juicethirstyfruitwarriors.Server.server_message_constants as sermess

import juicethirstyfruitwarriors.Client.client_message_constants as climess

from juicethirstyfruitwarriors.BaseMessage import BaseMessage



class OrangeLogic(PlayerLogic):
    def __init__(self, player_id, terrain):
        super(OrangeLogic, self).__init__(player_id, terrain)

        self._is_attacking = False
        self._attack_strength = 5


    def _process_requests(self, network_messages):
        super()._process_requests(network_messages)
        for mess in network_messages:
            if mess.type == climess.MessageType.ORANGE_ATTACK:
                if self._vel != Vector2D.zero():
                    self._attack()

                    #  ACK valid attack -> actually for rolling purposes
                    mes = BaseMessage(sermess.MessageType.ORANGE_ROLL, sermess.Target.ORANGE_PLAYER + str(self._id))
                    Server.get_instance().send_all(mes)

    def _attack(self):
        if super()._attack() and not self._is_flying:
            self._is_attacking = True
            self._add_ground_directed_force(self._attack_strength, self.my_dir())
            self._impact()
            return True
        return False

    def _impact(self):
        if self._is_attacking:
            print("roll orange roll")
            self._is_attacking = False
