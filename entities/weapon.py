import pygame

from entities.projectile import Projectile

class Weapon:
    def __init__(
            self,
            image_path,
            projectile_image_path,
            distance=30,
            barrel_length=20,
            projectile_speed=10,
            projectile_scale=0.5,
            fire_cooldown=150
    ):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.projectile_image = pygame.image.load(projectile_image_path).convert_alpha()

        self.distance = distance

        self.barrel_length = barrel_length
        self.projectile_speed = projectile_speed
        self.projectile_scale = projectile_scale

        self.fire_cooldown = fire_cooldown
        self.last_shot = 0

        self.position = pygame.Vector2()
        self.direction = pygame.Vector2(1, 0)
        self.angle = 0

    def update(self, owner_center):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        owner_center = pygame.Vector2(owner_center)

        direction = mouse_position - owner_center

        if direction.length_squared() == 0:
            return

        self.direction = direction.normalize()

        self.angle = self.direction.angle_to(
            pygame.Vector2(1, 0)
        )

        self.position = (
            owner_center
            + self.direction * self.distance
        )

    def shoot(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot < self.fire_cooldown:
            return None

        self.last_shot = current_time

        barrel_position = self.position + self.direction * self.barrel_length

        return Projectile(
            self.projectile_image,
            barrel_position,
            self.direction,
            self.projectile_speed,
            self.projectile_scale
        )


    def draw(self, screen):
        image = self.image

        if self.direction.x < 0:
            image = pygame.transform.flip(
                image,
                False,
                True
            )

        image = pygame.transform.rotate(
            image,
            self.angle
        )

        rect = image.get_rect(center=self.position)

        screen.blit(image, rect)
