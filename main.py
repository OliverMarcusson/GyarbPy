import pygame
from player import Player


def init(screen):
    player = Player(screen)
    return player


def main():
    # Initialize PyGame
    pygame.init()

    # Set up the display
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Gyarb Platformer")

    # Set up the clock
    clock = pygame.time.Clock()
    clock.tick(60)
    dt = clock.tick(60) / 1000

    # Initialize the player
    player = init(screen)

    # Game loop
    running = True
    while running:
        pygame.time.delay(10)
        # Checking for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Player actions
        player.move(dt)
        player.draw()

        pygame.display.update()

    # Quit the game when the game loop is exited
    pygame.quit()


if __name__ == '__main__':
    main()
