import pygame as pg
from enum import Enum

from src.Client.Network_communication.Client import Client
import src.Client.Network_communication.client_message_constants as climess

import src.Server.Network_communication.server_message_constants as sermess

from src.utils.BaseMessage import BaseMessage


class PicFile(Enum):
    ORANGE = "img/orange_test_image.png"
    APPLE = "img/apple_test_image.png"


class Player(pg.sprite.Sprite):
    SCREEN_HEIGHT = 600  # TODO use general constant
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, player_id, pic_file):
        super(Player, self).__init__()
        self.surf = pg.image.load(pic_file.value).convert()  # may have to change the path
        self.surf.set_colorkey((255, 253, 201), pg.RLEACCEL)  # background color of the picture -> that color not shown
        self.rect = self.surf.get_rect()
        # TODO: replace this current player funcionality by showing it's health in green instead of re
        # if Client.get_instance().id == player_id:  # Show that it's the client's own player
        #    pg.draw.line(self.surf, (0, 255, 0), (15, 0), (45, 0))
        self._id = player_id
        self.hp = None

    def update(self, pressed_keys, events):
        network_messages = []

        if pressed_keys:
            if pressed_keys[pg.K_LEFT]:
                network_messages.append(climess.ActionRequest.MOVE_LEFT)
            if pressed_keys[pg.K_RIGHT]:
                network_messages.append(climess.ActionRequest.MOVE_RIGHT)
        if network_messages:
            mes = BaseMessage(climess.MessageType.PLAYER_MOVEMENT, climess.Target.PLAYER_LOGIC + str(self._id))
            mes.movement_list = network_messages
            Client.get_instance().send_message(mes)

        self.pos_hp_update()

    def pos_hp_update(self):
        messages = Client.get_instance().get_targets_messages(sermess.Target.PLAYER+str(self._id))
        for mess in messages:
            if mess.type == sermess.MessageType.PLAYER_POS_HP:
                self.rect.center = (mess.x, self.SCREEN_HEIGHT - mess.y)  # graphical y axis is weird
                self.dir = mess.dir

                if self.hp != mess.hp:
                    self.hp = mess.hp
                    pg.draw.rect(self.surf, self.WHITE, (14, 0, 32, 7))  # 1-1 pixel thicker in every dir. to form border
                    pg.draw.rect(
                        self.surf,
                        self.GREEN if Client.get_instance().id == self._id else self.RED,
                        (15, 1, 30 * mess.hp / 100, 5)
                    )
