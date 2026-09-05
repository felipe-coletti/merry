import pygame

from settings import FLOOR_COLOR, WALL_COLOR, OBSTACLE_COLOR

class Level:
    def __init__(self, size):
        self.size = size

        self.walls = [
            pygame.Rect(0, 0, size[0], 20),
            pygame.Rect(
                0,
                size[1] - 20,
                size[0],
                20
            ),
            pygame.Rect(0, 0, 20, size[1]),
            pygame.Rect(
                size[0] - 20,
                0,
                20,
                size[1]
            ),
        ]

        self.obstacles = [
            pygame.Rect(300, 200, 100, 40),
            pygame.Rect(500, 350, 40, 120),
        ]

    @property
    def collision_rects(self):
        return self.walls + self.obstacles

    def draw(self, screen):
        screen.fill(FLOOR_COLOR)

        for wall in self.walls:
            pygame.draw.rect(
                screen,
                WALL_COLOR,
                wall
            )

        for obstacle in self.obstacles:
            pygame.draw.rect(
                screen,
                OBSTACLE_COLOR,
                obstacle
            )