import math

import src.Client.Network_communication.client_message_constants as climess

from src.Server.Player.PlayerLogic import PlayerLogic
from src.utils.Vector2D import Vector2D
from src.utils.Timer import Timer


class AppleLogic(PlayerLogic):
    def __init__(self, player_id, terrain, game):
        super(AppleLogic, self).__init__(player_id, terrain, game)

        self._min_attack_angle = 0.55  # it is around 30 deg
        self._normal_attack_strength = 25
        self._attack_damage = 10

        self._min_attack_x, self._min_attack_y = self._attack_constants()

    def _process_requests(self, network_messages):
        super()._process_requests(network_messages)
        for mess in network_messages:
            if mess.type == climess.MessageType.APPLE_ATTACK:
                force_of_jump = self._calculate_attack_force(mess.x, mess.y)

                self._attack(force_of_jump)

    def _attack_constants(self):
        x = -1 * self._normal_attack_strength * math.cos(self._min_attack_angle)
        y = self._normal_attack_strength * math.sin(self._min_attack_angle)
        return x, y

    def _calculate_attack_force(self, x, y):
        dist = math.sqrt((x - self.pos.x) ** 2 + (y - self.pos.y) ** 2)
        angle = math.asin((y - self.pos.y) / dist)

        if angle > self._min_attack_angle:
            attack_x = (self._normal_attack_strength / dist) * (x - self.pos.x)
            attack_y = (self._normal_attack_strength / dist) * (y - self.pos.y)

        else:
            if x < self.pos.x:
                attack_x = self._min_attack_x
            else:
                attack_x = -1 * self._min_attack_x
            attack_y = self._min_attack_y

        return Vector2D(attack_x, attack_y)

    def _attack(self, force):
        if self._can_attack and not self._is_flying:
            super()._attack()
            self._add_force(force)

    def _finish_attack(self):
        super()._finish_attack()
        self._game.player_damage(self, self._attack_damage, 2*PlayerLogic.RADIUS)

    def _impact(self):
        if self._is_attacking:
            self._finish_attack()
