import pygame as pg

from src.Client.Network_communication.Client import Client
from src.Client.Player.Player import Player
from src.Client.Player.Player import PicFile
import src.Client.Network_communication.client_message_constants as climess

import src.Server.Network_communication.server_message_constants as sermess

from src.utils.BaseMessage import BaseMessage


class OrangePlayer(Player):
    def __init__(self, player_id):
        super(OrangePlayer, self).__init__(player_id, PicFile.ORANGE)

        self.surf_angle = 0
        self.surf_base = None
        self.rotation_angle = 30  # it must be a divisor of 360 degrees for correct functioning!
        self.rotation_dir = None

    def update(self, pressed_keys, events):
        super().update(pressed_keys, events)

        if pressed_keys and pressed_keys[pg.K_a] and self.surf_angle == 0:
            mes = BaseMessage(climess.MessageType.ORANGE_ATTACK, climess.Target.PLAYER_LOGIC + str(self._id))
            Client.get_instance().send_message(mes)

        self.orange_rolling()

    def orange_rolling(self):
        messages = Client.get_instance().get_targets_messages(sermess.Target.ORANGE_PLAYER + str(self._id))
        for mes in messages:
            if mes.type == sermess.MessageType.ORANGE_ROLL and self.surf_angle == 0:
                self.surf_angle += self.rotation_angle
                self.surf_base = self.surf
                self.rotation_dir = self.dir

        if self.surf_angle != 0:
            self.surf = self.surf_base
            self.surf = pg.transform.rotate(self.surf, self.rotation_dir * self.surf_angle)
            self.surf_angle += self.rotation_angle
            if self.surf_angle == 360 + self.rotation_angle:
                self.surf_angle = 0
                self.surf = self.surf_base
