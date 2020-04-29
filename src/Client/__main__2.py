import pygame as pg

from src.Client.Screen.Screen import Screen
from src.utils.awesome_logging import setup_logger


def main():
    pg.init()

    # Logging
    setup_logger()

    screen = Screen()  # set up the screen

    # Setup the clock for a decent framerate
    clock = pg.time.Clock()

    running = True  # variable to keep the main loop running

    while running:  # main loop
        # update screen & pass all the events in the queue for handling
        running = screen.update(pg.event.get(), pg.key.get_pressed())  
        clock.tick(40)  # Ensure program maintains a rate of 40 frames per second

    pg.quit()  # all done


if __name__ == "__main__":
    main()
