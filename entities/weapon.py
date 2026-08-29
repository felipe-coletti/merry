import pygame

from entities.projectile import Projectile

class Weapon:
    def __init__(
            self,
            image_path,
            projectile_image_path,
            muzzle_flash_image_path,
            distance=30,
            projectile_speed=10,
            projectile_scale=0.5,
            muzzle_offset=(20, -3),
            fire_cooldown=150,
            recoil_amount=6,
            recoil_recovery=1
    ):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.projectile_image = pygame.image.load(projectile_image_path).convert_alpha()
        self.muzzle_flash_image = pygame.image.load(muzzle_flash_image_path).convert_alpha()

        self.distance = distance

        self.projectile_speed = projectile_speed
        self.projectile_scale = projectile_scale

        self.fire_cooldown = fire_cooldown
        self.last_shot = 0

        self.recoil = 0
        self.recoil_amount = recoil_amount
        self.recoil_recovery = recoil_recovery

        self.muzzle_flash_until = 0
        self.muzzle_flash_position = pygame.Vector2()
        self.muzzle_offset = pygame.Vector2(muzzle_offset[0], muzzle_offset[1])

        self.position = pygame.Vector2()
        self.direction = pygame.Vector2(1, 0)
        self.angle = 0


    def get_muzzle_position(self):
        offset = pygame.Vector2(self.muzzle_offset)

        if self.direction.x < 0:
            offset.y *= -1

        offset = offset.rotate(-self.angle)

        return self.position + offset


    def update(self, owner_center):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())
        owner_center = pygame.Vector2(owner_center)

        direction = mouse_position - owner_center

        if direction.length_squared() != 0:
            self.direction = direction.normalize()

            self.angle = self.direction.angle_to(
                pygame.Vector2(1, 0)
            )

        self.recoil = max(
            self.recoil - self.recoil_recovery,
            0
        )

        self.position = (
                owner_center
                + self.direction * (
                        self.distance - self.recoil
                )
        )

    def shoot(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot < self.fire_cooldown:
            return None

        self.last_shot = current_time

        self.recoil = self.recoil_amount

        muzzle_position = self.get_muzzle_position()

        self.muzzle_flash_position = muzzle_position
        self.muzzle_flash_until = current_time + 50

        return Projectile(
            self.projectile_image,
            muzzle_position,
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

        if pygame.time.get_ticks() < self.muzzle_flash_until:
            flash = pygame.transform.rotate(
                self.muzzle_flash_image,
                self.angle
            )

            flash_rect = flash.get_rect(
                center=self.muzzle_flash_position
            )

            screen.blit(flash, flash_rect)
