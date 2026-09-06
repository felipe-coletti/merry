import pygame

from graphics.camera import Camera

from ui.hud import HUD

from maps.level import Level

from entities.characters.harlequin import Harlequin
from entities.items.ammo.magnum_ammo import MagnumAmmo
from entities.enemies.butteflies.cyan_butterfly import CyanButterfly

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

        start_pos = PLAYER_POSITIONS.get(
            self.current_level,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )

        self.level_bounds = pygame.Rect(
            (0, 0),
            self.level.size
        )

        self.player = Harlequin(start_pos)        

        self.ammo_pickups.append(
            MagnumAmmo(
                (100, 100)
            )
        )

        self.ammo_pickups.append(
            MagnumAmmo(
                (1000, 400)
            )
        )

        self.enemies.append(
            CyanButterfly(
                (600, 300),
                scale=2
            )
        )

        self.enemies.append(
            CyanButterfly(
                (200, 400),
                scale=2
            )
        )

        self.enemies.append(
            CyanButterfly(
                (1000, 400),
                scale=2
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