import pygame as pg

from src.Client.Screen.Screen import Screen
from src.utils.awesome_logging import setup_logger
from src.utils.general_constants import FPS
from src.utils.Timer import Timer


def main():
    """" The main function of the game. """
    pg.init()  # initializes pyGame

    # Logging
    setup_logger()  # initializes the logger

    screen = Screen()  # set up the screen

    # Setup the clock for a decent frame rate
    clock = pg.time.Clock()

    running = True  # variable to keep the main loop running

    while running:  # main loop
        # update screen & pass all the events in the queue for handling
        running = screen.update(pg.event.get(), pg.key.get_pressed())  
        clock.tick(FPS)  # Ensure program maintains a rate of 40 frames per second
        Timer.update()

    pg.quit()  # all done


if __name__ == "__main__":
    main()
