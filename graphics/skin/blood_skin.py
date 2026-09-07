import pygame

from graphics import spritesheet

class BloodSkin:
    FRAME_WIDTH = 32
    FRAME_HEIGHT = 32
    FRAME_COUNT = 8

    def __init__(self, path, scale=2):
        self.scale = scale

        image = pygame.image.load(path).convert_alpha()
        sheet = spritesheet.Spritesheet(image)

        self.frames = self._load_frames(sheet)

    def _sprite(self, sheet, x):
        return sheet.get_image(
            0,
            x,
            0,
            self.FRAME_WIDTH,
            self.FRAME_HEIGHT,
            self.scale,
            (0, 0, 0)
        )

    def _load_frames(self, sheet):
        return [
            self._sprite(
                sheet,
                index * self.FRAME_WIDTH
            )
            for index in range(self.FRAME_COUNT)
        ]