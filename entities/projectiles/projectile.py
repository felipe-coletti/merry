import pygame

class Projectile:
    def __init__(self, image, position, direction, speed=10, scale=0.5):
        self.image = pygame.transform.scale_by( image, scale )
        self.position = pygame.Vector2(position)
        self.previous_position = pygame.Vector2(position)

        self.direction = pygame.Vector2(direction).normalize()
        self.speed = speed

        self.angle = self.direction.angle_to(pygame.Vector2(1, 0))

        self.current_image = pygame.transform.rotate(
            self.image,
            self.angle
        )

        self.rect = self.current_image.get_rect(
            center=self.position
        )

        self.mask = pygame.mask.from_surface(
            self.current_image
        )

    def update(self):
        self.previous_position = self.position.copy()

        self.position += self.direction * self.speed

        self.current_image = pygame.transform.rotate(
            self.image,
            self.angle
        )

        self.rect = self.current_image.get_rect(
            center=self.position
        )

        self.mask = pygame.mask.from_surface(
            self.current_image
        )

    def draw(self, screen, camera):
        image = pygame.transform.rotate(
            self.image,
            self.angle
        )

        rect = image.get_rect(
            center=self.position
        )

        rect = camera.apply(rect)

        screen.blit(image, rect)
