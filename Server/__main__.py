import sched
import time

from juicethirstyfruitwarriors.Server.Server import Server
from juicethirstyfruitwarriors.Server.Game import Game
from juicethirstyfruitwarriors.Server.Timer import Timer

def printer(every_s):
    print("I am being printed rougly every " + str(every_s) + " s")
    Timer.sch_fun(40*every_s, printer, (every_s,))
    
def hello_timer():
    print("Hello timer! :)")


def main():
    def update():
        s.enter(1.0/fps, 1, update, ())  # call update again in 25 ms
        Timer.update()
        game.update()

    # Networking
    server = Server.get_instance()
    server.start()

    # Game
    game = Game()

    Timer.sch_fun(40*5, printer, (5,))
    Timer.sch_fun(40*2, printer, (2,))
    Timer.sch_fun(40*3, hello_timer, ())

    # Setup regular update "loop"
    s = sched.scheduler(time.time, time.sleep)
    fps = 40.0
    s.enter(1.0/fps, 1, update, ())
    s.run()


if __name__ == "__main__":
    main()
