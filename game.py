import pygame
import os

from graphics.camera import Camera
from graphics.character_skin import CharacterSkin

from ui.hud import HUD

from maps.level import Level

from entities.weapon import Weapon
from entities.player import Player
from entities.ammo_pickup import AmmoPickup
from entities.enemies.butterfly import Butterfly

from settings import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(SCREEN_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.camera = Camera(self.screen.get_size())
        self.level = Level((1600, 1200))

        self.hud = HUD()

        self.current_level = 0

        self.ammo_pickups = []

        self.projectiles = []

        self.enemies = []

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

        self.level_bounds = pygame.Rect(
            (0, 0),
            self.level.size
        )

        self.player = Player(skin, start_pos, weapon, self.level_bounds)

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

        self.ammo_pickups.append(
            AmmoPickup(
                ammo_image,
                (1000, 400)
            )
        )

        butterfly_image = os.path.join(
            "assets",
            "images",
            "enemies",
            "butterfly",
            "butterfly.png"
        )

        self.enemies.append(
            Butterfly(
                butterfly_image,
                (600, 300),
                scale=1.5,
            )
        )

        self.enemies.append(
            Butterfly(
                butterfly_image,
                (200, 400),
                scale=1.5,
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


    def update_ammo_pickups(self):
        for pickup in self.ammo_pickups[:]:
            if self.player.rect.colliderect(pickup.rect):
                self.player.weapon.add_ammo(
                    pickup.AMMO_AMOUNT
                )

                self.ammo_pickups.remove(pickup)


    def update_enemies(self):
        for enemy in self.enemies[:]:
            enemy.update(self.player.center)

            if enemy.rect.colliderect(self.player.rect):
                self.player.take_damage(10)


    def update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile.update()

            for enemy in self.enemies[:]:
                if enemy.rect.colliderect(projectile.rect):
                    enemy.take_damage(1)
                    self.projectiles.remove(projectile)

                    if enemy.health <= 0:
                        self.enemies.remove(enemy)

                        self.player.add_adrenaline(
                            enemy.ADRENALINE_REWARD
                        )

                    break

            if not self.level_bounds.collidepoint(projectile.position):
                self.projectiles.remove(projectile)
    

    def update(self):
        keys = pygame.key.get_pressed()

        self.player.update(
            keys,
            self.level,
            self.camera
        )

        self.camera.update(
            self.player.rect,
            self.level.size
        )

        self.update_ammo_pickups()
        self.update_enemies()
        self.update_projectiles()

        self.player.update_adrenaline()

    
    def draw(self):
        self.screen.fill(SKY_COLOR)

        self.level.draw(self.screen, self.camera)

        for pickup in self.ammo_pickups:
            pickup.draw(self.screen, self.camera)

        self.player.draw(
            self.screen,
            self.camera
        )

        for enemy in self.enemies:
            enemy.draw(
                self.screen,
                self.camera
            )

        for projectile in self.projectiles:
            projectile.draw(
                self.screen,
                self.camera
            )

        self.hud.draw(
            self.screen,
            self.player
        )

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(FPS)