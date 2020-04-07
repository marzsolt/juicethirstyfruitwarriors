import pygame as pg
from BaseMessage import BaseMessage
from Client import Client
import server_message_constants as sermess
import client_message_constants as climess


class Player(pg.sprite.Sprite):
    def __init__(self, player_id):
        super(Player, self).__init__()
        self.surf = pg.image.load("img/apple_test_image.png").convert()  # may have to change the path
        self.surf.set_colorkey((255, 253, 201), pg.RLEACCEL)  # background color of the picture -> that color not shown
        self.rect = self.surf.get_rect()
        self._id = player_id

    def update(self, pressed_keys):
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

        self.pos_update()

    def pos_update(self):
        messages = Client.get_instance().get_targets_messages(sermess.Target.PLAYER+str(self._id))
        for mess in messages:
            if mess.type == sermess.MessageType.PLAYER_POSITION:
                self.rect.center = (mess.x, 600 - mess.y)  # setting Sprite's center TODO 600...
