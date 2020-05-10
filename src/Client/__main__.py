import pygame as pg
import argparse
import socket  # to be able to set default IP on connection screen to OUR IP

from src.Client.Screen.Screen import Screen
from src.utils.awesome_logging import setup_logger
from src.utils.general_constants import FPS


def main():
    """" The main function of the game. """
    # Get args
    args = get_args()

    pg.init()  # initializes pyGame

    # Logging
    setup_logger()  # initializes the logger

    screen = Screen(port=args.port, ip=args.ip, name=args.name)  # set up the screen

    # Setup the clock for a decent frame rate
    clock = pg.time.Clock()

    running = True  # variable to keep the main loop running

    while running:  # main loop
        # update screen & pass all the events in the queue for handling
        running = screen.update(pg.event.get(), pg.key.get_pressed())  
        clock.tick(FPS)  # Ensure program maintains a rate of 40 frames per second

    pg.quit()  # all done


def get_args():
    """" Function that performs argparse """
    # Create the parser
    parser = argparse.ArgumentParser(
        description='Client module for the juicethirstyfruitwarriors game!',
        epilog='Proudly delivered to you by Farkas Domonkos László, Molnár Petra and Márkos Zsolt'
    )
    parser.add_argument(
        '-p',
        '--port',
        action='store',
        help='specify the desired port number',
        default=12145
    )
    parser.add_argument(
        '-i',
        '--ip',
        action='store',
        help='specify the desired (default) ip',
        default=socket.gethostbyname(socket.gethostname())
    )
    parser.add_argument(
        '-n',
        '--name',
        action='store',
        help='specify the desired (default) name',
        default='Anonymus'
    )

    # Return with the executed parse_args()
    return parser.parse_args()


if __name__ == "__main__":
    main()
