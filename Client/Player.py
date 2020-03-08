import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pg.image.load("img/apple_test_image.png").convert()
        self.surf.set_colorkey((255, 253, 201), pg.RLEACCEL)
        self.rect = self.surf.get_rect()

        screen.blit(self.surf, self.rect)

    def update(self, pressed_keys, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    print("WHUISKDJNKF")
        if pressed_keys[pg.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pg.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pg.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pg.K_RIGHT]:
            self.rect.move_ip(5, 0)
            print(pressed_keys)


pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((800, 600))
p = Player()
while True:
    p.update(pg.key.get_pressed(), pg.event.get())

    screen.fill((0, 0, 0))
    screen.blit(p.surf, p.rect)
    pg.display.flip()

    clock.tick(300)  # Ensure program maintains a rate of 30 frames per second
