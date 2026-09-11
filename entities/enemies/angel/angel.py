import pygame

from entities.enemies.angel.forms.angel_form_1 import AngelForm1
from entities.enemies.angel.forms.angel_form_2 import AngelForm2


class Angel:
    ADRENALINE_REWARD = 25

    def __init__(self, position):
        self.position = pygame.Vector2(position)

        self.health = 100
        self.max_health = 100

        self.form_index = 0
        self.released_objects = []

        self.forms = [
            AngelForm1(self),
            AngelForm2(self),
        ]

        self.current_form = self.forms[self.form_index]
        self.rect = self.current_form.rect

    @property
    def swords(self):
        return getattr(self.current_form, "swords", [])

    def next_form(self):
        self.released_objects.extend(
            self.current_form.release_objects()
        )

        self.form_index += 1

        if self.form_index >= len(self.forms):
            self.health = 0
            return

        self.current_form = self.forms[self.form_index]
        self.rect = self.current_form.rect

    def take_damage(self, damage):
        self.current_form.take_damage(damage)

    @property
    def dead(self):
        if self.form_index < len(self.forms):
            return False

        return self.health <= 0

    def update(self, target):
        self.current_form.update(target)
        self.rect = self.current_form.rect

    def draw(self, screen, camera):
        self.current_form.draw(screen, camera)