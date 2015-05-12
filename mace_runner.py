import math
import pygame
import game

from pygame.locals import *


class Player(pygame.sprite.Sprite):

    """A player that is going to run around in the maze."""

    def __init__(self, x, y, width, height):
        super(Player, self).__init__()

        # Set the visuals and the position
        self.width = width
        self.height = height
        self.color = pygame.Color('red')
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Movement related varables
        self.old_x = 0
        self.old_y = 0
        self.x_dir = 0  # Should either be 1, 0 or -1
        self.y_dir = 0  # Should either be 1, 0 or -1
        self.speed = .2

        # Collision detections
        self.collider_list = []

    def update(self, delta):
        # Make sure delta x and y are in range [-1, 1]
        if self.x_dir:
            self.x_dir = math.copysign(1, self.x_dir)
        if self.y_dir:
            self.y_dir = math.copysign(1, self.y_dir)

        # Move the player
        self.old_x = self.rect.x
        self.old_y = self.rect.y

        # Move and check for collision in x direction
        self.rect.x = self.rect.x + self.x_dir * int(self.speed * delta)
        coll = pygame.sprite.spritecollide(self, self.collider_list, False)
        if coll:
            coll = coll[0]
            if self.x_dir > 0:
                self.rect.right = coll.rect.left
            else:
                self.rect.left = coll.rect.right

        # Move and check for collision in y direction
        self.rect.y = self.rect.y + self.y_dir * int(self.speed * delta)
        coll = pygame.sprite.spritecollide(self, self.collider_list, False)
        if coll:
            coll = coll[0]
            if self.y_dir > 0:
                self.rect.bottom = coll.rect.top
            else:
                self.rect.top = coll.rect.bottom


class Wall(pygame.sprite.Sprite):

    """Boundrys for the levels"""

    def __init__(self, x, y, width, height, color='blue'):
        super(Wall, self).__init__()

        # Set the visuals and the position
        self.width = width
        self.height = height
        self.color = pygame.Color(color)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Level(object):

    """Base class for all levels in this mace runner game.
    This class should not be use directly but only be extended"""

    def __init__(self):
        super(Level, self).__init__()
        self.wall_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()


class Level_01(Level):

    """First level"""

    def __init__(self, width, height):
        super(Level_01, self).__init__()

        walls = [
            # Outer lines
            (0, 0, width, 10),
            (0, 470, width, 10),
            (0, 0, 10, height),
            (630, 0, 10, height / 2 - 15),
            (630, height / 2 + 15, 10, height),

            (100, 40, 10, height - 80),
            (200, 40, 10, height - 80),
            (300, 40, 10, height - 80),
            (400, 40, 10, height - 80),
            (500, 40, 10, height - 80),
        ]

        for wall in walls:
            self.wall_list.add(Wall(
                                    wall[0],
                                    wall[1],
                                    wall[2],
                                    wall[3],
                                    color='red'))


class Level_02(Level):

    """Second level"""

    def __init__(self, width, height):
        super(Level_02, self).__init__()

        walls = [
            # Outer lines
            (0, 0, width, 10),
            (0, 470, width, 10),
            (0, 0, 10, height),
            (630, 0, 10, height / 2 - 15),
            (630, height / 2 + 15, 10, height),

            (40, 100, width - 80, 10),
            (40, 200, width - 80, 10),
            (40, height/2, width - 80, 10),
            (40, 400, width - 80, 10),
        ]

        for wall in walls:
            self.wall_list.add(Wall(wall[0], wall[1], wall[2], wall[3]))


class MaceRunner(game.Game):

    """A simple implementation of mace runner.
    Main takeaway should be changing levels/screens."""

    def __init__(self):
        super(MaceRunner, self).__init__()

        # List of all the levels in the game
        self.levels = []
        self.current_level = 0
        self.levels.append(Level_01(self.WINDOWWIDTH, self.WINDOWHEIGHT))
        self.levels.append(Level_02(self.WINDOWWIDTH, self.WINDOWHEIGHT))

        # List for all the sprites in the game
        self.all_sprites = pygame.sprite.Group()

        # Add the player to the list
        self.player = Player(40, 40, 15, 15)
        self.all_sprites.add(self.player)
        self.player.collider_list = self.levels[self.current_level].wall_list

    def update(self, delta):
        self.player.update(delta)

        # MAKE LEVEL TRANSITION
        if self.player.rect.x > self.WINDOWWIDTH:
            self.current_level = 1
            self.player.collider_list = self.levels[1].wall_list
            self.player.rect.topleft = (30, 30)

    def evnt_hndlr(self, event):
        if event.type == KEYDOWN:
            if event.key == K_d:
                self.player.x_dir += 1
            if event.key == K_a:
                self.player.x_dir += -1
            if event.key == K_s:
                self.player.y_dir += 1
            if event.key == K_w:
                self.player.y_dir += -1
        if event.type == KEYUP:
            if event.key == K_d:
                self.player.x_dir += -1
            if event.key == K_a:
                self.player.x_dir += 1
            if event.key == K_s:
                self.player.y_dir += -1
            if event.key == K_w:
                self.player.y_dir += 1

    def draw(self, surf):
        self.levels[self.current_level].wall_list.draw(surf)
        self.all_sprites.draw(surf)


def main():
    mr = MaceRunner()
    mr.run()

if __name__ == '__main__':
    main()
