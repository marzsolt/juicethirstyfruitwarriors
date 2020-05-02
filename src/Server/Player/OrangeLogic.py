from src.Server.Network_communication.Server import Server
from src.Server.Player.PlayerLogic import PlayerLogic
from src.utils.Vector2D import Vector2D
import src.Server.Network_communication.server_message_constants as sermess

import src.Client.Network_communication.client_message_constants as climess

from src.utils.BaseMessage import BaseMessage
from src.utils.Timer import Timer


class OrangeLogic(PlayerLogic):
    def __init__(self, player_id, terrain, game):
        super(OrangeLogic, self).__init__(player_id, terrain, game)

        self._attack_strength = 10
        self._attack_damage = 3

    def update(self):
        super().update()
        if self._is_attacking:
            self._game.player_damage(self, self._attack_damage)

    def _process_requests(self, network_messages):
        super()._process_requests(network_messages)
        for mess in network_messages:
            if mess.type == climess.MessageType.ORANGE_ATTACK and self._can_attack and self.is_moving():
                self._attack()
                # self.logger.debug(f"velocity: {self._vel} ")

    def _finish_attack(self):
        super()._finish_attack()
        self._is_attacking = False

    def _attack(self):
        if self._can_attack and not self._is_flying:
            super()._attack()
            self._add_ground_directed_force(self._attack_strength, self.my_dir())
            mes = BaseMessage(sermess.MessageType.ORANGE_ROLL, sermess.Target.ORANGE_PLAYER + str(self._id))
            Server.get_instance().send_all(mes)
            Timer.sch_fun(12, self._finish_attack, ())  #disgusting, I know,






    def _impact(self):
        if self._is_attacking:
            print("roll orange roll")
            self._is_attacking = False
