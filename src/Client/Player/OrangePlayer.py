import pygame as pg

from src.Client.Network_communication.Client import Client
from src.Client.Player.Player import Player
from src.Client.Player.Player import PicFile
import src.Client.Network_communication.client_message_constants as climess

import src.Server.Network_communication.server_message_constants as sermess

from src.utils.BaseMessage import BaseMessage


class OrangePlayer(Player):
    """ Client side specialized Player (orange) """
    def __init__(self, player_id, name):
        super(OrangePlayer, self).__init__(player_id, name, PicFile.ORANGE)

        self.surf_angle = 0  # current angle in degrees of the player's surface, standard is 0
        self.surf_base = None  # standard surface (at angle 0) so that rotation caused deviations can be corrected
        self.rotation_angle = 30  # it must be a divisor of 360 degrees for correct functioning!
        self.rotation_dir = None  # direction of rotation = direction of player when attacked

    def update(self, pressed_keys, events):
        """ The update method of orange - looks for special (orange related) key presses """
        super().update(pressed_keys, events)

        # Orange special attack if 'a' is pressed (and a rolling caused by an earlier attack isn't in place).
        if pressed_keys and pressed_keys[pg.K_a] and self.surf_angle == 0:
            mes = BaseMessage(climess.MessageType.ORANGE_ATTACK, climess.Target.PLAYER_LOGIC + str(self.id))
            Client.get_instance().send_important_message(mes)

        # update the rolling of attack
        self.orange_rolling()

    def orange_rolling(self):
        """ Handle orange's rolling animation. """
        messages = Client.get_instance().get_targets_messages(sermess.Target.ORANGE_PLAYER + str(self.id))
        for mes in messages:
            if mes.type == sermess.MessageType.ORANGE_ROLL and self.surf_angle == 0:
                self.surf_angle += self.rotation_angle  # this triggers the animation, see if clause below
                self.surf_base = self.surf  # saves the standard surface
                self.rotation_dir = self.dir  # and gets rotation direction as current direction (on attack start)

        # perform rotation animation if one was triggered i.e. angle is NOT 0
        if self.surf_angle != 0:
            self.surf = self.surf_base
            self.surf = pg.transform.rotate(self.surf, self.rotation_dir * self.surf_angle)
            self.surf_angle += self.rotation_angle
            if self.surf_angle == 360 + self.rotation_angle:  # if done with 360 degrees stop
                self.surf_angle = 0
                self.surf = self.surf_base  # restore original surface
