import pygame

from entities.enemies.enemy import Enemy
from entities.enemies.angel.forms.angel_form_1 import AngelForm1
from entities.enemies.angel.forms.angel_form_2 import AngelForm2


class Angel(Enemy):
    """Inimigo com várias formas; morre ao sair da última.

    Forma 1: espadas em órbita (dano por contato), cai com 3 tiros e
             solta as espadas no chão.
    Forma 2: olho que dispara um raio de dano contínuo; um tiro no
             olho mata.
    """

    ADRENALINE_REWARD = 25

    def __init__(self, position):
        super().__init__()

        self.position = pygame.Vector2(position)

        self.form_index = 0

        self.forms = [
            AngelForm1(self),
            AngelForm2(self),
        ]

        self.rect = self.current_form.rect

    @property
    def current_form(self):
        return self.forms[min(self.form_index, len(self.forms) - 1)]

    @property
    def dead(self):
        return self.form_index >= len(self.forms)

    @property
    def projectile_blockers(self):
        if self.dead:
            return []

        return self.current_form.projectile_blockers

    def next_form(self):
        self.released_objects.extend(
            self.current_form.release_objects()
        )

        self.form_index += 1

        if not self.dead:
            self.rect = self.current_form.rect

    def take_damage(self, damage):
        if not self.dead:
            self.current_form.take_damage(damage)

    def attack(self, player, dt):
        if not self.dead:
            self.current_form.attack(player, dt)

    def update(self, target, dt):
        if self.dead:
            return

        self.current_form.update(target, dt)

        if not self.dead:
            self.rect = self.current_form.rect

    def draw(self, screen, camera):
        if not self.dead:
            self.current_form.draw(screen, camera)
