import pygame
from subprocess import Popen
import os
from os.path import join


class Player(pygame.sprite.Sprite):
    WHITE = (255, 255, 255)
    VELOCITY = 5
    GRAVITY = 1
    ANIMATION_DELAY = 3  # Frames per animation frame

    def __init__(self, x, y, width, height, screen):
        """
        Initialize the Player object as a sprite in a pygame application.

        This method sets up the player character in a pygame game. It initializes the player's position, dimensions,
        animation states, and movement properties. The player is represented as a sprite and can interact with the game
        environment through various methods defined in the class.

        Parameters:
        - x (int): The initial x-coordinate of the player on the screen.
        - y (int): The initial y-coordinate of the player on the screen.
        - width (int): The width of the player's sprite.
        - height (int): The height of the player's sprite.
        - screen (pygame.Surface): The game screen where the player will be rendered.

        Attributes:
        - screen (pygame.Surface): The game screen for rendering the player.
        - rect (pygame.Rect): The rectangle representing the player's position and dimensions.
        - mask (pygame.mask.Mask or None): The collision mask for the player, initially None.
        - SPRITES (dict): Loaded sprite sheets for the player's animations.
        - direction (str): The current direction the player is facing ('left' or 'right').
        - sprite (pygame.Surface): The current sprite image of the player.
        - animation_count (int): Counter for managing animation frames.
        - x_velocity (int): Horizontal velocity of the player.
        - y_velocity (int): Vertical velocity of the player.
        - is_jumping (bool): Flag indicating whether the player is currently jumping.
        - jump_count (int): Counter for managing jump mechanics.
        - fall_count (int): Counter for managing falling mechanics.
    """
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)

        # Sprites
        self.SPRITES = self.load_sprite_sheets(
            "MainCharacters/NinjaFrog", 32, 32, True)
        self.direction = "left"
        self.sprite = self.SPRITES[f"idle_{self.direction}"][0]
        self.animation_count = 0

        self.mask = pygame.mask.from_surface(self.sprite)

        # Velocity
        self.x_velocity = 0
        self.y_velocity = 0
        self.offset_x = 0

        # Jumping
        self.is_jumping = False
        self.on_ground = False
        self.jump_count = 0
        self.fall_count = 0
        self.colliding = False

    def flip(self, sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    def load_sprite_sheets(self, path, width, height, direction=False):
        """
        Loads sprite sheets from a specified directory and processes them into animation frames.

        This method is used to load sprite sheets for animations in a pygame application. It scans a given directory
        for image files, loads each sprite sheet, and then splits it into individual animation frames based on the 
        specified width and height. Optionally, it can create mirrored versions of the sprites for multi-directional 
        animations (e.g., left and right facing).

        Parameters:
        - path (str): The subdirectory within 'assets' where the sprite sheets are located.
        - width (int): The width of each individual sprite frame in the sprite sheet.
        - height (int): The height of each individual sprite frame in the sprite sheet.
        - direction (bool, optional): If True, creates both 'left' and 'right' versions of the sprites. 
        Default is False.

        Returns:
        - animations (dict): A dictionary where each key is the name of an animation (derived from the sprite sheet filename) 
        and each value is a list of pygame.Surface objects representing the frames of that animation. If 
        'direction' is True, the dictionary contains both '_left' and '_right' versions of each animation.

        Example usage:
        >>> player = Player(...)
        >>> animations = player.load_sprite_sheets("character_sprites", 64, 64, True)
        """
        asset_path = join("assets", path)

        # Generates a list of all the image files in the asset directory
        sprite_sheets = [file for file in os.listdir(
            asset_path) if os.path.isfile(join(asset_path, file))]

        animations = {}

        for image in sprite_sheets:
            sheet = pygame.image.load(join(asset_path, image)).convert_alpha()
            sprites = []

            # Loops through the sprite sheet, frame by frame
            for i in range(0, sheet.get_width(), width):
                # Creates a new surface for each frame of the animation and appends it to the list of sprites
                ani_frame = pygame.Surface(
                    (width, height), pygame.SRCALPHA, 32)
                ani_size = pygame.Rect(i, 0, width, height)
                ani_frame.blit(sheet, (0, 0), ani_size)
                sprites.append(pygame.transform.scale2x(ani_frame))

            # If multi-directional, add both left and right versions of the sprites to the dictionary
            # removes the file extension from the filename
            if direction:
                animations[image.replace(".png", "") + "_right"] = sprites
                animations[image.replace(
                    ".png", "") + "_left"] = self.flip(sprites)
            else:
                animations[image.replace(".png", "")] = sprites

        return animations

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def jump(self):
        self.y_velocity = -self.GRAVITY * 8
        self.jump_count += 1
        self.is_jumping = True
        self.on_ground = False

    def move_left(self):
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

        self.x_velocity = -self.VELOCITY

    def move_right(self):
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

        self.x_velocity = self.VELOCITY

    def draw(self, *args):
        self.screen.blit(self.sprite, (self.rect.x -
                         self.offset_x, self.rect.y))

    def handle_movement(self, objects):
        keys = pygame.key.get_pressed()
        self.x_velocity = 0
        collided_left = self.collide_check(objects, -self.VELOCITY)
        collided_right = self.collide_check(objects, self.VELOCITY)

        if keys[pygame.K_a] and not collided_left:
            self.move_left()
        if keys[pygame.K_d] and not collided_right:
            self.move_right()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.jump()

        self.handle_vertical_collision(objects, self.y_velocity)

    def handle_vertical_collision(self, objects, dy):
        collided_objects = []

        for obj in objects:
            if pygame.sprite.collide_mask(self, obj) and dy > 0.5:
                self.colliding = True
                self.rect.bottom = obj.rect.top
                self.y_velocity = 0
                self.fall_count = 0
                self.is_jumping = False
                self.on_ground = True
                collided_objects.append(obj)

            if pygame.sprite.collide_mask(self, obj) and dy < -0.5:
                self.rect.top = obj.rect.bottom
                self.move(0, -dy * 10)
                self.y_velocity = self.GRAVITY
                self.update_colliders()
                self.fall_count = 0
                collided_objects.append(obj)

        return collided_objects

    def collide_check(self, objects, dx):
        self.move(dx, 0)
        self.update_colliders()

        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                self.move(-dx, 0)
                self.update_colliders()
                return obj

    def fall(self):
        # Player is falling at least 1 pixel per frame, until it hits terminal velocity
        self.y_velocity += min(1, (self.fall_count / 60) * self.GRAVITY)
        self.fall_count += 1

    def update_sprite(self):
        animation = "idle"

        if self.x_velocity != 0:
            animation = "run"

        if self.is_jumping:
            animation = "jump"

        if self.is_jumping and self.y_velocity < 0:
            animation = "fall"

        animation = f"{animation}_{self.direction}"
        sprites = self.SPRITES[animation]

        # Selects animation frame based on delay and animation count
        ani_frame = (self.animation_count //
                     self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[ani_frame]
        self.animation_count += 1
        self.update_colliders()

    def update_colliders(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def loop(self, objects):
        # if not self.on_ground:
        self.fall()
        self.handle_movement(objects)
        self.move(self.x_velocity, self.y_velocity)
        self.update_sprite()


if __name__ == "__main__":
    Popen("python main.py", shell=True)
