import Player
import pygame as pg
from BaseMessage import BaseMessage
from Client import Client
import client_message_constants as climess


class OrangePlayer(Player.Player):
    def __init__(self, player_id):
        super(OrangePlayer, self).__init__(player_id, Player.PicFile.ORANGE)

        self.surf_angle = 0
        self.surf_base = None
        self.rotation_angle = 20  # it must be a divisor of 360 degrees for correct functioning!
        self.rotation_dir = None

    def update(self, pressed_keys, events):
        super().update(pressed_keys, events)

        if pressed_keys and pressed_keys[pg.K_a] and self.surf_angle == 0:
            mes = BaseMessage(climess.MessageType.ORANGE_ATTACK, climess.Target.PLAYER_LOGIC + str(self._id))
            Client.get_instance().send_message(mes)

            self.surf_angle += self.rotation_angle
            self.surf_base = self.surf
            self.rotation_dir = self.dir
            print(self.dir)

        if self.surf_angle != 0:
            self.surf = self.surf_base
            self.surf = pg.transform.rotate(self.surf, self.rotation_dir * self.surf_angle)
            self.surf_angle += self.rotation_angle
            if self.surf_angle == 360 + self.rotation_angle:
                self.surf_angle = 0
                self.surf = self.surf_base
