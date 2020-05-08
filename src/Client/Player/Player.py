import pygame as pg
from enum import Enum
import logging

from src.Client.Network_communication.Client import Client
import src.Client.Network_communication.client_message_constants as climess

import src.Server.Network_communication.server_message_constants as sermess

from src.utils.BaseMessage import BaseMessage

from src.utils.general_constants import SCREEN_HEIGHT, GREEN, WHITE, RED


class PicFile(Enum):
    ORANGE = "img/orange_test_image.png"
    APPLE = "img/apple_test_image.png"


class Player(pg.sprite.Sprite):

    def __init__(self, player_id, name, pic_file):
        super(Player, self).__init__()
        self.logger = logging.getLogger('Domi.Player')
        try:
            img_surf = pg.image.load(pic_file.value).convert()  # may have to change the path
            self.surf = pg.Surface((60, 60))
            self.surf.fill((255, 253, 201))
            self.surf.blit(img_surf, (0, 10))
            self.surf.set_colorkey((255, 253, 201),
                pg.RLEACCEL)  # background color of the picture -> that color not shown

            # showing player name
            font = pg.font.SysFont('freesansbold', 17)
            name_surf = font.render(name, False, WHITE)
            name_surf_rect = name_surf.get_rect()
            name_surf_rect.center = (self.surf.get_width() // 2, name_surf_rect.centery)
            self.surf.blit(name_surf, name_surf_rect)
        except pg.error:  # PyCharm you are a liar, it's perfectly OK
            self.logger.exception("Cannot load image!")
            self.logger.critical("Atya ég!")
        self.rect = self.surf.get_rect()
        self._id = player_id
        self.hp = None
        self.dir = 1

    def update(self, pressed_keys, events):
        network_messages = []

        # Collect basic movement requests (go left/right) and send them to server.
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
                self.rect.center = (mess.x, SCREEN_HEIGHT - mess.y)  # graphical y axis is weird
                self.dir = mess.dir

                if self.hp != mess.hp:  # update HP if it's changed
                    self.hp = mess.hp

                    # Show HP bar:
                    # draw a white rect which is 1-1 pixel thicker in every direction to form border
                    pg.draw.rect(self.surf, WHITE, (14, 10, 32, 7))
                    # draw green/red health bar for own/enemy player respectively
                    pg.draw.rect(
                        self.surf,
                        GREEN if Client.get_instance().id == self._id else RED,
                        (15, 11, 30 * mess.hp / 100, 5)
                    )
