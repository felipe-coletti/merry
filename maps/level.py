import pygame

from settings import FLOOR_COLOR, OBSTACLE_COLOR

class Level:
    def __init__(
        self,
        size,
        player_spawn,
        floor_areas,
        obstacles,
        enemies,
        ammo
    ):
        self.size = size
        self.player_spawn = player_spawn

        self.floor_areas = floor_areas
        self.obstacles = obstacles

        self.enemies = enemies
        self.ammo = ammo

        self.bounds = pygame.Rect(
            (0, 0),
            self.size
        )


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