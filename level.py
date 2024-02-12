import pygame
from object import Object


WINDOW_WIDTH = 800
SCROLL_AREA_WIDTH = 200
WINDOW_HEIGHT = 600
FPS = 60


def floor_block(x, y, width, height, screen):
    block = Object(x, y, width, height, screen)
    block.load_texture((0, 0), (48, 48))
    return block


def course_block(x, y, width, height, screen):
    block = Object(x, y, width, height, screen)
    block.load_texture((208, 80), (32, 32))
    return block


def create_level(screen) -> pygame.sprite.Group:
    level = pygame.sprite.Group()
    
    # Ground
    for i in range(20):
        block = floor_block(i*96, WINDOW_HEIGHT - 96, 48, 48, screen)
        level.add(block)

    # Left wall
    for i in range(20):
        block = course_block(200 + i*64, WINDOW_HEIGHT -
                             96 - 256, 32, 32, screen)
        level.add(block)

    
    for i in range(10):
        block = floor_block(0, WINDOW_HEIGHT - i*96, 48, 48, screen)
        level.add(block)
