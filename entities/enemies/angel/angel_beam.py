import pygame


class AngelBeam:
    DAMAGE_PER_SECOND = 25

    LENGTH = 2000
    WIDTH = 8

    def __init__(self, position, direction):
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction).normalize()

    def update(self, position, direction):
        self.position = pygame.Vector2(position)

        if direction.length_squared() > 0:
            self.direction = pygame.Vector2(direction).normalize()

    def get_end_position(self):
        return self.position + self.direction * self.LENGTH

    def hits(self, rect):
        return bool(
            rect.clipline(
                tuple(self.position),
                tuple(self.get_end_position())
            )
        )

    def draw(self, screen, camera):
        offset = -camera.position

        pygame.draw.line(
            screen,
            (255, 255, 255),
            self.position + offset,
            self.get_end_position() + offset,
            self.WIDTH
        )
