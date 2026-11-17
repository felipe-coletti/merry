from itertools import pairwise

import pygame

from settings import FLOOR_COLOR, OBSTACLE_COLOR


def is_covered(rect, areas):
    """True se `rect` estiver inteiramente coberto pela união de `areas`.

    Divide `rect` nas bordas das áreas que o tocam e confere se o centro
    de cada célula está dentro de alguma área. Funciona mesmo quando o
    retângulo atravessa a emenda entre duas áreas.
    """
    clips = [
        clip for clip in (area.clip(rect) for area in areas)
        if clip.width and clip.height
    ]

    if not clips:
        return False

    xs = sorted({rect.left, rect.right}.union(
        edge for clip in clips for edge in (clip.left, clip.right)
    ))
    ys = sorted({rect.top, rect.bottom}.union(
        edge for clip in clips for edge in (clip.top, clip.bottom)
    ))

    for left, right in pairwise(xs):
        center_x = (left + right) / 2

        for top, bottom in pairwise(ys):
            center_y = (top + bottom) / 2

            if not any(
                clip.left <= center_x < clip.right
                and clip.top <= center_y < clip.bottom
                for clip in clips
            ):
                return False

    return True


class Level:
    def __init__(
        self,
        size,
        player_spawn,
        floor_areas,
        obstacles,
        enemies,
        ammo
    ):
        self.size = size
        self.player_spawn = player_spawn

        self.floor_areas = floor_areas
        self.obstacles = obstacles

        self.enemies = enemies
        self.ammo = ammo

        self.bounds = pygame.Rect((0, 0), self.size)

    def can_walk(self, movement_rect):
        return is_covered(movement_rect, self.floor_areas)

    def can_move(self, rect):
        # Só a metade de baixo (os pés) colide com o cenário.
        movement_rect = pygame.Rect(
            rect.left,
            rect.centery,
            rect.width,
            rect.height // 2
        )

        if not self.can_walk(movement_rect):
            return False

        return movement_rect.collidelist(self.obstacles) == -1

    def draw(self, screen, camera):
        for floor in self.floor_areas:
            pygame.draw.rect(screen, FLOOR_COLOR, camera.apply(floor))

        for obstacle in self.obstacles:
            pygame.draw.rect(screen, OBSTACLE_COLOR, camera.apply(obstacle))
