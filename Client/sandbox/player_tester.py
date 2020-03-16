import pygame as pg
from Player import Player

# FOR TESTING...
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((800, 600))
p = Player(0)
p2 = Player(1)
while True:
    pressed_keys = pg.key.get_pressed()
    events = pg.event.get()
    p.update(pressed_keys, events)
    p2.update(pressed_keys, events)

    # Clear screen
    screen.fill((0, 0, 0))
    # Draw player
    screen.blit(p.surf, p.rect)
    screen.blit(p2.surf, p2.rect)
    # Update screen
    pg.display.flip()
    clock.tick(30)  # Ensure program maintains a rate of 30 frames per second
