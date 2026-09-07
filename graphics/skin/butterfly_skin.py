import pygame
from graphics import spritesheet

class ButterflySkin:
    BORDER = 3
    SPACING = 3
    COLUMN_WIDTH = 34


    def __init__(self, path, scale=2, animation_speed=0.5):
        self.scale = scale
        self.animation_speed = animation_speed

        image = pygame.image.load(path).convert_alpha()
        sheet = spritesheet.Spritesheet(image)

        self.frames = self._load_frames(sheet)


    def _sprite(self, sheet, x, y):
        return sheet.get_image(
            0,
            x,
            y,
            42,
            34,
            self.scale,
            (0, 0, 0)
        )


    def _load_frames(self, sheet):
        return [
            self._sprite(sheet, 3, 6),
            self._sprite(sheet, 51, 6)
        ]
