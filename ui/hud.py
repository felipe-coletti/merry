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


    def _draw_text(
        self,
        screen,
        text,
        position,
        font,
        text_color=(255, 255, 255),
        outline_color=(0, 0, 0),
        outline_width=2
    ):
        for x in range(-outline_width, outline_width + 1):
            for y in range(-outline_width, outline_width + 1):
                if x == 0 and y == 0:
                    continue

                outline = font.render(
                    text,
                    True,
                    outline_color
                )

                screen.blit(
                    outline,
                    (
                        position[0] + x,
                        position[1] + y
                    )
                )

        text_surface = font.render(
            text,
            True,
            text_color
        )

        screen.blit(
            text_surface,
            position
        )


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

        self._draw_text(
            screen,
            f"HP: {player.health}",
            (
                position[0] + 8,
                position[1] - 2
            ),
            self.font
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

        self._draw_text(
            screen,
            f"Adrenaline: {int(player.adrenaline)}",
            (
                position[0] + 8,
                position[1] - 2
            ),
            self.font
        )

    def _draw_ammo(self, screen, player):
        weapon = player.weapon
        screen_width = screen.get_width()

        ammo_text = f"{weapon.ammo} / {weapon.capacity}"
        ammo_surface = self.font.render(
            ammo_text,
            True,
            TEXT_COLOR
        )

        ammo_position = (
            screen_width - ammo_surface.get_width() - self.MARGIN,
            self.MARGIN
        )

        self._draw_text(
            screen,
            ammo_text,
            ammo_position,
            self.font
        )

        reserve_text = f"Reserve: {weapon.reserve_ammo}"
        reserve_surface = self.small_font.render(
            reserve_text,
            True,
            TEXT_COLOR
        )

        reserve_position = (
            screen_width - reserve_surface.get_width() - self.MARGIN,
            ammo_position[1] + 30
        )

        self._draw_text(
            screen,
            reserve_text,
            reserve_position,
            self.small_font
        )

        if weapon.reloading:
            reload_text = "Reloading..."
            reload_surface = self.small_font.render(
                reload_text,
                True,
                TEXT_COLOR
            )

            reload_position = (
                screen_width - reload_surface.get_width() - self.MARGIN,
                reserve_position[1] + 25
            )

            self._draw_text(
                screen,
                reload_text,
                reload_position,
                self.small_font
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