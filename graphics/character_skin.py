import pygame
from graphics import spritesheet

class CharacterSkin:
    BORDER = 3
    SPACING = 3
    COLUMN_WIDTH = 23


    def __init__(self, path, scale = 2):
        self.scale = scale

        image = pygame.image.load(path).convert_alpha()
        sheet = spritesheet.Spritesheet(image)

        self.frames = self._load_frames(sheet)


    def _sprite(self, sheet, x, y):
        return sheet.get_image(
            0,
            x,
            y,
            26,
            38,
            self.scale,
            (0, 0, 0)
        )


    def _load_frames(self, sheet):
        down_0 = self._sprite(
            sheet,
            2,
            2
        )
        down_1 = self._sprite(
            sheet,
            30,
            2
        )
        down_2 = self._sprite(
            sheet,
            58,
            2
        )
        up_0 = self._sprite(
            sheet,
            2,
            42
        )
        up_1 = self._sprite(
            sheet,
            30,
            42
        )
        up_2 = self._sprite(
            sheet,
            58,
            42
        )
        right_0 = self._sprite(
            sheet,
            2,
            122
        )
        right_1 = self._sprite(
            sheet,
            30,
            122
        )
        right_2 = self._sprite(
            sheet,
            58,
            122
        )
        left_0 = self._sprite(
            sheet,
            2,
            82
        )
        left_1 = self._sprite(
            sheet,
            30,
            82
        )
        left_2 = self._sprite(
            sheet,
            58,
            82
        )

        return {
            "down": [down_0, down_1, down_0, down_2, down_0],
            "left": [left_0, left_1, left_0, left_2, left_0],
            "right": [right_0, right_1, right_0, right_2, right_0],
            "up": [up_0, up_1, up_0, up_2, up_0],
        }
