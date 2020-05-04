import sched
import time

from src.Server.Network_communication.Server import Server
from src.Server.Game.Game import Game
from src.utils.Timer import Timer
from src.utils.awesome_logging import setup_logger


def main():
    def update():
        Timer.update()
        running = game.update()
        if running:
            s.enter(1.0/fps, 1, update, ())  # call update again in 25 ms

    # Logging
    setup_logger()

    # Networking
    server = Server.get_instance()
    server.start()

    # Game
    game = Game()

    # Setup regular update "loop"
    s = sched.scheduler(time.time, time.sleep)
    fps = 40.0
    s.enter(1.0/fps, 1, update, ())
    s.run()


if __name__ == "__main__":
    main()
