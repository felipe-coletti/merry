import pygame
import os

from graphics.character_skin import CharacterSkin
from entities.weapon import Weapon
from entities.player import Player
from entities.ammo_pickup import AmmoPickup

from settings import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(SCREEN_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.font = pygame.font.Font(None, 24)

        self.current_level = 0

        self.ammo_pickups = []

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
            os.path.join(
                "assets",
                "images",
                "weapons",
                "magnum",
                "magnum_muzzle_flash.png"
            ),
            projectile_speed=30,
            projectile_scale=0.5,
            muzzle_offset=(37, -7),
            fire_cooldown=550,
            recoil_amount=8,
            recoil_recovery=2
        )

        self.bounds = pygame.Rect(
            0,
            0,
            *SCREEN_SIZE
        )

        self.player = Player(skin, start_pos, weapon, self.bounds)

        ammo_image = os.path.join(
            "assets",
            "images",
            "weapons",
            "magnum",
            "magnum_pickup.png"
        )

        self.ammo_pickups.append(
            AmmoPickup(
                ammo_image,
                (100, 100)
            )
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    projectile = self.player.weapon.shoot()

                    if projectile:
                        self.projectiles.append(projectile)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.player.weapon.reload()

    def update(self):
        keys = pygame.key.get_pressed()

        self.player.update(keys)

        for pickup in self.ammo_pickups[:]:
            if self.player.rect.colliderect(pickup.rect):
                self.player.weapon.add_ammo(
                    pickup.AMMO_AMOUNT
                )

                self.ammo_pickups.remove(pickup)

        for projectile in self.projectiles[:]:
            projectile.update()

            if not self.bounds.collidepoint(projectile.position):
                self.projectiles.remove(projectile)

    def draw(self):
        self.screen.fill(SKY_COLOR)

        for pickup in self.ammo_pickups:
            pickup.draw(self.screen)

        self.player.draw(self.screen)

        for projectile in self.projectiles:
            projectile.draw(self.screen)

        ammo_text = self.font.render(
            f"ammo: {self.player.weapon.ammo}/{self.player.weapon.capacity}\n"
            f"reserve_ammo: {self.player.weapon.reserve_ammo}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(ammo_text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(FPS)