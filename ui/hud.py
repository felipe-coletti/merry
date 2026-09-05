import pygame

from settings import TEXT_COLOR

class HUD:
    MARGIN = 20

    BAR_WIDTH = 200
    BAR_HEIGHT = 20

    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)

    def draw(self, screen, player):
        self._draw_health(screen, player)
        self._draw_adrenaline(screen, player)
        self._draw_ammo(screen, player)

    def _draw_health(self, screen, player):
        position = (
            self.MARGIN,
            self.MARGIN
        )

        self._draw_bar(
            screen,
            position,
            self.BAR_WIDTH,
            self.BAR_HEIGHT,
            player.health,
            100,
            (120, 30, 30),
            (220, 60, 60)
        )

        text = self.font.render(
            f"HP: {player.health}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (
                position[0] + 8,
                position[1] - 2
            )
        )

    def _draw_adrenaline(self, screen, player):
        position = (
            self.MARGIN,
            self.MARGIN + 35
        )

        self._draw_bar(
            screen,
            position,
            self.BAR_WIDTH,
            self.BAR_HEIGHT,
            player.adrenaline,
            player.max_adrenaline,
            (80, 50, 20),
            (255, 180, 50)
        )

        text = self.font.render(
            f"Adrenaline: {int(player.adrenaline)}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (
                position[0] + 8,
                position[1] - 2
            )
        )

    def _draw_ammo(self, screen, player):
        weapon = player.weapon

        screen_width = screen.get_width()

        ammo_text = self.font.render(
            f"{weapon.ammo} / {weapon.capacity}",
            True,
            TEXT_COLOR
        )

        ammo_position = (
            screen_width - ammo_text.get_width() - self.MARGIN,
            self.MARGIN
        )

        screen.blit(
            ammo_text,
            ammo_position
        )

        reserve_text = self.small_font.render(
            f"Reserve: {weapon.reserve_ammo}",
            True,
            TEXT_COLOR
        )

        reserve_position = (
            screen_width - reserve_text.get_width() - self.MARGIN,
            ammo_position[1] + 30
        )

        screen.blit(
            reserve_text,
            reserve_position
        )

        if weapon.reloading:
            reload_text = self.small_font.render(
                "Reloading...",
                True,
                TEXT_COLOR
            )

            reload_position = (
                screen_width - reload_text.get_width() - self.MARGIN,
                reserve_position[1] + 25
            )

            screen.blit(
                reload_text,
                reload_position
            )

    def _draw_bar(
        self,
        screen,
        position,
        width,
        height,
        value,
        maximum,
        background_color,
        fill_color
    ):
        background = pygame.Rect(
            position[0],
            position[1],
            width,
            height
        )

        pygame.draw.rect(
            screen,
            background_color,
            background
        )

        if maximum <= 0:
            return

        ratio = max(
            0,
            min(value / maximum, 1)
        )

        fill = pygame.Rect(
            position[0],
            position[1],
            width * ratio,
            height
        )

        pygame.draw.rect(
            screen,
            fill_color,
            fill
        )