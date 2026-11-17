import pygame

from entities.enemies.angel.angel_beam import AngelBeam


class AngelForm2:
    RADIUS = 50

    IDLE_TIME = 1000
    CHARGE_TIME = 1000
    FIRE_TIME = 500

    def __init__(self, angel):
        self.angel = angel

        self.position = pygame.Vector2(angel.position)

        self.rect = pygame.Rect(0, 0, self.RADIUS * 2, self.RADIUS * 2)
        self.rect.center = self.position

        self.aim_direction = pygame.Vector2(0, 1)

        self.state = "idle"
        self.state_start = pygame.time.get_ticks()

        self.beam = None

    @property
    def projectile_blockers(self):
        return []

    def take_damage(self, damage):
        # Por enquanto qualquer dano representa um tiro no olho.
        self.angel.next_form()

    def release_objects(self):
        return []

    def attack(self, player, dt):
        if self.beam and self.beam.hits(player.rect):
            player.take_damage_over_time(
                self.beam.DAMAGE_PER_SECOND,
                dt
            )

    def _change_state(self, state, current_time):
        self.state = state
        self.state_start = current_time

    def update(self, target, dt):
        direction = pygame.Vector2(target) - self.position

        if direction.length_squared() == 0:
            return

        self.aim_direction = direction.normalize()

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.state_start

        if self.state == "idle":
            if elapsed >= self.IDLE_TIME:
                self._change_state("charging", current_time)

        elif self.state == "charging":
            if elapsed >= self.CHARGE_TIME:
                self._change_state("firing", current_time)

                self.beam = AngelBeam(self.position, self.aim_direction)

        elif self.state == "firing":
            self.beam.update(self.position, self.aim_direction)

            if elapsed >= self.FIRE_TIME:
                self._change_state("idle", current_time)

                self.beam = None

    def draw(self, screen, camera):
        center = camera.apply(self.rect).center

        pygame.draw.circle(screen, (255, 255, 255), center, self.RADIUS)

        if self.beam:
            self.beam.draw(screen, camera)
