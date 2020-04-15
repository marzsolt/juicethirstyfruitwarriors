import sched
import time
from Server import Server
from Game import Game


def main():
    def update():
        s.enter(1.0/fps, 1, update, ())  # call update again in 25 ms
        game.update()

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
