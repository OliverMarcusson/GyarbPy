import pygame
import os
from os.path import join


class Object(pygame.sprite.Sprite):
    """
    A base class for drawable objects in a pygame application.

    Represents a generic object with basic attributes like position, size, and an image surface. 
    It's designed to be subclassed for specific types of objects in the game.

    Attributes:
    - screen (pygame.Surface): The screen where the object is drawn.
    - rect (pygame.Rect): A rectangle representing the object's position and size.
    - image (pygame.Surface): The surface on which the object's visual representation is drawn.
    - width (int): The width of the object.
    - height (int): The height of the object.
    - name (str, optional): An optional name for the object.

    Methods:
    - draw(screen): Draws the object on the specified screen.
    """

    def __init__(self, x, y, width, height, screen, name=None) -> None:
        """
    Initializes an Object instance with position, size, and screen attributes.

    Sets up the basic properties of a game object, including its position, dimensions, and the screen 
    where it will be rendered. It also creates an empty surface for the object's image.

    Parameters:
    - x (int): The x-coordinate of the object's position.
    - y (int): The y-coordinate of the object's position.
    - width (int): The width of the object.
    - height (int): The height of the object.
    - screen (pygame.Surface): The screen where the object will be drawn.
    - name (str, optional): A name for the object. Defaults to None.
    """
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.mask = pygame.mask.from_surface(self.image)
        self.width = width
        self.height = height
        self.name = name

    def load_texture(self, xy: tuple[int, int], size: tuple[int, int], path="./assets/Terrain/Terrain.png"):
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        rect = pygame.Rect(*xy, *size)
        surface.blit(image, (0, 0), rect)
        self.image = pygame.transform.scale2x(surface)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, offset_x):
        self.screen.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    """
    A class representing a block in a pygame application, subclassing Object.

    This class is specific to block-like objects in the game. It includes functionality 
    for loading a texture and applying it to the block's surface.

    Attributes:
    - mask (pygame.Mask): A mask for pixel-perfect collision detection.

    Methods:
    - load_texture(xy, size): Loads a texture for the block from a sprite sheet.
    """

    def __init__(self, x, y, size, screen, name=None) -> None:
        """
    Initializes a Block instance as a square object with texture.

    Creates a block with a specified size and loads its texture. Inherits from the Object class and 
    includes additional functionality for handling texture loading and collision detection.

    Parameters:
    - x (int): The x-coordinate of the block's position.
    - y (int): The y-coordinate of the block's position.
    - size (int): The size (width and height) of the block.
    - screen (pygame.Surface): The screen where the block will be drawn.
    - name (str, optional): A name for the block. Defaults to None.
    """
        super().__init__(x, y, size, size, screen, name=name)
        self.image = self.load_texture((96, 0), (96, 96))
        self.mask = pygame.mask.from_surface(self.image)

    def load_texture(self, xy: tuple[int, int], size: tuple[int, int]):
        """
    Loads a specific texture from a sprite sheet for the Block object.

    This method is designed to extract a specific texture from a sprite sheet, using the provided coordinates and size. 
    It loads the image from a predetermined path (assets/Terrain/Block.png), extracts the specified area, and 
    then scales it up by a factor of 2. This texture is intended to be used as the visual representation of the Block 
    object in a pygame application.

    Parameters:
    - xy (tuple): A tuple containing the (x, y) coordinates of the top-left corner of the texture on the sprite sheet.
    - size (tuple): A tuple containing the (width, height) of the texture to be extracted.

    Returns:
    - pygame.Surface: A pygame Surface object representing the scaled-up texture extracted from the sprite sheet.

    Example usage:
    >>> block = Block(100, 100, 50, screen)
    >>> texture = block.load_texture((96, 0), (50, 50))
    """
        path = join("assets", "Terrain", "Block.png")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface(size, pygame.SRCALPHA, 32)
        # 96 is the x-coordinate of the block texture in the sprite sheet
        rect = pygame.Rect(*xy, *size)
        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)
