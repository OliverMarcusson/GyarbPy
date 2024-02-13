import pygame
from os.path import join


WINDOW_WIDTH = 800
SCROLL_AREA_WIDTH = 200
WINDOW_HEIGHT = 600
FPS = 60


class Background:
    def __init__(self, color, screen):
        self.screen = screen

        self.image = pygame.image.load(
            join("assets", "Background", color + ".png"))
        _, _, width, height = self.image.get_rect()

        self.tiles = []
        # Creates a list of tiles for the background
        for x in range(WINDOW_WIDTH // width + 1):
            for y in range(WINDOW_HEIGHT // height + 1):
                self.tiles.append((x * width, y * height))

    def draw(self, *args):
        # Draws the background tiles over the screen
        for tile in self.tiles:
            self.screen.blit(self.image, tile)
