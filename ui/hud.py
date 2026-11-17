import math

import pygame


class HUD:
    MARGIN = 20

    BAR_WIDTH = 200
    BAR_HEIGHT = 20

    TEXT_COLOR = (255, 255, 255)
    OUTLINE_COLOR = (0, 0, 0)
    OUTLINE_WIDTH = 2

    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)

    def draw(self, screen, player):
        self._draw_health(screen, player)
        self._draw_adrenaline(screen, player)
        self._draw_ammo(screen, player)

    def _draw_text(self, screen, text, position, font):
        outline = font.render(text, True, self.OUTLINE_COLOR)

        width = self.OUTLINE_WIDTH

        for x in range(-width, width + 1):
            for y in range(-width, width + 1):
                if x or y:
                    screen.blit(outline, (position[0] + x, position[1] + y))

        screen.blit(font.render(text, True, self.TEXT_COLOR), position)

    def _draw_right_aligned_text(self, screen, text, y, font):
        x = screen.get_width() - font.size(text)[0] - self.MARGIN

        self._draw_text(screen, text, (x, y), font)

    def _draw_health(self, screen, player):
        position = (self.MARGIN, self.MARGIN)

        self._draw_bar(
            screen,
            position,
            player.health,
            player.max_health,
            (120, 30, 30),
            (220, 60, 60)
        )

        # Arredonda para cima: o jogador só vê 0 quando realmente morreu.
        self._draw_text(
            screen,
            f"HP: {math.ceil(player.health)}",
            (position[0] + 8, position[1] - 2),
            self.font
        )

    def _draw_adrenaline(self, screen, player):
        position = (self.MARGIN, self.MARGIN + 35)

        self._draw_bar(
            screen,
            position,
            player.adrenaline,
            player.max_adrenaline,
            (80, 50, 20),
            (255, 180, 50)
        )

        self._draw_text(
            screen,
            f"Adrenaline: {int(player.adrenaline)}",
            (position[0] + 8, position[1] - 2),
            self.font
        )

    def _draw_ammo(self, screen, player):
        weapon = player.weapon

        y = self.MARGIN

        self._draw_right_aligned_text(
            screen,
            f"{weapon.ammo} / {weapon.capacity}",
            y,
            self.font
        )

        y += 30

        self._draw_right_aligned_text(
            screen,
            f"Reserve: {weapon.reserve_ammo}",
            y,
            self.small_font
        )

        if weapon.reloading:
            self._draw_right_aligned_text(
                screen,
                "Reloading...",
                y + 25,
                self.small_font
            )

    def _draw_bar(
        self,
        screen,
        position,
        value,
        maximum,
        background_color,
        fill_color
    ):
        background = pygame.Rect(position, (self.BAR_WIDTH, self.BAR_HEIGHT))

        pygame.draw.rect(screen, background_color, background)

        if maximum <= 0:
            return

        ratio = max(0, min(value / maximum, 1))

        fill = pygame.Rect(
            position,
            (self.BAR_WIDTH * ratio, self.BAR_HEIGHT)
        )

        pygame.draw.rect(screen, fill_color, fill)
