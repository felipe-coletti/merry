import pygame

class Level:
    def __init__(self, size):
        self.size = size
        self.floor_color = (180, 180, 180)

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
        screen.fill(self.floor_color)
        
        for wall in self.walls:
            pygame.draw.rect(
                screen,
                (40, 40, 40),
                wall
            )

        for obstacle in self.obstacles:
            pygame.draw.rect(
                screen,
                (80, 80, 80),
                obstacle
            )