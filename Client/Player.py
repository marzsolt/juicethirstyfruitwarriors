import pygame as pg
import PlayerLogic
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

    def update(self, events):  #pressed_keys
        network_messages = []
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    print("LEFT PRESSED")
                    network_messages.append("LEFT")
                if event.key == pg.K_RIGHT:
                    print("RIGHT PRESSED")
                    network_messages.append("RIGHT")
#        if pressed_keys[pg.K_LEFT]:
#            network_messages.append("LEFT")
#        if pressed_keys[pg.K_RIGHT]:
#            network_messages.append("RIGHT")
        mes = BaseMessage(climess.MessageType.PLAYER_POS, climess.Target.PLAYER_LOGIC)
        mes.list = network_messages
        mes.player_id = self._id
        Client.get_instance().send_message(mes)

        self.pos_update()

    def pos_update(self):
        # TODO shall be (called from)/in update, messages loaded from networking by id
        messages = Client.get_instance().get_targets_messages(sermess.Target.PLAYER)
        for mess in messages:
            if mess.player_id == self._id:
                if mess.type == sermess.MessageType.PLAYER_POS:
                    self.rect.center = (mess.x, mess.y)  # setting Sprite's center
