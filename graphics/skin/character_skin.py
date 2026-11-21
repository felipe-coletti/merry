import pygame

from graphics.spritesheet import Spritesheet


class CharacterSkin:
    FRAME_WIDTH = 26
    FRAME_HEIGHT = 38

    # Linha (y) de cada direção no spritesheet.
    ROWS = {
        "down": 2,
        "up": 42,
        "left": 82,
        "right": 122,
    }

    # Colunas (x) dos três quadros de cada direção.
    COLUMNS = (2, 30, 58)

    # Ordem dos quadros na animação de caminhada.
    WALK_CYCLE = (0, 1, 0, 2, 0)

    def __init__(self, image, scale=2):
        self.scale = scale

        sheet = Spritesheet(image)

        self.frames = self._load_frames(sheet)

        self.masks = {
            direction: [
                pygame.mask.from_surface(frame)
                for frame in frames
            ]
            for direction, frames in self.frames.items()
        }

    def _sprite(self, sheet, x, y):
        return sheet.get_image(
            x,
            y,
            self.FRAME_WIDTH,
            self.FRAME_HEIGHT,
            self.scale
        )

    def _load_frames(self, sheet):
        frames = {}

        for direction, y in self.ROWS.items():
            sprites = [
                self._sprite(sheet, x, y)
                for x in self.COLUMNS
            ]

            frames[direction] = [
                sprites[index]
                for index in self.WALK_CYCLE
            ]

        return frames
