import game
import pygame

from pygame.locals import *


class SpriteSheet(object):

    """Helper class to load single images from a sprite sheet"""

    # This points to the sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        super(SpriteSheet, self).__init__()

        self.file_name = file_name

        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """Grab a single image out of the larger spritesheet."""

        # Create a blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller one
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(pygame.Color('black'))

        return image


class Player(pygame.sprite.Sprite):

    """The player that is going to run around in the world"""

    # Image, Animation and Movement Variables
    walking_frames_l = []
    walking_frames_r = []
    direction = 'R'

    def __init__(self):
        super(Player, self).__init__()

        # Set the visuals and the position
        sprite_sheet = SpriteSheet('p1_walk.png')

        # TODO: Transform into list comprehension
        # Load all the right facing images into a list
        # Then flip the image and load it into left facing list
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Load the first image
        self.image = self.walking_frames_r[0]

        # Set the collider to match the image
        self.rect = self.image.get_rect()


class Gestrandet(game.Game):

    """A copy of the game GESTRANDET."""

    def __init__(self):
        super(Gestrandet, self).__init__(width=1280, height=786)

        # TODO: shall we add caves and stuff?
        # List of the levels in the game
        # self.levels = []

        # List of all the sprites in the game
        self.all_sprites = pygame.sprite.Group()

        # Add the player to the list
        self.player = Player()
        self.all_sprites.add(self.player)

        # List of all the colliders in the current level
        self.all_collider = pygame.sprite.Group()

    def update(self, delta):
        self.player.update(delta)

    def evnt_hndlr(self, event):
        pass

    def draw(self, surf):
        self.all_sprites.draw(surf)


def main():
    gs = Gestrandet()
    gs.run()

if __name__ == '__main__':
    main()
