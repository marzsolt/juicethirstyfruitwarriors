import pygame as pg
import PlayerLogic


class Player(pg.sprite.Sprite):
    def __init__(self, player_id):
        super(Player, self).__init__()
        self.surf = pg.image.load("../img/apple_test_image.png").convert()  # may have to change the path
        self.surf.set_colorkey((255, 253, 201), pg.RLEACCEL)  # background color of the picture -> that color not shown
        self.rect = self.surf.get_rect()
        self._id = player_id

    def update(self, pressed_keys, events):
        network_messages = []
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    print("A PRESSED")
        if pressed_keys[pg.K_LEFT]:
            network_messages.append("LEFT")
        if pressed_keys[pg.K_RIGHT]:
            network_messages.append("RIGHT")
        PlayerLogic.players[self._id].process_requests(network_messages, self)  # TODO use normal networking

    def pos_update(self, x, y):
        # TODO shall be (called from)/in update, messages loaded from networking by id
        self.rect.center = (x, y)  # setting Sprite's center
