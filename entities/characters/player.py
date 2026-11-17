import pygame

from entities.characters.character import Character


class Player(Character):
    MAX_HEALTH = 100
    DAMAGE_COOLDOWN = 500

    MAX_ADRENALINE = 100
    ADRENALINE_DECAY = 1
    ADRENALINE_DECAY_DELAY = 1000
    ADRENALINE_DECAY_COOLDOWN = 500

    # A cada MAX_ADRENALINE / ADRENALINE_SPEED_STEPS de adrenalina o
    # jogador ganha ADRENALINE_SPEED_PER_STEP pixels/s de velocidade.
    ADRENALINE_SPEED_STEPS = 5
    ADRENALINE_SPEED_PER_STEP = 60

    MOVEMENT_KEYS = (
        ((pygame.K_LEFT, pygame.K_a), "left", (-1, 0)),
        ((pygame.K_RIGHT, pygame.K_d), "right", (1, 0)),
        ((pygame.K_UP, pygame.K_w), "up", (0, -1)),
        ((pygame.K_DOWN, pygame.K_s), "down", (0, 1)),
    )

    def __init__(self, skin, position, weapon):
        super().__init__(skin, position)

        self.max_health = self.MAX_HEALTH
        self.health = self.max_health
        self.last_damage = -self.DAMAGE_COOLDOWN

        self.max_adrenaline = self.MAX_ADRENALINE
        self.adrenaline = 0
        self.last_adrenaline = 0
        self.last_adrenaline_decay = 0

        self.weapon = weapon

        self.previous_position = self.position

    @property
    def dead(self):
        return self.health <= 0

    def take_damage(self, damage):
        """Dano de impacto: respeita a invencibilidade após cada golpe."""
        current_time = pygame.time.get_ticks()

        if current_time - self.last_damage < self.DAMAGE_COOLDOWN:
            return

        self.last_damage = current_time
        self.health = max(0, self.health - damage)

    def take_damage_over_time(self, damage_per_second, dt):
        """Dano contínuo (ex.: raios): ignora a invencibilidade."""
        self.health = max(0, self.health - damage_per_second * dt)

    def add_adrenaline(self, amount):
        self.adrenaline = min(
            self.adrenaline + amount,
            self.max_adrenaline
        )

        self.last_adrenaline = pygame.time.get_ticks()

    def update_adrenaline(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_adrenaline < self.ADRENALINE_DECAY_DELAY:
            return

        if current_time - self.last_adrenaline_decay < self.ADRENALINE_DECAY_COOLDOWN:
            return

        self.last_adrenaline_decay = current_time

        self.adrenaline = max(0, self.adrenaline - self.ADRENALINE_DECAY)

    def current_speed(self):
        step = self.max_adrenaline // self.ADRENALINE_SPEED_STEPS

        return self.speed + (
            self.adrenaline // step * self.ADRENALINE_SPEED_PER_STEP
        )

    def move(self, velocity, dt, level):
        # Cada eixo é testado separadamente para permitir deslizar
        # ao longo de paredes.
        for axis in (0, 1):
            new_position = self.float_position.copy()
            new_position[axis] += velocity[axis] * dt

            new_rect = self.rect.copy()
            new_rect.topleft = (
                round(new_position.x),
                round(new_position.y)
            )

            if level.can_move(new_rect):
                self.float_position = new_position
                self.rect.topleft = new_rect.topleft

    @property
    def moved(self):
        return self.position != self.previous_position

    def update(self, keys, level, dt):
        self.previous_position = self.position

        direction = pygame.Vector2()

        for key_codes, facing, step in self.MOVEMENT_KEYS:
            if any(keys[key] for key in key_codes):
                self.direction = facing
                direction += step

        moving = direction.length_squared() > 0

        if moving:
            # Normaliza para não andar mais rápido na diagonal.
            velocity = direction.normalize() * self.current_speed()
            self.move(velocity, dt, level)

        self.animate(moving, dt)

    def aim(self, camera, dt):
        self.weapon.update(self.center, camera.position, dt)

    def draw(self, screen, camera):
        super().draw(screen, camera)

        self.weapon.draw(screen, camera)
