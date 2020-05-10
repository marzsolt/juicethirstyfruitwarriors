import sched
import time
import argparse

from src.Server.Network_communication.Server import Server
from src.Server.Game.Game import Game
from src.utils.Timer import Timer
from src.utils.awesome_logging import setup_logger
from src.utils.general_constants import FPS


def main():
    # Get args
    args = get_args()

    def update():
        Timer.update()
        running = game.update()
        if running:
            s.enter(1.0/FPS, 1, update, ())  # call update again in 25 ms

    # Logging
    setup_logger()

    # Networking
    server = Server.get_instance(port=args.port)  # this shall be the first call of Server get instance
    server.start()

    # Game
    game = Game()

    # Setup regular update "loop"
    s = sched.scheduler(time.time, time.sleep)
    fps = 40.0
    s.enter(1.0/FPS, 1, update, ())
    s.run()


def get_args():
    # Create the parser
    parser = argparse.ArgumentParser(
        description='Server module for the juicethirstyfruitwarriors game!',
        epilog='Proudly delivered to you by Farkas Domonkos László, Molnár Petra and Márkos Zsolt'
    )
    parser.add_argument(
        '-p',
        '--port',
        action='store',
        help='specify the desired port number',
        default=12145
    )

    # Return with the executed parse_args()
    return parser.parse_args()


if __name__ == "__main__":
    main()
