import math

import pygame

from entities.enemies.angel.angel_sword import AngelSword
from entities.enemies.angel.movement import keep_distance
from utils.angles import angle_difference
from utils.assets import load_image


class AngelForm1:
    ANGEL_SCALE = 3

    # 3 tiros da Magnum (25 de dano cada).
    HEALTH = 75

    TRANSFORMATION_TIME = 1000

    # Fica longe o bastante para o jogador não encostar nas espadas em
    # órbita, mas perto o bastante para a estocada alcançá-lo.
    MOVE_SPEED = 100
    PREFERRED_DISTANCE = 220
    DISTANCE_TOLERANCE = 30

    # Tempo entre o fim de uma estocada e o início da próxima.
    ATTACK_COOLDOWN = 1000

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

        self.attacking_sword = None
        self.last_attack_end = 0

        # Alcance da ponta da espada no auge da estocada.
        self.attack_range = (
            AngelSword.ORBIT_RADIUS
            + AngelSword.STAB_DISTANCE
            + self.swords[0].length / 2
        )

    def enter(self):
        self.rect.center = self.angel.position
        self.last_attack_end = pygame.time.get_ticks()

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

        self.attacking_sword = None

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

    def _update_attack(self, target):
        current_time = pygame.time.get_ticks()

        if self.attacking_sword:
            if not self.attacking_sword.attacking:
                self.attacking_sword = None
                self.last_attack_end = current_time

            return

        if current_time - self.last_attack_end < self.ATTACK_COOLDOWN:
            return

        offset = pygame.Vector2(target) - self.angel.position

        if offset.length() > self.attack_range:
            return

        # Usa a espada que menos precisa girar para apontar ao jogador.
        target_angle = math.degrees(math.atan2(offset.y, offset.x))

        self.attacking_sword = min(
            self.swords,
            key=lambda sword: abs(angle_difference(sword.angle, target_angle))
        )

        self.attacking_sword.start_attack()

    def _update_movement(self, target, dt, level):
        # Parado durante a transformação e durante a estocada, para o
        # ataque ser legível.
        if self.transforming or self.attacking_sword:
            return

        position = keep_distance(
            self.angel.position,
            target,
            self.PREFERRED_DISTANCE,
            self.DISTANCE_TOLERANCE,
            self.MOVE_SPEED,
            dt
        )

        self.angel.move_to(position, level)

        self.rect.center = self.angel.position

    def update(self, target, dt, level):
        self._update_movement(target, dt, level)

        if not self.transforming:
            self._update_attack(target)

        for sword in self.swords:
            if sword.released:
                sword.update(dt)
            else:
                sword.update_orbit(self.rect.center, target, dt)

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
