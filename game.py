import pygame

from graphics.camera import Camera
from ui.hud import HUD
from maps.map import Map

from entities.characters.harlequin import Harlequin

from settings import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(SCREEN_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.camera = Camera(self.screen.get_size())
        self.hud = HUD()

        self.current_level = 0
        self.level = Map.get_level(
            self.current_level
        )

        self.ammo_pickups = []
        self.projectiles = []
        self.enemies = []

        self.player = Harlequin(
            self.level.player_spawn
        )

        self.create_level_entities()


    def create_level_entities(self):
        self.create_enemies()
        self.create_ammo_pickups()


    def create_enemies(self):
        for enemy_type, position in self.level.enemies:
            enemy = enemy_type(position)

            self.enemies.append(enemy)


    def create_ammo_pickups(self):
        for ammo_type, position in self.level.ammo:
            ammo = ammo_type(position)

            self.ammo_pickups.append(ammo)


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
            enemy.update(
                self.player.center
            )

            if enemy.rect.colliderect(
                self.player.rect
            ):
                self.player.take_damage(10)


    def update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile.update()

            projectile_removed = False

            for enemy in self.enemies[:]:
                if enemy.rect.colliderect(
                    projectile.rect
                ):
                    enemy.take_damage(1)

                    self.projectiles.remove(
                        projectile
                    )

                    projectile_removed = True

                    if enemy.health <= 0:
                        self.enemies.remove(enemy)

                        self.player.add_adrenaline(
                            enemy.ADRENALINE_REWARD
                        )

                    break

            if not projectile_removed:
                if not self.level.bounds.collidepoint(
                    projectile.position
                ):
                    self.projectiles.remove(
                        projectile
                    )


    def update(self):
        keys = pygame.key.get_pressed()

        self.camera.update(
            self.player.rect,
            self.level.size
        )

        self.player.update(
            keys,
            self.level,
            self.camera
        )

        self.update_ammo_pickups()
        self.update_enemies()
        self.update_projectiles()

        self.player.update_adrenaline()


    def draw(self):
        self.screen.fill(SKY_COLOR)

        self.level.draw(
            self.screen,
            self.camera
        )

        for pickup in self.ammo_pickups:
            pickup.draw(
                self.screen,
                self.camera
            )

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