import pygame

from entities.enemies.angel.angel_sword import AngelSword
from utils.assets import load_image


class AngelForm1:
    ANGEL_SCALE = 3

    # 3 tiros da Magnum (25 de dano cada).
    HEALTH = 75

    TRANSFORMATION_TIME = 1000

    SWORDS = (
        (45, 1),
        (135, -1),
        (225, 1),
        (315, -1),
    )

    def __init__(self, angel):
        self.angel = angel

        self.health = self.HEALTH

        self.image = pygame.transform.scale_by(
            load_image("images", "enemies", "angel", "angel_1", "angel.png"),
            self.ANGEL_SCALE
        )

        self.rect = self.image.get_rect(center=self.angel.position)

        sword_image = load_image(
            "images", "enemies", "angel", "angel_1", "angel_sword.png"
        )

        self.swords = [
            AngelSword(
                sword_image,
                self.rect.center,
                angle,
                rotation_direction=rotation_direction
            )
            for angle, rotation_direction in self.SWORDS
        ]

        self.transforming = False
        self.transformation_start = 0

    @property
    def projectile_blockers(self):
        return self.swords

    def take_damage(self, damage):
        if self.transforming:
            return

        self.health = max(0, self.health - damage)

        if self.health <= 0:
            self.transform()

    def transform(self):
        if self.transforming:
            return

        self.transforming = True
        self.transformation_start = pygame.time.get_ticks()

        for sword in self.swords:
            sword.release()

    def attack(self, player, dt):
        for sword in self.swords:
            if sword.released:
                hit = sword.damages_player(player)
            else:
                hit = sword.touches_player(player)

            if hit:
                player.take_damage(sword.DAMAGE)
                return

    def update(self, target, dt):
        for sword in self.swords:
            if sword.released:
                sword.update(dt)
            else:
                sword.update_orbit(self.rect.center, dt)

        if self.transforming:
            self.update_transformation()

    def release_objects(self):
        swords = self.swords
        self.swords = []

        return swords

    def update_transformation(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.transformation_start >= self.TRANSFORMATION_TIME:
            self.angel.next_form()

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))

        for sword in self.swords:
            sword.draw(screen, camera)
