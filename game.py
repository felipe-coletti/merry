import pygame

from graphics.camera import Camera
from ui.hud import HUD
from maps.map import Map

from entities.characters.harlequin import Harlequin

from effects.blood_pool import BloodPool

from settings import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(SCREEN_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.game_over = False

        self.camera = Camera(self.screen.get_size())
        self.hud = HUD()

        self.current_level = 0
        self.level = Map.get_level(
            self.current_level
        )

        self.ammo_pickups = []
        self.projectiles = []
        self.enemies = []
        self.blood = []
        self.dropped_swords = []

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


    def create_blood(self, position):
        blood = BloodPool(position)
        self.blood.append(blood)


    def restart(self):
        self.level = Map.get_level(self.current_level)

        self.ammo_pickups.clear()
        self.projectiles.clear()
        self.enemies.clear()
        self.blood.clear()
        self.dropped_swords.clear()

        self.player = Harlequin(
            self.level.player_spawn
        )

        self.create_level_entities()

        self.game_over = False


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()

                continue

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

            released_objects = getattr(
                enemy,
                "released_objects",
                []
            )

            if released_objects:
                self.dropped_swords.extend(released_objects)
                enemy.released_objects.clear()

            if hasattr(enemy, "damages_player"):
                if enemy.damages_player(self.player):
                    self.player.take_damage(enemy.DAMAGE)


    def update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile.update()

            projectile_removed = False

            distance = projectile.previous_position.distance_to(
                projectile.position
            )

            steps = max(1, int(distance / 2))

            for i in range(1, steps + 1):
                position = projectile.previous_position.lerp(
                    projectile.position,
                    i / steps
                )

                test_rect = projectile.mask.get_rect(
                    center=position
                )

                for enemy in self.enemies:
                    for sword in getattr(enemy, "swords", []):
                        if sword.collides_with(
                            test_rect,
                            projectile.mask
                        ):
                            self.projectiles.remove(projectile)
                            projectile_removed = True
                            break

                    if projectile_removed:
                        break

                if projectile_removed:
                    break

            if projectile_removed:
                continue

            if not projectile_removed:
                for enemy in self.enemies[:]:
                    if enemy.rect.colliderect(
                        projectile.rect
                    ):
                        enemy.take_damage(25)

                        self.projectiles.remove(
                            projectile
                        )

                        projectile_removed = True

                        if enemy.dead:
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


    def update_blood(self):
        for blood in self.blood:
            blood.update()


    def update_dropped_swords(self):
        for sword in self.dropped_swords:
            sword.update()

            if sword.damages_player(self.player):
                self.player.take_damage(sword.DAMAGE)


    def update(self):
        if self.game_over:
            self.update_blood()
            return
    
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
        self.update_dropped_swords()
        self.update_projectiles()
        self.update_blood()

        self.player.update_adrenaline()

        if self.player.health <= 0:
            blood_position = self.player.rect.midbottom

            self.create_blood(blood_position)

            self.game_over = True


    def draw_game_over(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 72)
        text = font.render(
            "LOVE WINS",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=(
                self.screen.get_width() // 2,
                self.screen.get_height() // 2 - 30
            )
        )

        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 32)
        text = font.render(
            "Press R to try again",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=(
                self.screen.get_width() // 2,
                self.screen.get_height() // 2 + 40
            )
        )

        self.screen.blit(text, text_rect)


    def draw(self):
        self.screen.fill(SKY_COLOR)

        self.level.draw(
            self.screen,
            self.camera
        )

        for blood in self.blood:
            blood.draw(
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

        for sword in self.dropped_swords:
            sword.draw(self.screen, self.camera)

        for projectile in self.projectiles:
            projectile.draw(
                self.screen,
                self.camera
            )

        self.hud.draw(
            self.screen,
            self.player
        )

        if self.game_over:
            self.draw_game_over()


        pygame.display.flip()


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(FPS)