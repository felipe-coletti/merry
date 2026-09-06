import pygame

class Camera:
    def __init__(self, screen_size):
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]

        self.position = pygame.Vector2()

    def update(self, target, level_size):
        self.position.x = (
            target.centerx -
            self.screen_width / 2
        )

        self.position.y = (
            target.centery -
            self.screen_height / 2
        )

        max_x = level_size[0] - self.screen_width
        max_y = level_size[1] - self.screen_height

        self.position.x = max(
            0,
            min(self.position.x, max_x)
        )

        self.position.y = max(
            0,
            min(self.position.y, max_y)
        )

    def apply(self, rect):
        return rect.move(
            -self.position.x,
            -self.position.y
        )