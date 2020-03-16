import pygame as pg
import PlayerLogic
from enum import Enum
import random


class Movement(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    IDLE = "IDLE"


class PlayerAI(pg.sprite.Sprite):
    def __init__(self, player_id):
        super(PlayerAI, self).__init__()
        self.surf = pg.image.load("../img/apple_test_image.png").convert()
        self.surf.set_colorkey((255, 253, 201), pg.RLEACCEL)
        self.rect = self.surf.get_rect()
        self._id = player_id
        self._dir = Movement.IDLE

    def update(self, pressed_keys, events):
        if random.random() < 0.1:
            self._dir = random.choice([m.value for m in Movement])
        network_messages = [self._dir]
        PlayerLogic.players[self._id].process_requests(network_messages, self)

    def pos_update(self, x, y):
        # TODO shall be called from update, messages loaded from networking by id
        self.rect.center = (x, y)
