import pygame as pg

from juicethirstyfruitwarriors.Client.Client import Client
from juicethirstyfruitwarriors.Client.Player import Player
from juicethirstyfruitwarriors.Client.Player import PicFile
import juicethirstyfruitwarriors.Client.client_message_constants as climess

from juicethirstyfruitwarriors.BaseMessage import BaseMessage




class ApplePlayer(Player):
    def __init__(self, player_id):
        super(ApplePlayer, self).__init__(player_id, PicFile.APPLE)

    def update(self, pressed_keys, events):
        super().update(pressed_keys, events)
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                x, y = pg.mouse.get_pos()
                
                mes = BaseMessage(climess.MessageType.APPLE_ATTACK, climess.Target.PLAYER_LOGIC + str(self._id))
                mes.x = x
                mes.y = self.SCREEN_HEIGHT - y
                Client.get_instance().send_message(mes)



