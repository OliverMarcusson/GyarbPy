import pygame
from player import Player
from level import create_level
from background import Background
# import os
# from os.path import join
# from object import Object


WINDOW_WIDTH = 800
SCROLL_AREA_WIDTH = 200
WINDOW_HEIGHT = 600
FPS = 60


def draw(offset_x, *args):
    """
    Draws all the objects passed in as arguments. Objects must be in the order they are to be drawn in.

    Parameters:
    - *args: Objects to be drawn. Must have a draw() method.
    """
    for arg in args:
        arg.draw(offset_x)


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

    # Creating the level
    level = create_level(screen)

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
        draw(player.offset_x, background, player, *level)

        player_at_screen_right_edge = player.rect.right - \
            player.offset_x >= WINDOW_WIDTH - SCROLL_AREA_WIDTH and player.x_velocity > 0
        player_at_screen_left_edge = player.rect.left - \
            player.offset_x <= SCROLL_AREA_WIDTH and player.x_velocity < 0

        if player_at_screen_right_edge or player_at_screen_left_edge:
            player.offset_x += player.x_velocity

        pygame.display.update()

    # Quit the game when the game loop is exited
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
