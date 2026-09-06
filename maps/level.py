import pygame

from settings import FLOOR_COLOR, OBSTACLE_COLOR

class Level:
    def __init__(self, size):
        self.size = size

        self.floor_areas = [
            pygame.Rect(100, 100, 600, 400),
            pygame.Rect(500, 300, 500, 200),
            pygame.Rect(900, 150, 500, 500),
        ]

        self.obstacles = [
            pygame.Rect(300, 200, 100, 40),
            pygame.Rect(500, 350, 40, 120),
        ]

    @property
    def collision_rects(self):
        return self.obstacles

    def can_walk(self, movement_rect):
        for floor in self.floor_areas:
            if floor.contains(movement_rect):
                return True

        return False


    def can_move(self, rect):
        movement_rect = pygame.Rect(
            rect.left,
            rect.centery,
            rect.width,
            rect.height // 2
        )

        if not self.can_walk(movement_rect):
            return False

        for obstacle in self.obstacles:
            if movement_rect.colliderect(obstacle):
                return False

        return True

    def draw(self, screen, camera):
        for floor in self.floor_areas:
            pygame.draw.rect(
                screen,
                FLOOR_COLOR,
                camera.apply(floor)
            )

        for obstacle in self.obstacles:
            pygame.draw.rect(
                screen,
                OBSTACLE_COLOR,
                camera.apply(obstacle)
            )