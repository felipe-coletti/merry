import pygame


class AngelBeam:
    DAMAGE = 25

    LENGTH = 2000

    def __init__(self, position, direction):
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction).normalize()

    def update(self, position, direction):
        self.position = pygame.Vector2(position)

        if direction.length_squared() > 0:
            self.direction = pygame.Vector2(
                direction
            ).normalize()

    def get_end_position(self):
        return (
            self.position +
            self.direction * self.LENGTH
        )

    def draw(self, screen, camera):
        start = camera.apply(
            pygame.Rect(
                self.position.x,
                self.position.y,
                1,
                1
            )
        ).center

        end_position = self.get_end_position()

        end = camera.apply(
            pygame.Rect(
                end_position.x,
                end_position.y,
                1,
                1
            )
        ).center

        pygame.draw.line(
            screen,
            (255, 255, 255),
            start,
            end,
            8
        )