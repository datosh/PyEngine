import math
import game
import random
import pygame

from pygame.locals import *


class Block(pygame.sprite.Sprite):

    """Implements a basic block in the game using pygames Sprite class"""

    def __init__(self, x=0, y=0):
        super(Block, self).__init__()

        self.image = pygame.Surface([32, 16])
        self.image.fill(pygame.Color('green'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):

    """Implements the ball that is going to bust the bricks"""

    def __init__(self, x, y, screen_width, screen_height):
        super(Ball, self).__init__()
        self.width = 6
        self.height = self.width
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(pygame.Color('black'))
        pygame.draw.circle(self.image,
                           pygame.Color('yellow'),
                           (int(self.width / 2), int(self.height / 2)),
                           int(self.width / 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = -(math.pi / 2)
        self.speed = 0
        self.alive = True
        self.SPIN = 0.04
        self.DEFAULT_SPEED = 4

        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        area = pygame.display.get_surface().get_rect()
        assert area, "Couldn't retrieve display surface"

        dx = self.speed * math.cos(self.angle)
        dy = self.speed * math.sin(self.angle)
        self.rect.move_ip((dx, dy))

        # Collision with the window, i.e. keep ball in window
        if not area.contains(self.rect):
            tl = not area.collidepoint(self.rect.topleft)
            tr = not area.collidepoint(self.rect.topright)
            bl = not area.collidepoint(self.rect.bottomleft)
            br = not area.collidepoint(self.rect.bottomright)
            if (tr and tl) or (br and bl):
                self.angle = -self.angle
            if (tl and bl) or (tr and br):
                self.angle = math.pi - self.angle

        # If ball is at bottom of screen, ball is dead
        if self.screen_height - self.rect.y < self.height:
            self.alive = False

    def collide_with(self, colls):
        for coll in colls:
            if self.screen_height - self.rect.y < 100:
                dist = self.rect.centerx - coll.rect.centerx
                self.angle = (-math.pi / 2) + (dist * self.SPIN)
            elif not coll.rect.contains(self.rect):
                tl = not coll.rect.collidepoint(self.rect.topleft)
                tr = not coll.rect.collidepoint(self.rect.topright)
                bl = not coll.rect.collidepoint(self.rect.bottomleft)
                br = not coll.rect.collidepoint(self.rect.bottomright)
                if (tr and tl) or (br and bl):
                    self.angle = -self.angle
                if (tl and bl) or (tr and br):
                    self.angle = math.pi - self.angle


class Player(pygame.sprite.Sprite):

    """Implements the player of the BrickBuster game."""

    def __init__(self, x, y, screen_width):
        super(Player, self).__init__()
        self.width = 64
        self.height = 8
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(pygame.Color('blue'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.screen_width = screen_width

    def update(self):
        """Update the player location."""

        # Only update the x position of the player. Not y, since he is only
        # allowed to stay at the bottom of the screen
        new_x = pygame.mouse.get_pos()[0]
        if new_x < 0 + (self.width / 2):
            new_x = 0 + (self.width / 2)
        elif new_x > self.screen_width - self.width + self.width / 2:
            new_x = self.screen_width - self.width + self.width / 2
        self.rect.centerx = new_x


class BrickBuster(game.Game):

    """Implementing the old arcade game BrickBuster"""

    def __init__(self):
        super(BrickBuster, self).__init__()

        self.FPS = 120

        # Create a container for all sprites
        self.all_sprites = pygame.sprite.Group()

        # Create a container only for the blocks
        self.collide_sprites = pygame.sprite.Group()

        # Create some blocks and put them in their containers
        for x in range(130, 500, 50):
            for y in range(100, 300, 50):
                block = Block(x, y)
                self.all_sprites.add(block)
                self.collide_sprites.add(block)

        # Create the player
        self.player = Player(self.WINDOWWIDTH / 2,
                             self.WINDOWHEIGHT - 30,
                             self.WINDOWWIDTH)
        self.all_sprites.add(self.player)
        self.collide_sprites.add(self.player)

        # Create the ball
        self.ball = Ball(300, 300, self.WINDOWWIDTH, self.WINDOWHEIGHT)
        self.all_sprites.add(self.ball)

        # Some statistics
        self.score = 0

        # Font
        self.text_font = pygame.font.SysFont(None, 48)
        self.text_color = pygame.Color('white')

        # States
        self.intro = 'intro'
        self.playing = 'playing'
        self.gameover = 'gameover'
        self.state = self.intro

    def evnt_hndlr(self, event):
        # INTRO
        if self.state == self.intro:
            # If any key is pressed make the transition to playing state
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                self.state = self.playing
        # PLAYING
        elif self.state == self.playing:
            if event.type == MOUSEBUTTONDOWN:
                self.ball.speed = self.ball.DEFAULT_SPEED
        # GAMEOVER
        elif self.state == self.gameover:
            # If any key is pressed make a new game
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                self.__init__()

    def update(self, delta):
        # ---- INTRO ----
        if self.state == self.intro:
            pass
        # ---- PLAYING ----
        elif self.state == self.playing:
            # Get all sprites that collide with the ball. If the player is one
            # of them remove it from the list, and delete the remaining blocks
            colls = pygame.sprite.spritecollide(self.ball,
                                                self.collide_sprites,
                                                False)
            self.ball.collide_with(colls)
            if self.player in colls:
                colls.remove(self.player)
            self.score += len(colls)
            self.collide_sprites.remove(colls)
            self.all_sprites.remove(colls)

            # Update the player and the ball
            self.player.update()
            self.ball.update()

            # Test if the game is over
            if not self.ball.alive:
                self.state = self.gameover
        # ---- GAMEOVER ----
        elif self.state == self.gameover:
            pass

    def draw(self, surf):
        if self.state == self.intro:
            self.drawText(surf, 'Press a button to start', 140, 200)
        elif self.state == self.playing:
            self.all_sprites.draw(surf)
            self.drawText(surf, str(self.score), 10, 20)
        elif self.state == self.gameover:
            self.drawText(surf, 'Wanna play again?', 140, 200)
            self.drawText(surf,
                          'Your score was {}'.format(self.score),
                          140,
                          240)

    def drawText(self, surface, text, x, y):
        textobj = self.text_font.render(text, 1, self.text_color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


def main():
    bb = BrickBuster()
    bb.run()

if __name__ == '__main__':
    main()
