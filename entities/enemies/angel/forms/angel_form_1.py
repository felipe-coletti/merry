import os
import pygame

from entities.enemies.angel.angel_sword import AngelSword


class AngelForm1:
    DAMAGE = 20

    ANGEL_SCALE = 3

    TRANSFORMATION_HEALTH = 50
    TRANSFORMATION_TIME = 1000

    def __init__(self, angel):
        self.angel = angel

        self.image = self.load_image(
            os.path.join(
                "assets",
                "images",
                "enemies",
                "angel",
                "angel_1",
                "angel.png"
            ),
            self.ANGEL_SCALE
        )

        self.rect = self.image.get_rect(
            center=self.angel.position
        )

        sword_image = pygame.image.load(
            os.path.join(
                "assets",
                "images",
                "enemies",
                "angel",
                "angel_1",
                "angel_sword.png"
            )
        ).convert_alpha()

        center = self.rect.center

        self.swords = [
            AngelSword(
                sword_image,
                center,
                45,
                rotation_direction=1
            ),
            AngelSword(
                sword_image,
                center,
                135,
                rotation_direction=-1
            ),
            AngelSword(
                sword_image,
                center,
                225,
                rotation_direction=1
            ),
            AngelSword(
                sword_image,
                center,
                315,
                rotation_direction=-1
            )
        ]

        self.transforming = False
        self.transformation_start = 0

    def load_image(self, path, scale):
        image = pygame.image.load(path).convert_alpha()

        width = image.get_width() * scale
        height = image.get_height() * scale

        return pygame.transform.scale(
            image,
            (width, height)
        )

    def take_damage(self, damage):
        if self.transforming:
            return

        self.angel.health -= damage

        if self.angel.health <= self.TRANSFORMATION_HEALTH:
            self.angel.health = self.TRANSFORMATION_HEALTH
            self.transform()

    def transform(self):
        if self.transforming:
            return

        self.transforming = True
        self.transformation_start = pygame.time.get_ticks()

        for sword in self.swords:
            sword.release()

    def update(self, target):
        if self.transforming:
            self.update_transformation()
        else:
            self.update_swords()

        for sword in self.swords:
            sword.update()

    def update_swords(self):
        center = self.rect.center

        for sword in self.swords:
            if not sword.falling:
                sword.update_orbit(center)

    def release_objects(self):
        swords = self.swords
        self.swords = []

        return swords

    def update_transformation(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.transformation_start >= self.TRANSFORMATION_TIME:
            self.angel.next_form()

    def draw(self, screen, camera):
        rect = camera.apply(self.rect)

        screen.blit(
            self.image,
            rect
        )

        for sword in self.swords:
            sword.draw(screen, camera)