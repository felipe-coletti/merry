import pygame
import os

from graphics.character_skin import CharacterSkin
from entities.weapon import Weapon
from entities.player import Player

from settings import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(SCREEN_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.current_level = 0

        self.projectiles = []

        skin = CharacterSkin(
            os.path.join(
                "assets",
                "images",
                "characters",
                "harlequin",
                "harlequin.png"
            )
        )

        start_pos = PLAYER_POSITIONS.get(
            self.current_level,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )

        weapon = Weapon(
            os.path.join(
                "assets",
                "images",
                "weapons",
                "magnum",
                "magnum.png"
            ),
            os.path.join(
                "assets",
                "images",
                "weapons",
                "magnum",
                "magnum_projectile.png"
            ),
            projectile_speed=30,
            projectile_scale=0.5,
            fire_cooldown=550
        )

        self.bounds = pygame.Rect(
            0,
            0,
            *SCREEN_SIZE
        )

        self.player = Player(skin, start_pos, weapon, self.bounds)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    projectile = self.player.weapon.shoot()

                    if projectile:
                        self.projectiles.append(projectile)

    def update(self):
        keys = pygame.key.get_pressed()

        self.player.update(keys)

        for projectile in self.projectiles:
            projectile.update()

            if not self.bounds.collidepoint(projectile.position):
                self.projectiles.remove(projectile)

    def draw(self):
        self.screen.fill(SKY_COLOR)

        self.player.draw(self.screen)

        for projectile in self.projectiles:
            projectile.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(FPS)