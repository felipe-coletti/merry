import pygame


class Projectile:
    # Distância (px) entre os pontos testados ao longo da trajetória,
    # para que projéteis rápidos não atravessem alvos.
    SWEEP_STEP = 2

    def __init__(self, image, position, direction, speed, damage, scale=0.5):
        """speed: pixels por segundo."""
        self.position = pygame.Vector2(position)
        self.previous_position = self.position.copy()

        self.direction = pygame.Vector2(direction).normalize()
        self.speed = speed
        self.damage = damage

        # A direção não muda durante o voo, então a imagem e a máscara
        # são calculadas uma única vez.
        angle = self.direction.angle_to(pygame.Vector2(1, 0))

        self.image = pygame.transform.rotate(
            pygame.transform.scale_by(image, scale),
            angle
        )

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt):
        self.previous_position = self.position.copy()

        self.position += self.direction * self.speed * dt

        self.rect.center = self.position

    def swept_rects(self):
        """Retângulos ao longo do caminho percorrido no último update."""
        distance = self.previous_position.distance_to(self.position)

        steps = max(1, int(distance / self.SWEEP_STEP))

        for i in range(1, steps + 1):
            position = self.previous_position.lerp(
                self.position,
                i / steps
            )

            yield self.mask.get_rect(center=position)

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
