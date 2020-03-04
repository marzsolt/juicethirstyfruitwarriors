import pygame as pg


class Screen:
    screen = None
    h = None
    w = None
    screenState = 0 # 0: main menu; 1: connecting

    def __init__(self, screen_height=0, screen_width=0):
        self.screen = pg.display.set_mode([screen_width, screen_height], pg.FULLSCREEN)
        [self.h, self.w] = [pg.display.Info().current_h, pg.display.Info().current_w] # get screen h and w

    def update(self, events):

        # draw the adequate screen (according to the state)
        if self.screenState == 0:
            self.drawMainMenu(events)
        elif self.screenState == 1:
            self.drawConnecting()

        running = True
        for event in events: # event handling - look at every event in the queue

            if event.type == pg.KEYDOWN: # did the user hit a key?

                if event.key == pg.K_ESCAPE: # Was it the Escape key? If so, stop the loop.
                    running = False

            if event.type == pg.QUIT: # Did the user click the window close button? If so, stop the loop. w/o. doesn't work
                running = False

        pg.display.flip() # flip the display

        return running

    def drawMainMenu(self, events):
        self.screen.fill((255, 128, 0))  # some sort of orange

        playBtnSurf = pg.Surface([int(self.w*0.1), int(self.h*0.05)])
        playBtnSurf.fill((0, 0, 0)) # colour of border
        playBtnSurfRect = playBtnSurf.get_rect()
        playBtnSurfRect.center = (self.w//2, self.h//2)

        # Let the above surface have 1 px width border, whereas the actual object background be white
        tmpSurf = pg.Surface((playBtnSurf.get_width()-2, playBtnSurf.get_height()-2))
        tmpSurf.fill((255, 255, 255))
        playBtnSurf.blit(tmpSurf, (1, 1))


        font = pg.font.Font('freesansbold.ttf', 16)
        text = font.render('Play', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (playBtnSurf.get_width()//2, playBtnSurf.get_height()//2)

        playBtnSurf.blit(text, textRect)

        self.screen.blit(playBtnSurf, playBtnSurfRect)

        for event in events: # event handling - look at every event in the queue [main menu specific]
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button.
                    # Check if the rect collides with the mouse pos.
                    if playBtnSurfRect.collidepoint(event.pos):
                        self.screenState = 1

    def drawConnecting(self):
        self.screen.fill((255, 128, 0))  # some sort of orange

        font = pg.font.Font('freesansbold.ttf', 16)
        text = font.render('Connecting...', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.w // 2, self.h // 2)

        self.screen.blit(text, textRect)
