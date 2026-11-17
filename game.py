import pygame

from effects.blood_pool import BloodPool
from entities.characters.harlequin import Harlequin
from graphics.camera import Camera
from maps.map import Map
from settings import FPS, MAX_DT, SCREEN_SIZE, SCREEN_TITLE, SKY_COLOR
from ui.hud import HUD


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(SCREEN_TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.camera = Camera(self.screen.get_size())
        self.hud = HUD()

        self.game_over_font = pygame.font.Font(None, 72)
        self.game_over_small_font = pygame.font.Font(None, 32)

        self.current_level = 0

        self.ammo_pickups = []
        self.projectiles = []
        self.enemies = []
        self.blood = []
        self.dropped_swords = []

        self.restart()

    def restart(self):
        self.level = Map.get_level(self.current_level)

        self.ammo_pickups.clear()
        self.projectiles.clear()
        self.enemies.clear()
        self.blood.clear()
        self.dropped_swords.clear()

        self.player = Harlequin(self.level.player_spawn)

        self.create_level_entities()

        self.game_over = False

    def create_level_entities(self):
        for enemy_type, position in self.level.enemies:
            self.enemies.append(enemy_type(position))

        for ammo_type, position in self.level.ammo:
            self.ammo_pickups.append(ammo_type(position))

    def create_blood(self, position):
        self.blood.append(BloodPool(position))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart()

                continue

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == pygame.BUTTON_LEFT
            ):
                projectile = self.player.weapon.shoot()

                if projectile:
                    self.projectiles.append(projectile)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.player.weapon.reload()

    def update_ammo_pickups(self):
        for pickup in self.ammo_pickups[:]:
            if self.player.rect.colliderect(pickup.rect):
                self.player.weapon.add_ammo(pickup.AMMO_AMOUNT)

                self.ammo_pickups.remove(pickup)

    def update_enemies(self, dt):
        for enemy in self.enemies:
            enemy.update(self.player.center, dt)
            enemy.attack(self.player, dt)

            self.dropped_swords.extend(enemy.pop_released_objects())

    def update_dropped_swords(self, dt):
        for sword in self.dropped_swords:
            sword.update(dt)

            if sword.damages_player(self.player):
                self.player.take_damage(sword.DAMAGE)

    def projectile_hit(self, projectile):
        """Aplica o primeiro impacto ao longo da trajetória.

        Retorna True se o projétil atingiu algo e deve ser removido.
        """
        for test_rect in projectile.swept_rects():
            for enemy in self.enemies:
                if enemy.dead:
                    continue

                for blocker in enemy.projectile_blockers:
                    if blocker.collides_with(test_rect, projectile.mask):
                        return True

                if enemy.rect.colliderect(test_rect):
                    enemy.take_damage(projectile.damage)
                    return True

        return False

    def update_projectiles(self, dt):
        for projectile in self.projectiles[:]:
            projectile.update(dt)

            if (
                self.projectile_hit(projectile)
                or not self.level.bounds.collidepoint(projectile.position)
            ):
                self.projectiles.remove(projectile)

    def remove_dead_enemies(self):
        for enemy in self.enemies[:]:
            if not enemy.dead:
                continue

            self.dropped_swords.extend(enemy.pop_released_objects())

            self.enemies.remove(enemy)

            self.player.add_adrenaline(enemy.ADRENALINE_REWARD)

    def update_blood(self, dt):
        for blood in self.blood:
            blood.update(dt)

    def update(self, dt):
        if self.game_over:
            self.update_blood(dt)
            return

        keys = pygame.key.get_pressed()

        # O jogador se move primeiro; a câmera o segue no mesmo frame e
        # só então a mira é calculada com a câmera já atualizada.
        self.player.update(keys, self.level, dt)
        self.camera.update(self.player.rect, self.level.size)
        self.player.aim(self.camera, dt)

        self.update_ammo_pickups()
        self.update_enemies(dt)
        self.update_dropped_swords(dt)
        self.update_projectiles(dt)
        self.remove_dead_enemies()
        self.update_blood(dt)

        self.player.update_adrenaline()

        if self.player.dead:
            self.create_blood(self.player.rect.midbottom)

            self.game_over = True

    def _draw_centered_text(self, text, font, offset_y):
        surface = font.render(text, True, (255, 255, 255))

        rect = surface.get_rect(
            center=(
                self.screen.get_width() // 2,
                self.screen.get_height() // 2 + offset_y
            )
        )

        self.screen.blit(surface, rect)

    def draw_game_over(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        self.screen.blit(overlay, (0, 0))

        self._draw_centered_text("LOVE WINS", self.game_over_font, -30)
        self._draw_centered_text(
            "Press R to try again",
            self.game_over_small_font,
            40
        )

    def draw(self):
        self.screen.fill(SKY_COLOR)

        self.level.draw(self.screen, self.camera)

        drawables = (
            self.blood
            + self.ammo_pickups
            + [self.player]
            + self.enemies
            + self.dropped_swords
            + self.projectiles
        )

        for drawable in drawables:
            drawable.draw(self.screen, self.camera)

        self.hud.draw(self.screen, self.player)

        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, MAX_DT)

            self.handle_events()
            self.update(dt)
            self.draw()
