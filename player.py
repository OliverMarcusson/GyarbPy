import pygame
from subprocess import Popen

WHITE = (255, 255, 255)


class Player:
    def __init__(self, screen):
        self.screen = screen  # Pygame screen

        # Position
        self.x = 50
        self.y = 500

        # Size
        self.width = 40
        self.height = 60

        # Movement
        self.vel = 200
        self.jump_count = 36
        self.def_jump_count = self.jump_count
        self.is_jumping = False

    def draw(self):
        # Draw the player as a rectangle (you can later replace this with an image)
        pygame.draw.rect(
            self.screen, WHITE, (self.x, self.y, self.width, self.height))

    def pos(self):
        print(self.x, self.y)

    def goto(self, x, y):
        self.x = x
        self.y = y

    def move(self, dt):
        keys = pygame.key.get_pressed()

        # Move Left
        if keys[pygame.K_LEFT]:
            self.x -= self.vel * dt

        # Move Right
        if keys[pygame.K_RIGHT]:
            self.x += self.vel * dt

        # Handle Jumping
        if not self.is_jumping:  # If not jumping, check if the player is trying to jump
            if keys[pygame.K_UP]:
                self.is_jumping = True

        else:  # If jumping, jump
            if self.is_jumping:
                if self.jump_count >= -self.def_jump_count:
                    neg = 1
                    if self.jump_count < 0:
                        neg = -1
                    self.y -= (self.jump_count ** 2) * 0.5 * neg * dt
                    self.jump_count -= 1
                else:
                    self.is_jumping = False
                    self.jump_count = self.def_jump_count


if __name__ == "__main__":
    Popen("python main.py", shell=True)
