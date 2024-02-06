import pygame
from player import Player
import os
from os.path import join
from object import Object

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

    def draw(self):
        # Draws the background tiles over the screen
        for tile in self.tiles:
            self.screen.blit(self.image, tile)


def draw(*args):
    """
    Draws all the objects passed in as arguments. Objects must be in the order they are to be drawn in.

    Parameters:
    - *args: Objects to be drawn. Must have a draw() method.
    """
    for arg in args:
        arg.draw()


def floor_block(x, y, width, height, screen):
    block = Object(x, y, width, height, screen)
    block.load_texture((0, 0), (48, 48))
    return block


def main():
    # Initialize PyGame, clock, screen and background
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Olivers och Isaks fantastiska platformer")
    clock = pygame.time.Clock()

    # Initialize game objects
    background = Background("Purple", screen)
    player = Player(100, 100, 50, 50, screen)
    # ground_block = Object(100, 300, 96, 96, screen)
    # ground_block.load_texture((0, 0), (48, 48))

    level = pygame.sprite.Group()
    for i in range(0, WINDOW_WIDTH + 1, 96):
        block = floor_block(i, WINDOW_HEIGHT - 96, 48, 48, screen)
        level.add(block)

    # Game loop
    running = True
    while running:
        clock.tick(FPS)

        # Checking for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # Player
        player.loop(level)

        # Drawing everything
        draw(background, player, *level)
        
        player_at_screen_right_edge = player.rect.right - player.offset_x >= WINDOW_WIDTH - SCROLL_AREA_WIDTH and player.x_velocity > 0
        player_at_screen_left_edge = player.rect.right - player.offset_x <= WINDOW_WIDTH - SCROLL_AREA_WIDTH and player.x_velocity > 0

        if player_at_screen_right_edge or player_at_screen_left_edge:
            player.offset_x += player.x_velocity
        
        pygame.display.update()

    # Quit the game when the game loop is exited
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
