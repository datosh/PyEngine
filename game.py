import pygame
import sys

from pygame.locals import *


def terminate():
    pygame.quit()
    sys.exit()


class Game(object):

    """This represents the abstract base class for any new game. Every new
    game should extend this calss"""

    def __init__(self, width=640, height=480):
        """Initializes the Game with a standard window size, fps and
        background color."""

        # Window
        self.WINDOWWIDTH = width
        self.WINDOWHEIGHT = height
        self.WINDOWDIMENSIONS = (self.WINDOWWIDTH, self.WINDOWHEIGHT)
        self.FPS = 60
        self.background_color = pygame.Color('black')

        self.quit_on_esc = True
        self.done = False

        pygame.init()
        self.surf = pygame.display.set_mode(self.WINDOWDIMENSIONS)
        self.clock = pygame.time.Clock()

    def __str__(self):
        return "game.Game: WIDTH = {}, HEIGHT = {}, FPS = {}".format(
            self.WINDOWWIDTH,
            self.WINDOWHEIGHT,
            self.FPS)

    def run(self):
        """The run functions implements the main loop of the game. The
        functions self.update and self.draw are called, and shall be
        overwritten by the super class do to something useful."""

        while not self.done:
            # wait for frame to pass
            delta = self.clock.tick(self.FPS)

            for event in pygame.event.get():
                # Terminate on X button
                if event.type == QUIT:
                    terminate()
                # Terminate on ESC
                if self.quit_on_esc:
                    if event.type == KEYDOWN and event.key == K_ESCAPE:
                        terminate()
                # pass event to event handler
                self.evnt_hndlr(event)
            # ---- EVENT HANDLING DONE ----

            # ---- UPDATE GAME OBJECTS ----
            self.update(delta)

            # ---- DRAW GAME OBJECTS ----
            self.surf.fill(self.background_color)
            self.draw(self.surf)
            pygame.display.update()

    def evnt_hndlr(self, event):
        pass

    def update(self, delta):
        pass

    def draw(self, surf):
        pass
