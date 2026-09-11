import pygame

from entities.enemies.angel.angel_beam import AngelBeam


class AngelForm2:
    DAMAGE = 25

    CHARGE_TIME = 1000
    FIRE_TIME = 500

    def __init__(self, angel):
        self.angel = angel

        self.position = pygame.Vector2(
            angel.position
        )

        self.rect = pygame.Rect(
            0,
            0,
            100,
            100
        )

        self.rect.center = self.position

        self.aim_direction = pygame.Vector2(0, 1)

        self.state = "idle"
        self.state_start = pygame.time.get_ticks()

        self.beam = None

    def take_damage(self, damage):
        # Por enquanto:
        # qualquer dano representa um tiro no olho.
        self.angel.health = 0

    def update(self, target):
        target = pygame.Vector2(target)

        direction = target - self.position

        if direction.length_squared() == 0:
            return

        direction = direction.normalize()

        current_time = pygame.time.get_ticks()

        if self.state == "idle":
            self.aim_direction = direction

            if current_time - self.state_start >= 1000:
                self.state = "charging"
                self.state_start = current_time

        elif self.state == "charging":
            self.aim_direction = direction

            if current_time - self.state_start >= self.CHARGE_TIME:
                self.state = "firing"
                self.state_start = current_time

                self.beam = AngelBeam(
                    self.position,
                    self.aim_direction
                )

        elif self.state == "firing":
            self.aim_direction = direction

            if self.beam:
                self.beam.update(
                    self.position,
                    self.aim_direction
                )

            if current_time - self.state_start >= self.FIRE_TIME:
                self.state = "idle"
                self.state_start = current_time
                self.beam = None

    def draw(self, screen, camera):
        center = camera.apply(
            self.rect
        ).center

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            center,
            50
        )

        if self.beam:
            self.beam.draw(
                screen,
                camera
            )