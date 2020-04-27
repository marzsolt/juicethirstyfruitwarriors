import pygame as pg

from juicethirstyfruitwarriors.Client.Screen.Screen import Screen


def main():
    pg.init()

    screen = Screen()  # set up the screen

    # Setup the clock for a decent frame rate
    clock = pg.time.Clock()

    running = True  # variable to keep the main loop running

    while running:  # main loop
        # update screen & pass all the events in the queue for handling
        running = screen.update(pg.event.get(), pg.key.get_pressed())  
        clock.tick(40)  # Ensure program maintains a rate of 40 frames per second

    pg.quit()  # all done


if __name__ == "__main__":
    main()
