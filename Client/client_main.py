import pygame as pg

# Self defined classes
import Screen


def main():
    pg.init()

    screen = Screen.Screen()  # set up the screen

    # Setup the clock for a decent frame rate
    clock = pg.time.Clock()

    running = True  # variable to keep the main loop running

    while running:  # main loop

        running = screen.update(pg.event.get())  # update screen & pass all the events in the queue for handling

        clock.tick(60)  # Ensure program maintains a rate of 60 frames per second

    pg.quit()  # all done


if __name__ == "__main__":
    main()
