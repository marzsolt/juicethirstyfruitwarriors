import pygame as pg
from Player import Player
from PlayerAI import PlayerAI

# FOR TESTING...
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((800, 600))
p = Player(0)
p2 = Player(1)
p3 = PlayerAI(2)
players = [p, p2, p3]
while True:
    pressed_keys = pg.key.get_pressed()
    events = pg.event.get()
    for p in players:
        p.update(pressed_keys, events)

    # Clear screen
    screen.fill((0, 0, 0))
    # Draw player
    for p in players:
        screen.blit(p.surf, p.rect)
    # Update screen
    pg.display.flip()
    clock.tick(30)  # Ensure program maintains a rate of 30 frames per second
