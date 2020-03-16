import pygame as pg
import PlayerLogic


class Player(pg.sprite.Sprite):
    def __init__(self, player_id):
        super(Player, self).__init__()
        self.surf = pg.image.load("../img/apple_test_image.png").convert()
        self.surf.set_colorkey((255, 253, 201), pg.RLEACCEL)
        self.rect = self.surf.get_rect()
        self._id = player_id

    def update(self, pressed_keys, events):
        network_messages = []
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    print("A PRESSED")
        # if pressed_keys[pg.K_UP]:
        #     self.rect.move_ip(0, -self._speed)
        # if pressed_keys[pg.K_DOWN]:
        #     self.rect.move_ip(0, self._speed)
        if pressed_keys[pg.K_LEFT]:
            network_messages.append("LEFT")
        if pressed_keys[pg.K_RIGHT]:
            network_messages.append("RIGHT")
        PlayerLogic.players[self._id].process_requests(network_messages, self)

    def pos_update(self, x, y):
        # TODO shall be called from update, messages loaded from networking by id
        self.rect.center = (x, y)
