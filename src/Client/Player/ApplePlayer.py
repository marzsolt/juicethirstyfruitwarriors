import pygame as pg

from src.Client.Network_communication.Client import Client
from src.Client.Player.Player import Player
from src.Client.Player.Player import PicFile
import src.Client.Network_communication.client_message_constants as climess

from src.utils.BaseMessage import BaseMessage
from src.utils.general_constants import SCREEN_HEIGHT


class ApplePlayer(Player):
    def __init__(self, player_id, name):
        super(ApplePlayer, self).__init__(player_id, name, PicFile.APPLE)

    def update(self, pressed_keys, events):
        super().update(pressed_keys, events)
        for event in events:
            # Request attack if mouse clicked.
            if event.type == pg.MOUSEBUTTONUP:
                x, y = pg.mouse.get_pos()
                
                mes = BaseMessage(climess.MessageType.APPLE_ATTACK, climess.Target.PLAYER_LOGIC + str(self.id))
                mes.x = x
                mes.y = SCREEN_HEIGHT - y
                Client.get_instance().send_important_message(mes)
