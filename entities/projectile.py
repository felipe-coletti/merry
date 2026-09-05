import pygame

class Projectile:
    def __init__(
            self,
            image,
            position,
            direction,
            speed=10,
            scale=0.5
    ):
        self.image = pygame.transform.scale_by( image, scale )
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction).normalize()
        self.speed = speed

        self.angle = self.direction.angle_to(
            pygame.Vector2(1, 0)
        )

        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.position += self.direction * self.speed
        self.rect.center = self.position

    def draw(self, screen):
        image = pygame.transform.rotate(
            self.image,
            self.angle
        )

        rect = image.get_rect(
            center=self.position
        )

        screen.blit(image, rect)
